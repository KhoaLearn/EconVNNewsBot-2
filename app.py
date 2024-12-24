import streamlit as st
from views.streamlit_ui import display_query_ui  # For the search page
from views.about_ui import display_about_ui      # For the about page

# Custom CSS for improved UI and consistent fonts
def inject_custom_css():
    st.markdown("""
    <style>
        /* Customize sidebar background color and font */
        body {
            font-family: 'Georgia', serif; /* Set default font to Georgia */
        }
        .stSidebar {
            background-color: #ccd9e6;
            font-size: 18px;
            color: #1a7d3b;
        }
        /* Customize buttons for better appearance */
        .stButton > button {
            background-color: #4a8c6c;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Georgia', serif;  /* Keep font consistent */
        }
        /* Customize the header section */
        .header {
            font-family: 'Georgia', serif;
            color: #1a7d3b;
            text-align: center;
            padding-bottom: 12px;
        }
        /* Customize headers and text */
        h1, h2, h3, h4, h5, h6, p {
            font-family: 'Georgia', serif;
        }
    </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    layout="centered", 
    page_title="EconVNNewsBot",
    page_icon="📄"
)

# Sidebar menu for navigation
def sidebar_menu():
    st.sidebar.title("EconVNNewsBot")
    st.sidebar.subheader("Navigation")
    return st.sidebar.selectbox("Select Page", ["Search", "About"])

# Welcome message (optional)
# def display_welcome_message():
    # st.markdown('<h3 style="color: #1a7d3b;" class="header">EconVNNewsBot: A Retrieval-Based Reasoning System for Answering Questions on Vietnamese Economic News</h3>', unsafe_allow_html=True)
    # st.markdown('<p style="font-size: 18px;">This system provides accurate answers, based on context, from an extensive database of Vietnamese economic news, supported by RAT reasoning and reputable references.</p>', unsafe_allow_html=True)

# Main function of the application
def main():
    # Inject custom CSS
    inject_custom_css()

    # Display the welcome message when the app starts (optional)
    # display_welcome_message()
    
    # Sidebar navigation
    selected_page = sidebar_menu()

    # Navigate between pages based on user selection
    if selected_page == "Search":
        display_query_ui()  
    elif selected_page == "About":
        display_about_ui()  

# Main entry point of the application
if __name__ == "__main__":
    main()
