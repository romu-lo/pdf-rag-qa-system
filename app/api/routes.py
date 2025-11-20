import shutil
import tempfile
from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.domain import UploadResponse, answer_question, upload_files

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"message": "API Online"}

@router.post("/documents")
async def upload_documents(
    files: Annotated[list[UploadFile], File(...)]
):
    temp_paths = []

    for uploaded_file in files:
        suffix = "." + uploaded_file.filename.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:

            shutil.copyfileobj(uploaded_file.file, tmp)
            temp_paths.append(tmp.name)

    result = upload_files(temp_paths)

    return result

# TODO def get_temp_path(upload_arquivos) -> str:
#    temp_dir = tempfile.mkdtemp()
#
#    for arquivo in upload_arquivos:
#        path = os.path.join(temp_dir, arquivo.name)
#        with open(path, "wb") as f:
#            f.write(arquivo.getvalue())
#    return temp_dir

@router.post("/question")
async def ask_question(question: str):
    return {"message": "Document uploaded successfully"}
