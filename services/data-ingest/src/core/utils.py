import pandas as pd
import arxivscraper.arxivscraper as ax
import arxiv
import tiktoken
import psycopg2
import re
import pgvector
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_community.document_loaders import DataFrameLoader
import os 
from pypdf import PdfReader
import tempfile
import json
import pandas as pd
import datetime as DT

from src.config import settings

OPENAI_API_KEY  = settings.OPENAI_API_KEY
PG_DB_PW = settings.POSTGRES_DB_PASSWORD
host = settings.POSTGRES_DB_HOST
port = settings.POSTGRES_DB_PORT
user = settings.POSTGRES_DB_USER
password = settings.POSTGRES_DB_PASSWORD
dbname = settings.POSTGRES_DB_DBNAME
collection_name = settings.PGVECTOR_COLLECTION_NAME

def get_today_and_n_days_ago(n):
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=n)
    today = today.strftime('%Y-%m-%d')
    week_ago = week_ago.strftime('%Y-%m-%d')
    return today, week_ago

today, week_ago = get_today_and_n_days_ago(7)

def get_conn_string():
    CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return CONNECTION_STRING

CONNECTION_STRING = get_conn_string()

def read_pdf(file_path):
    pdf_reader = PdfReader(file_path, strict=False)
    text = ""

    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:  # Check if text is extracted successfully
            text += extracted_text + "\n"  # Append text of each page

    return text

        
# Helper functions to help us create the embeddings
# Helper func: calculate number of tokens
def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    if not string:
        return 0
    # Returns the number of tokens in a text string
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Helper function: calculate cost of embedding num_tokens
# Assumes we're using the text-embedding-ada-002 model
# See https://openai.com/pricing
def get_embedding_cost(num_tokens):
    return num_tokens/1000*0.0001


# Helper function: calculate total cost of embedding all content in the dataframe
def get_total_embeddings_cost(df):
    total_tokens = 0
    for i in range(len(df.index)):
        text = df['content'][i]
        token_len = num_tokens_from_string(text)
        total_tokens = total_tokens + token_len
    total_cost = get_embedding_cost(total_tokens)
    return total_cost


def get_arxiv_pdfs_to_df(date_from="2024-01-22", date_until="2024-01-29"):
    scraper = ax.Scraper(
        category="physics:astro-ph",
        date_from=date_from,
        date_until=date_until,
        t=10,
        filters={"abstract": ["quasar"]},
    )
    try:
        output = scraper.scrape()
    except Exception as e:
        raise e
        
    cols = ["id", "title", "categories", "abstract", "doi", "created", "updated", "authors"]
    df = pd.DataFrame(output, columns=cols)
    df['id_no_period'] = df.id.apply(lambda x: x.replace(".",""))

    for index, row in df.iterrows():
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[row['id']])))
        # Download the PDF to a specified directory with a custom filename.
        pdf_filename = row['id_no_period']+'.pdf'

        with tempfile.TemporaryDirectory() as tmpdirname:
            paper.download_pdf(dirpath=tmpdirname, filename=pdf_filename)
            tmp_filepath = os.path.join(tmpdirname, pdf_filename)
            df.loc[index, 'content'] = read_pdf(tmp_filepath)

    # drop columns that have a lot of nas, then drop all rows with remaining nas
    df = df.drop(['doi', 'updated'], axis=1)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df = df.map(lambda x: str(x).replace("\x00", "\uFFFD"))
    print(get_total_embeddings_cost(df))

    return df


def pdf_df_to_chunked_docs_l(df):
    #load documents from Pandas dataframe for insertion into database
    # page_content_column is the column name in the dataframe to create embeddings for
    loader = DataFrameLoader(df, page_content_column = 'content')
    docs = loader.load()
    # Initialize the RecursiveCharacterTextSplitter with the desired parameters
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(encoding_name='cl100k_base',
                                                                    chunk_size=1024,  # Maximum size of chunks to return
                                                                    chunk_overlap=50,)

    chunked_documents = splitter.split_documents(docs)

    return chunked_documents

def insert_embeddings_into_db(chunked_documents, reset_db=False):
    CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    print('connecting to db through psycopg2')
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector");
    conn.commit()

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    print('Inserting documents into DB via PGVector Langchain')
    db = PGVector.from_documents(
        documents=chunked_documents,
        embedding=embeddings,
        collection_name=collection_name,
        connection_string=CONNECTION_STRING,
        distance_strategy=DistanceStrategy.COSINE,
        pre_delete_collection=reset_db 
    )
    return None


def ingest_arxiv(date_from="2023-02-05", date_until=today, reset_db=False):
    print(f'Step 1: Getting arxiv articles from {date_from} to {date_until} into a df')
    df = get_arxiv_pdfs_to_df(date_from, date_until)
    print('Step 2: arxiv df to chunked docs')
    chunked_documents = pdf_df_to_chunked_docs_l(df)
    print('Step 3: insert embeddings into postgreSQL')
    insert_embeddings_into_db(chunked_documents, reset_db=reset_db)
    print('Embedded chunked documents inserted into postgreSQL database')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "This weeks' arxiv articles successfully chunked, embedded, and inserted into postgreSQL database.",
        }),
    }


def delete_collection(collection_name = collection_name, connection_string = CONNECTION_STRING):
    store = PGVector(
        collection_name=collection_name,
        connection_string=connection_string,
        embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    )

    store.delete_collection()

    return 'Collection deleted.'