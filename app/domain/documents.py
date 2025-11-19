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

def _extract_file_name(file_path: str) -> str:
    """
    Extract the file name without extension from the file path.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

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

def _insert_into_vector_db(
    vector_db: Chroma,
    source_name: str,
    documents: list[Document],
) -> dict:
    """
    Generate IDs and insert documents into the vector database.
    """
    ids = [f"{source_name}_{i}" for i in range(len(documents))]

    try:
        vector_db.add_documents(documents, ids=ids)

    except Exception as e:
        raise RuntimeError(
            f"Failed to insert documents into vector database: {e}"
        ) from e

    return {"status": "success", "total_chunks": int(len(documents))}


def upload_files(file_paths: list[str]) -> dict:
    vector_db = _initialize_vector_db()
    insertion_responses = []

    for file_path in file_paths:
        source_name = _extract_file_name(file_path)

        if _can_load(file_path):
            loader = PDFMinerLoader(file_path)
            documents = loader.load()
            chunks = _split_chunks(documents)

            insertion_response = _insert_into_vector_db(vector_db, source_name, chunks)
            insertion_responses.append(insertion_response)

        else:
            raise ValueError(
                f"""Unsupported file format for file: {source_name}.
                Please upload a PDF file."""
            )

    return {
        "message": "Documents processed successfully",
        "documents_indexed": len(insertion_responses),
        "total_chunks": sum(
            resp["total_chunks"] for resp in insertion_responses
        ),
    }
