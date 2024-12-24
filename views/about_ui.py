import streamlit as st

# Function to display the "About" page
def display_about_ui():
    st.title("About EconVNNewsBot")

    st.header("Introduction")
    st.write("""
    EconVNNewsBot is an advanced system designed to provide efficient and accurate retrieval and analysis of Vietnamese economic news.
    """)

    st.header("System Workflow")
    # st.image("docs/EconVNNewsBot.png", caption="System Workflow of EconVNNewsBot")

    st.write("""
    The workflow involves key processes like data crawling, embedding, retrieval-augmented generation (RAG), and refined answering.
    """)

    st.header("Key Features")
    st.write("""
    - Advanced question-answering system tailored for Vietnamese economic news.
    - Supports retrieval-augmented generation to provide contextual and accurate responses.
    - User-friendly interface with seamless query handling.
    """)

    st.header("Contact Information")
    st.write("""
    For any questions or suggestions, please contact us at:
    - **Email**: khoale.aius@gmail.com.vn
    - **Phone**: +84 903 696 581
    """)
