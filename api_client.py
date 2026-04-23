import os
import streamlit as st
from exa_py import Exa


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