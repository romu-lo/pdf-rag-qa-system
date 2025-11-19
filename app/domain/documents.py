import os
import re

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PDFMinerLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
)
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _can_load(file_path: str) -> bool:
    """
    Check if the file can be loaded based on its extension.
    Only PDF files are supported.
    """
    return re.search(r'\.pdf$', file_path, re.IGNORECASE) is not None

def _split_chunks(
    documents:list[Document],
    chunk_size:int=1024,
    chunk_overlap:int=256,
) -> list[Document]:
    """
    Recursively split documents into smaller chunks for retrieval.
    Tries to split on natural boundaries first (e.g., paragraphs, sentences, words).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def _initialize_embedding_model() -> OpenAIEmbeddings:
    """
    Initialize and return the Embeddings model.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

def _initialize_vector_db() -> Chroma:
    """
    Initialize and return the Vector Database instance.
    """
    embeddings = _initialize_embedding_model()
    return Chroma(
        collection_name="knowledge_base",
        embedding_function=embeddings,
        persist_directory="../../vector_db",
    )

def _insert_into_vector_db(vector_db: Chroma, file_path: str, documents: list[Document]):
    """
    Generate IDs and insert documents into the vector database.
    """
    source_name = os.path.splitext(os.path.basename(file_path))[0]
    ids = [f"{source_name}_{i}" for i in range(len(documents))]

    try:
        vector_db.add_documents(documents, ids=ids)

    except Exception as e:
        raise RuntimeError(
            f"Failed to insert documents into vector database: {e}"
        ) from e

    return {"status": "success", "total_chunks": int(len(documents))}


def load_file(file_path: str):
    if _can_load(file_path):
        loader = PDFMinerLoader(file_path)
        documents = loader.load()
        chunks = _split_chunks(documents)
        vector_db = _initialize_vector_db()

        return _insert_into_vector_db(vector_db, file_path, chunks)

    else:
        raise ValueError("Unsupported file format. Please upload a PDF file.")
