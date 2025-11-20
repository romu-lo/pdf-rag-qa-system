from typing import Any

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores.base import VectorStoreRetriever

from source.core import LLMResponse, constants
from source.infrastructure import (
    generate_response,
    initialize_llm,
    initialize_retriever,
    retrieve_documents,
)


def _retrieve_context(
    question: str,
    retriever: VectorStoreRetriever,
) -> str:
    """
    Retrieve context from the vector database based on the question.
    """
    docs = retrieve_documents(retriever, question)
    return "\n\n".join([doc.page_content for doc in docs])

def _build_message_history(
    question: str,
    context: str,
    history: list|None = None,
) -> list[SystemMessage | AIMessage | HumanMessage]:
    """
    Build message history for the chat.
    """
    context_prompt_template = PromptTemplate.from_template(
        constants.CONTEXT_PROMPT_TEMPLATE,
    )

    context_prompt = context_prompt_template.format(context=context)

    system_prompt = SystemMessage(
            content=constants.SYSTEM_PROMPT
    )

    chat_messages = [system_prompt]

    if history:
        chat_messages.extend(history)

    chat_messages.extend([
        AIMessage(content=context_prompt),
        HumanMessage(content=question)
    ])

    return chat_messages

def answer_question(
    question: str,
    history: list[SystemMessage | AIMessage | HumanMessage] | None = None,
) -> LLMResponse:
    """
    Answer a question based on the provided context using the LLM model.
    """
    retriever = initialize_retriever()
    context = _retrieve_context(question, retriever)
    message_history = _build_message_history(question, context, history)
    llm = initialize_llm()
    return generate_response(message_history, llm)
