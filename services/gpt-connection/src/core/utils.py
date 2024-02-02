import pandas as pd
import numpy as np
import pgvector
import re
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from langchain.chains import RetrievalQA
from langchain.vectorstores.pgvector import PGVector
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from src.config import settings

OPENAI_API_KEY  = settings.OPENAI_API_KEY
PG_DB_PW = settings.POSTGRES_DB_PASSWORD
host = settings.POSTGRES_DB_HOST
port = settings.POSTGRES_DB_PORT
user = settings.POSTGRES_DB_USER
password = settings.POSTGRES_DB_PASSWORD
dbname = settings.POSTGRES_DB_DBNAME
collection_name = settings.PGVECTOR_COLLECTION_NAME


def remove_unicode_chars(input_str):
    """
    Removes unicode characters from string
    """
    string_encode = input_str.encode("ascii", "ignore")
    string_decode = string_encode.decode()
    string_decode = re.sub(r"[^ -~].*", "", string_decode)
    return string_decode


def replace_multiple_spaces_dots(input):
    """
    Cleans text by removing multiple spaces and/or periods replaced with a single space or period.
    """
    response = re.sub(r"\s+", " ", input)
    response = re.sub(r"\.\.+", ".", response)
    return response


def clean_and_validate_input(input):
    """
    Cleans input by removing unicode chars and excess spaces and periods.
    Validates that input is not just numbers and/or empty
    """
    input = input.strip().lstrip("0123456789.-")
    input = remove_unicode_chars(input)
    input = replace_multiple_space_dots(input)
    input = input.strip()

    if input != "":
        return input, "pass"
    else:
        return input, "fail"



def get_conn_string():
    CONNECTION_STRING = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return CONNECTION_STRING


def get_retriever(collection_name=collection_name):
    store = PGVector(
        collection_name=collection_name,
        connection_string=get_conn_string(),
        embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    )
    return store.as_retriever()


def get_llm(temp = 0.0, model_name='gpt-3.5-turbo-16k'):
    llm = ChatOpenAI(temperature = temp, model = model_name, openai_api_key = OPENAI_API_KEY)
    return llm


def get_qa_chain():
    qa_chain_with_sources = RetrievalQA.from_chain_type(
        llm=get_llm(), 
        chain_type="stuff", 
        retriever=get_retriever(),
        return_source_documents=True,
        verbose=True,
    )
    return qa_chain_with_sources


# Construct a single string with the LLM output and the source titles and urls
def construct_result_with_sources(responses, source_content, source_metadata):
    result = responses['result']
    result += "\n\n"
    result += "Sources used:"
    for i in range(len(source_content)):    
        result += "\n\n"
        result += source_metadata[i]['title']
        result += "\n\n"
        return result


def ask(query):
    qa_chain = get_qa_chain()
    query =  "How does a quasar die?"

    responses = qa_chain({"query": query})

    source_documents = responses["source_documents"]
    source_content = [doc.page_content for doc in source_documents]
    source_metadata = [doc.metadata for doc in source_documents]
    answer = construct_result_with_sources(responses, source_content, source_metadata)

    return answer