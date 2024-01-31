import pyscopg2
import openai
from langchain_openai import OpenAIEmbeddings
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
)

from langchain.document_loaders import DataFrameLoader
from langchain.vectorstores.pgvector import PGVector
from langchain_core.documents.base import Document

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

    def __init__(self, collection_name='arxiv', connection_string=get_connection_str(), embedding_function=OpenAIEmbeddings()):
        self.collection_name=collection_name,
        self.connection_string=connection_string,
        self.embedding_function=embedding_function

    def connect_to_existing_vs_collection(self):
        try:
            self.store = PGVector(
                collection_name=self.collection_name,
                connection_string=self.connection_string,
                embedding_function=self.embedding_function,
            )
        except Exception as e:
            print(e)
    
    def add_documents(self, docs:Document):
        return None

    def add_texts(self, texts:Iterable[str],
                  metadatas: Optional[List[dict]] = None,
                  ids: Optional[List[str]] = None,):
        

