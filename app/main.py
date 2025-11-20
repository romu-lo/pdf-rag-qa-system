import streamlit as st
from chat import chat_box, answer_question, clear_chat_history
from api_requests import upload_documents, health_check, clear_documents


def show_sidebar():
    with st.sidebar:
        st.title('Challenge Tractian - AI Engineer')
        st.subheader('Developped by Rômulo Mincache')
        st.markdown(
            """
            This application allows you to upload PDF documents,
            index their contents, and interactively ask questions
            based on the indexed information using a chatbot interface.

            It does not uses conversation memory, so each question is answered
            independently based on the uploaded documents.
            """
        )
        st.divider()
        if st.button("Clear Chat", icon="🧹", on_click=clear_chat_history):
            st.success("Chat history cleared.")
        if st.button("Clear Documents", icon="🗑️", on_click=clear_documents):
            st.success("All indexed documents have been cleared.")

def app():
    st.set_page_config(page_title="Chatbot - Challenge Tractian", page_icon='image.png')
    show_sidebar()

    if health_check() != 200:
        st.error("Error 404: API is offline. \nPlease start the API server and try again.")
        return

    user_question = st.chat_input(
        "Ask a question",
        accept_file="multiple",
        file_type=["pdf"],
    )
    with st.container():
        chat_box()
        if user_question and user_question.files:
            with st.spinner("Uploading files..."):
                upload_response = upload_documents(user_question.files)
            st.success(f"Uploaded {upload_response['documents_indexed']} document(s) with a total of {upload_response['total_chunks']} chunks indexed.")

        if user_question and user_question.text and user_question != "":
            answer_question(user_question.text)


if __name__ == "__main__":
    app()
