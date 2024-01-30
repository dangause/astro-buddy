import pyscopg2
import openai
from langchain.document_loaders import DataFrameLoader
from langchain.vectorstores.pgvector import PGVector

from src.config import settings


OPENAI_API_KEY  = settings.OPENAI_API_KEY
PG_DB_PW = settings.POSTGRES_DB_PASSWORD
host= settings.POSTGRES_DB_HOST
port= settings.POSTGRES_DB_PORT
user= settings.POSTGRES_DB_USER
password= settings.POSTGRES_DB_PASSWORD
dbname= settings.POSTGRES_DB_DBNAME


def get_connection_str():
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
 
def get_conn_cur():
    conn = psycopg2.connect(get_connection_str())
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector");
    conn.commit()
    return conn, cur

def get_langchain_docs_from_df(df):
    loader = DataFrameLoader(df, page_content_column = 'content')
    return loader.load()

class VectorStore:
    """
    Description here
    """

    def __init__(self, )
        store = PGVector(
            collection_name=collection_name,
            connection_string=CONNECTION_STRING,
            embedding_function=embeddings,
        )