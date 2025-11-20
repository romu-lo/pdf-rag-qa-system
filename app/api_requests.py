from typing import Annotated

import constants as constants
import requests
from fastapi import File, UploadFile
from fastapi.exceptions import HTTPException


def health_check() -> dict:
    """
    Call GET /health to test if API is online.
    """
    try:
        response = requests.get(constants.HEALTH_ENDPOINT)
        response.raise_for_status()
        return response.status_code

    except requests.RequestException:
        return {"status": 404}

def upload_documents(uploaded_files: Annotated[list[UploadFile], File(...)]) -> dict:
    """
    Call POST /documents sending multiple PDF files (multipart/form-data).
    """
    files = [
        ("files", (file.name, file.getvalue(), "application/pdf"))
        for file in uploaded_files
    ]

    response = requests.post(constants.DOCUMENTS_ENDPOINT, files=files)

    response.raise_for_status()
    return response.json()

def clear_documents() -> dict:
    """
    Call DELETE /documents to clear all indexed documents.
    """
    response = requests.delete(constants.DOCUMENTS_ENDPOINT)
    response.raise_for_status()
    return response.json()


def ask_question(question: str) -> dict:
    """
    Call POST /question sending a question and getting an answer.
    """
    response = requests.post(constants.QUESTION_ENDPOINT, params={"question": question})
    response.raise_for_status()
    return response.json()
