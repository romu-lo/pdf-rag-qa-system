from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    documents_indexed: int
    total_chunks: int

