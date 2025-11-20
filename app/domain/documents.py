import os
import re

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PDFMinerLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
)
from langchain_core.documents import Document
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core import UploadResponse, constants, settings
from app.infrastructure import initialize_vector_db, insert_documents

load_dotenv()

def _is_pdf(file_path: str) -> bool:
    """
    Check if the file can be loaded based on its extension.
    Only PDF files are supported.
    """
    return re.search(constants.FILE_PATTERN, file_path, re.IGNORECASE) is not None

def _extract_file_name(file_path: str) -> str:
    """
    Extract the file name without extension from the file path.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def _split_chunks(
    documents: list[Document],
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap,
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

def _insert_into_vector_db(
    vector_db: Chroma,
    source_name: str,
    documents: list[Document],
) -> dict[str, str | int]:
    """
    Generate IDs and insert documents into the vector database.
    """
    ids: list[str] = [f"{source_name}_{i}" for i in range(len(documents))]

    try:
        insert_documents(vector_db, documents, ids=ids)
        return {
            "status": "success",
            "total_chunks": int(len(documents)),
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to insert documents into vector database: {e}"
        ) from e



def upload_files(file_paths: list[str]) -> UploadResponse:
    """"
    Process and upload files to the vector database.
    Currently supports only PDF files.
    """
    vector_db = initialize_vector_db()
    insertion_responses = []

    for file_path in file_paths:

        if _is_pdf(file_path):
            loader = PDFMinerLoader(file_path)
            documents = loader.load()
            chunks = _split_chunks(documents)

            source_name = _extract_file_name(file_path)
            insertion_response = _insert_into_vector_db(vector_db, source_name, chunks)
            insertion_responses.append(insertion_response)

        else:
            raise ValueError(
                f"""Unsupported file format for file: {source_name}.
                Please upload a PDF file."""
            )

    return UploadResponse(
        message="Documents processed successfully",
        documents_indexed=len(insertion_responses),
        total_chunks=sum(
            resp["total_chunks"] for resp in insertion_responses
        ),
    )
