from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    answer: str = Field(
        description="The answer to the user question, based on the context."
    )
    references: list[str] = Field(
        description="List of relevant excerpts from the retrieved context, copy and pasted exactly as they appear."
    )

class UploadResponse(BaseModel):
    message: str
    documents_indexed: int
    total_chunks: int
