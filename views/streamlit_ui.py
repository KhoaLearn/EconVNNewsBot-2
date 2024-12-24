import streamlit as st
import pandas as pd
from controller.question_controller import QuestionController
from controller.cot_controller import CoTController
from controller.rag_controller import RAGController 
from src.model import EmbeddingModel
from datetime import date, datetime

def inject_custom_css():
    st.markdown("""
    <style>
        body {
            font-family: 'Georgia', serif;
        }
        .custom-input {
            padding: 15px;
            font-size: 16px;
            border: 1px solid #007bff;
            border-radius: 25px;
            background-color: #f8f9fa;
            font-family: 'Georgia', serif;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .send-button {
            background-color: #007bff;
            border: none;
            color: white;
            padding: 12px 18px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        .send-button:hover {
            background-color: #0056b3;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize controllers and model
embedding_model = EmbeddingModel()
cot_controller = CoTController()
question_controller = QuestionController()
rag_controller = RAGController(question_controller=question_controller, embedding_model=embedding_model)  # Pass correct parameters

# Load categories from CSV
# def load_categories():
#     df = pd.read_csv('/Users/khoale/EconVNNewsBot-Pro/controller/categories.csv')
#     categories = df['category'].tolist()
#     categories.insert(0, "All")
#     return categories

# Load sources from CSV
# def load_sources():
#     df = pd.read_csv('/Users/khoale/EconVNNewsBot-Pro/controller/source.csv')
#     sources = df['source'].tolist()
#     sources.insert(0, "All")
#     return sources

if 'query_history' not in st.session_state:
    st.session_state['query_history'] = []

def add_query_to_history(query):
    """Add a query to the query history"""
    if query not in st.session_state['query_history']:
        st.session_state['query_history'].append(query)

def convert_string_to_date(date_str):
    """Convert a string 'yyyy-mm-dd' to a datetime.date object"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def display_query_ui():
    inject_custom_css()

    # Sidebar - Filter Options and Query History
    with st.sidebar:
        st.subheader("Query History")
        st.markdown("Below are your recent queries. Click to rerun them.")
        # Query History
        if st.session_state['query_history']:
            selected_history = st.selectbox("Previous Queries:", st.session_state['query_history'], key='history_select')
            st.session_state['user_query'] = selected_history

    # Initialize user_query in session state if it doesn't exist
    if 'user_query' not in st.session_state:
        st.session_state['user_query'] = ""

    # Handle displaying results from previous queries
    if 'generated_thoughts' in st.session_state:
        st.markdown('<h4 style="color: #1a7d3b;">Results:</h4>', unsafe_allow_html=True)
        for idx, thought in enumerate(st.session_state['generated_thoughts'], 1):
            st.markdown(f"{thought}")
            st.markdown(f"Searching for related documents for {idx}...")

            # Embed and query documents for each Thought
            try:
                results = question_controller.query_for_thought(thought, embedding_model, top_k=5)
                if results:
                    for doc in results:
                        st.markdown(f"- **Title**: {doc['metadata']['title']} \n **URL**: {doc['metadata']['url']}")
                else:
                    st.warning(f"No documents found for Thought {idx}.")
            except Exception as e:
                st.error(f"Error querying Thought {idx}: {e}")

    # Create two columns for input box and button
    col1, col2 = st.columns([5, 1])

    with col1:
        user_query = st.text_input(
            "", value=st.session_state['user_query'], key="user_query_input",
            placeholder="Enter your question...", label_visibility='collapsed'
        )

    with col2:
        send_button = st.button("⤴️", key='submit_button', help='Send Query')

    # Handle query when button is clicked
    if send_button and user_query:
        st.session_state['user_query'] = user_query
        add_query_to_history(user_query)

        try:
            # Call CoT to generate Thoughts
            st.info("Generating chain of thoughts (Chain-of-Thought)...")
            thoughts = cot_controller.generate_cot(user_query)

            if thoughts:
                results = []
                for idx, thought in enumerate(thoughts, start=1):
                    st.markdown(f"{thought}")

                    # Search for documents and refine Thought
                    st.info(f"Searching for related documents for Thought {idx}...")
                    try:
                        result = rag_controller.process_thought(query=user_query, thought=thought)
                        results.append(result)

                        # Display refined Thought
                        st.markdown(f"{result['refined_thought']}")
                        st.markdown("**Related Documents:**")
                        for doc in result['related_documents']:
                            st.markdown(f"- **Title**: {doc['title']}\n  **URL**: {doc['url']}")

                    except Exception as e:
                        st.error(f"Error querying Thought {idx}: {e}")

                # Save results to session
                st.session_state['results'] = results
            else:
                st.warning("Unable to generate chain of thoughts. Please try again.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
