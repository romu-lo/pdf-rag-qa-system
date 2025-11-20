from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever

from app.core import constants, settings

from .language_models import initialize_embedding_model


def initialize_vector_db(
    collection_name: str= constants.COLLECTION_NAME,
    persist_directory: Path = constants.VECTOR_DIR,
) -> Chroma:
    """
    Initialize and return the Vector Database instance.
    """
    return Chroma(
        collection_name=collection_name,
        embedding_function=initialize_embedding_model(),
        persist_directory=persist_directory,
    )

def initialize_retriever(
    search_type: str = settings.search_type,
    k: int = settings.k,
    fetch_k: int = settings.fetch_k,
    lambda_mult: float = settings.lambda_mult,
) -> VectorStoreRetriever:
    """
    Initialize and return the retriever from the vector database.
    """
    vector_db = initialize_vector_db()

    kwargs = {
        "k": k,
        "fetch_k": fetch_k,
        "lambda_mult": lambda_mult,
    }

    return vector_db.as_retriever(
        search_type=search_type,
        search_kwargs=kwargs,
    )

def insert_documents(
    vector_db: Chroma,
    documents: list[Document],
    ids: list[str],
) -> list[str]:
    """
    Insert documents into the vector database.
    Returns the list of inserted documents IDs.
    """
    return vector_db.add_documents(documents, ids=ids)

def retrieve_documents(
    retriever: VectorStoreRetriever,
    query: str,
) -> list:
    """
    Retrieve documents from the vector database based on the query.
    """
    return retriever.invoke(query)
