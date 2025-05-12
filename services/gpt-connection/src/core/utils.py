import pandas as pd
import numpy as np
import pgvector
import re
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import ChatOpenAI, AzureChatOpenAI, OpenAIEmbeddings, AzureOpenAIEmbeddings

from src.config import settings

# Environment/config settings
OPENAI_API_KEY = settings.OPENAI_API_KEY
host = settings.POSTGRES_DB_HOST
port = settings.POSTGRES_DB_PORT
user = settings.POSTGRES_DB_USER
password = settings.POSTGRES_DB_PASSWORD
dbname = settings.POSTGRES_DB_DBNAME
collection_name = settings.PGVECTOR_COLLECTION_NAME

def get_conn_string():
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

CONNECTION_STRING = get_conn_string()

# --- Text Cleaning Utilities ---

def remove_unicode_chars(input_str):
    return re.sub(r"[^\x00-\x7F]+", "", input_str)

def replace_multiple_spaces_dots(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\.\.+", ".", text)
    return text

def clean_and_validate_input(input_text):
    input_text = input_text.strip().lstrip("0123456789.-")
    input_text = remove_unicode_chars(input_text)
    input_text = replace_multiple_spaces_dots(input_text).strip()
    return (input_text, "pass") if input_text else (input_text, "fail")

# --- LangChain Setup Utilities ---

def get_retriever(collection_name=collection_name):
    store = PGVector(
        collection_name=collection_name,
        connection_string=CONNECTION_STRING,
        embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
    )
    return store.as_retriever()

def get_llm(temp=0.0, model_name='gpt-3.5-turbo-16k'):
    return ChatOpenAI(temperature=temp, model=model_name, openai_api_key=OPENAI_API_KEY)

def get_qa_chain():
    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=get_retriever(),
        return_source_documents=True,
        verbose=True,
    )

def construct_result_with_sources(responses, source_content, source_metadata):
    result = responses['result'] + "\n\nSources used:"
    for i in range(len(source_content)):
        result += f"\n\n{source_metadata[i].get('title', 'Unknown Title')}"
    return result

# --- Main LLM Query Function ---

def ask(query, api_key, deployment_name=None, api_base=None, api_version=None):
    print("💬 Using API key:", api_key[:10], "..." if api_key else "(none)")
    if api_base and deployment_name:
        embeddings = AzureOpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=api_base,
            openai_api_version=api_version,
            deployment=deployment_name,
        )
        llm = AzureChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=api_base,
            openai_api_version=api_version,
            deployment_name=deployment_name,
        )
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        llm = ChatOpenAI(openai_api_key=api_key)

    store = PGVector(
        collection_name=collection_name,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )

    retriever = store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.invoke({"query": query})["result"]
