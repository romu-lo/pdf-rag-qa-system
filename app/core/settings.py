from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    search_type: str = "mmr"
    k: int = 5
    fetch_k: int = 20
    lambda_mult: float = 0.7

    chunk_size: int = 1024
    chunk_overlap: int = 256

    embedding_model: str = "text-embedding-3-small"

    llm_model: str = "gpt-5-nano"
    llm_temperature: float = 0.3
    llm_max_retries: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
