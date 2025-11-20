import shutil
import tempfile
from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.core import LLMResponse, UploadResponse
from app.domain import answer_question, upload_files

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"message": "API Online"}

@router.post("/documents")
async def upload_documents(
    files: Annotated[list[UploadFile], File(...)]
) -> UploadResponse:
    """
    Upload, break in chunks, embed, and index PDF file contents for question answering.
    """
    temp_paths = []

    for uploaded_file in files:
        suffix = "." + uploaded_file.filename.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:

            shutil.copyfileobj(uploaded_file.file, tmp)
            temp_paths.append(tmp.name)

    result = upload_files(temp_paths)

    return result

@router.post("/question")
async def ask_question(question: str) -> LLMResponse:
    """
    Ask a question and get an answer based on the indexed documents.
    """
    return answer_question(question)
