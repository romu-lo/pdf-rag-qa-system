import streamlit as st
from api_requests import ask_question


def _is_odd(index : int) -> bool:
    return index % 2 != 0

def _ai_message(message:str):
    with st.chat_message("ai"):
        st.markdown(message)

def _user_message(message:str):
    with st.chat_message("human"):
        st.markdown(message)

def _build_chat_history():
    for index, message in enumerate(st.session_state.chat_history):
        if _is_odd(index):
            _ai_message(message)

        else:
            _user_message(message)

def clear_chat_history():
    st.session_state.chat_history = []

def chat_box():
    """
    Display chat messages and handle user input.
    """
    _ai_message(
        "How can I help you? Don't forget to upload documents to provide context."
    )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    else:
        _build_chat_history()


def answer_question(user_question: str) -> dict:
    """
    Call POST /question sending a question and getting an answer.
    """
    _user_message(user_question)

    with st.spinner("Thinking..."):
        ai_answer = ask_question(user_question)
    _ai_message(ai_answer['answer'])

    st.session_state.chat_history.append(user_question)
    st.session_state.chat_history.append(ai_answer['answer'])