import os
from typing import Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core import LLMResponse, settings

load_dotenv()

def initialize_embedding_model(
    model: str = settings.embedding_model,
) -> OpenAIEmbeddings:
    """
    Initialize and return the Embeddings model.
    """
    return OpenAIEmbeddings(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

def initialize_llm(
    model: str = settings.llm_model,
    temperature: float = settings.llm_temperature,
    max_retries: int = settings.llm_max_retries,
) -> ChatOpenAI:
    """
    Initialize and return the LLM model.
    """
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_retries=max_retries,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    return llm.with_structured_output(LLMResponse, strict=True)

def generate_response(
    messages: list[Any],
    llm: ChatOpenAI,
) -> LLMResponse:
    """
    Generate a response from the LLM based on the given messages.
    """
    response = llm.invoke(messages)
    return response
