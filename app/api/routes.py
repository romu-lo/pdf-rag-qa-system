from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"message": "API Online"}

@router.post("/documents")
async def upload_documents():
    return {"message": "Document uploaded successfully"}
