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


# def get_arxiv_pdfs_to_df():
#     papers = fetch_arxiv_papers()
#     existing_ids = get_existing_ids()
#     data = []
#     for paper in papers:
#         paper_id = paper.get_short_id()
#         if paper_id in existing_ids:
#             continue
#         with tempfile.TemporaryDirectory() as tmpdirname:
#             pdf_path = os.path.join(tmpdirname, f"{paper_id}.pdf")
#             paper.download_pdf(dirpath=tmpdirname, filename=f"{paper_id}.pdf")
#             content = read_pdf(pdf_path)
#         data.append({
#             "id": paper_id,
#             "title": paper.title,
#             "categories": paper.categories,
#             "abstract": paper.summary,
#             "created": paper.published.strftime('%Y-%m-%d'),
#             "authors": [author.name for author in paper.authors],
#             "content": content
#         })
#     df = pd.DataFrame(data)
#     df = df.dropna().reset_index(drop=True)
#     df = df.map(lambda x: str(x).replace("\x00", "\uFFFD"))
#     print(f"Estimated embedding cost: ${get_total_embeddings_cost(df):.4f}")
#     return df



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

# def insert_embeddings_into_db(chunked_documents, reset_db=False):
#     CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
#     print('connecting to db through psycopg2')
#     conn = psycopg2.connect(CONNECTION_STRING)
#     cur = conn.cursor()
#     cur.execute("CREATE EXTENSION IF NOT EXISTS vector");
#     conn.commit()

#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#     print('Inserting documents into DB via PGVector Langchain')
#     db = PGVector.from_documents(
#         documents=chunked_documents,
#         embedding=embeddings,
#         collection_name=collection_name,
#         connection_string=CONNECTION_STRING,
#         distance_strategy=DistanceStrategy.COSINE,
#         pre_delete_collection=reset_db 
#     )
#     return None


# def ingest_arxiv(date_from="2020-02-05", date_until=today, reset_db=False):
#     try:
#         print(f'Step 1: Getting arxiv articles from {date_from} to {date_until} into a df')
#         df = get_arxiv_pdfs_to_df(date_from, date_until)
#     except Exception as e:
#         print(getattr(e, 'message', str(e)))
#     try:
#         print('Step 2: arxiv df to chunked docs')
#         chunked_documents = pdf_df_to_chunked_docs_l(df)
#     except Exception as e:
#         print(getattr(e, 'message', str(e)))
#     try:
#         print('Step 3: insert embeddings into postgreSQL')
#         insert_embeddings_into_db(chunked_documents, reset_db=reset_db)
#         print('Embedded chunked documents inserted into postgreSQL database')
#     except Exception as e:
#         print(getattr(e, 'message', str(e)))
#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "message": "This weeks' arxiv articles successfully chunked, embedded, and inserted into postgreSQL database.",
#         }),
#     }


def delete_collection(collection_name = collection_name, connection_string = CONNECTION_STRING):
    store = PGVector(
        collection_name=collection_name,
        connection_string=connection_string,
        embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    )

    store.delete_collection()

    return 'Collection deleted.'















import os
import json
import tempfile
import datetime as DT
import pandas as pd
import arxiv
import tiktoken
import psycopg2
from pypdf import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_community.document_loaders import DataFrameLoader
from src.config import settings

# Configuration
OPENAI_API_KEY = settings.OPENAI_API_KEY
PG_DB_PW = settings.POSTGRES_DB_PASSWORD
host = settings.POSTGRES_DB_HOST
port = settings.POSTGRES_DB_PORT
user = settings.POSTGRES_DB_USER
password = settings.POSTGRES_DB_PASSWORD
dbname = settings.POSTGRES_DB_DBNAME
collection_name = settings.PGVECTOR_COLLECTION_NAME

def get_conn_string():
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

CONNECTION_STRING = get_conn_string()

def read_pdf(file_path):
    pdf_reader = PdfReader(file_path, strict=False)
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    if not string:
        return 0
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def get_embedding_cost(num_tokens):
    return num_tokens / 1000 * 0.0001

def get_total_embeddings_cost(df):
    total_tokens = sum(num_tokens_from_string(text) for text in df['content'])
    return get_embedding_cost(total_tokens)

def get_existing_ids():
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute("SELECT cmetadata->>'id' FROM langchain_pg_embedding")
    existing_ids = {row[0] for row in cur.fetchall()}
    conn.close()
    return existing_ids

def fetch_arxiv_papers(query="quasar", max_results=100):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    return list(search.results())

def get_arxiv_pdfs_to_df():
    papers = fetch_arxiv_papers()
    existing_ids = get_existing_ids()
    data = []
    for paper in papers:
        paper_id = paper.get_short_id()
        if paper_id in existing_ids:
            continue
        with tempfile.TemporaryDirectory() as tmpdirname:
            pdf_path = os.path.join(tmpdirname, f"{paper_id}.pdf")
            paper.download_pdf(dirpath=tmpdirname, filename=f"{paper_id}.pdf")
            content = read_pdf(pdf_path)
        data.append({
            "id": paper_id,
            "title": paper.title,
            "categories": paper.categories,
            "abstract": paper.summary,
            "created": paper.published.strftime('%Y-%m-%d'),
            "authors": [author.name for author in paper.authors],
            "content": content
        })
    df = pd.DataFrame(data)
    df = df.dropna().reset_index(drop=True)
    df = df.map(lambda x: str(x).replace("\x00", "\uFFFD"))
    print(f"Estimated embedding cost: ${get_total_embeddings_cost(df):.4f}")
    return df

def pdf_df_to_chunked_docs_l(df):
    loader = DataFrameLoader(df, page_content_column='content')
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name='cl100k_base',
        chunk_size=1024,
        chunk_overlap=50,
    )
    return splitter.split_documents(docs)

def insert_embeddings_into_db(chunked_documents, reset_db=False):
    print(f"Inserting {len(chunked_documents)} chunks into PGVector...")
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    conn.close()

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # Create PGVector store instance ahead of time
    vectorstore = PGVector(
        collection_name=collection_name,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        distance_strategy=DistanceStrategy.COSINE,
    )

    batch_size = 100  # Adjust as needed to stay under 300k token limit
    for i in range(0, len(chunked_documents), batch_size):
        batch = chunked_documents[i:i + batch_size]
        print(f"  ➜ Embedding batch {i // batch_size + 1} of {((len(chunked_documents)-1)//batch_size)+1}")
        vectorstore.add_documents(batch)

    print("✓ Insertion complete.")

def ingest_arxiv(reset_db=False):
    try:
        print("Fetching new arXiv papers...")
        df = get_arxiv_pdfs_to_df()
        if df.empty:
            print("No new papers to ingest.")
            return
        print("Chunking documents...")
        chunked_documents = pdf_df_to_chunked_docs_l(df)
        print("Inserting embeddings into the database...")
        insert_embeddings_into_db(chunked_documents, reset_db=reset_db)
        print("Ingestion complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
