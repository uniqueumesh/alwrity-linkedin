import time #Iwish
import os
import json
import requests
import streamlit as st
from exa_py import Exa
import clipboard

from llm_generator import generate_text_with_exception_handling


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI LinkedIn Post Writer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Global CSS styles for UI improvements
    st.markdown("""
        <style>
            body {
                background-color: #f0f2f6;
            }
            div.stButton > button:first-child {
                background-color: #007bff;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            div.stButton > button:first-child:hover {
                background-color: #0056b3;
            }
            .reportview-container .markdown-text-container {
                font-family: 'Helvetica Neue', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hide top header and footer for a cleaner UI
    hide_elements = """
        <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_elements, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI LinkedIn Post Generator")
    st.write("Leverage AI to craft high-quality LinkedIn posts tailored to your audience.")

    # Initialize session state for generated post
    if "linkedin_post" not in st.session_state:
        st.session_state.linkedin_post = ""

    # Input section with an informative expander
    with st.expander("💡 **PRO TIP** - Follow these instructions for better results.", expanded=True):
        st.write("1. Use specific keywords related to your topic.\n"
                 "2. Choose a post type that aligns with your message.\n"
                 "3. Select an appropriate language and length for your audience.")

        # Input fields for the LinkedIn post generator
        input_blog_keywords = st.text_input(
            '🔑 **Enter main keywords for your post**', 
            placeholder='e.g., Marketing Trends, Leadership Tips...', 
            help="Use relevant keywords that define the topic of your LinkedIn post."
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            input_linkedin_type = st.selectbox('📝 **Post Type**', (
                'General', 'How-to Guides', 'Polls', 'Listicles', 
                'Reality Check Posts', 'Job Posts', 'FAQs', 'Checklists/Cheat Sheets'), 
                index=0, help="Choose the format that suits the message you want to deliver.")
        with col2:
            input_linkedin_length = st.selectbox('📏 **Post Length**', 
                ('1000 words', 'Long Form', 'Short Form'), index=0, 
                help="Decide the length of your post based on its complexity and target audience.")
        with col3:
            input_linkedin_language = st.selectbox('🌐 **Choose Language**', 
                ('English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish'), 
                index=0, help="Pick the language that resonates best with your audience.")

    # Button to generate the LinkedIn post
    if st.button('🚀 **Generate LinkedIn Post**'):
        if not input_blog_keywords:
            st.error('🚫 **Please provide keywords to generate a LinkedIn post!**')
        else:
            with st.spinner('🤖 Crafting your LinkedIn post...'):
                # Progress bar for user feedback
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(percent_complete + 1)

                # Generate the LinkedIn post
                st.session_state.linkedin_post = generate_linkedin_post(
                    input_blog_keywords, input_linkedin_type, 
                    input_linkedin_length, input_linkedin_language)

            # Check if post generation succeeded
            if st.session_state.linkedin_post is not None:
                # Post generation success message
                st.success('🎉 **Your LinkedIn post is ready!**')
                st.subheader('📄 **LinkedIn Post Preview**')
                st.write(st.session_state.linkedin_post)

                # Copy to Clipboard button with success feedback
                if st.button('📋 Copy to Clipboard'):
                    clipboard.copy(st.session_state.linkedin_post)
                    st.success("✅ LinkedIn post copied to clipboard!")
            else:
                st.error('❌ **Failed to generate LinkedIn post. Please check your inputs or try again later.**')


def generate_linkedin_post(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language):
    """ Function to call upon LLM to get the work done. """

    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")

    # If keywords and content both are given.
    if serp_results:
        from prompts import get_linkedin_prompt
        prompt = get_linkedin_prompt(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language, serp_results)
        linkedin_post = generate_text_with_exception_handling(prompt)
        return linkedin_post


# Metaphor search function
def metaphor_search_articles(query):
    EXA_API_KEY = os.getenv('EXA_API_KEY')
    if not EXA_API_KEY:
        raise ValueError("EXA_API_KEY environment variable not set!")

    exa = Exa(EXA_API_KEY)

    try:
        search_response = exa.search_and_contents(
            query,
            type="auto",
            num_results=5,
            highlights={"max_characters": 1000},
        )
        return search_response.results
    except Exception as err:
        st.error(f"Failed in exa.search_and_contents: {err}")
        return None


if __name__ == "__main__":
    main()
