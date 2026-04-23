import os
import streamlit as st

from llm_generator import generate_text_with_exception_handling
from api_client import metaphor_search_articles
from prompts import get_linkedin_prompt


def generate_linkedin_post(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language):
    """ Function to call upon LLM to get the work done. """

    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")

    # If keywords and content both are given.
    if serp_results:
        prompt = get_linkedin_prompt(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language, serp_results)
        linkedin_post = generate_text_with_exception_handling(prompt)
        return linkedin_post
