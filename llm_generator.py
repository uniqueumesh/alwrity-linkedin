import os
import streamlit as st
import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

GEMINI_MODEL_FALLBACK = (
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
)


def _is_retryable_gemini_error(err: Exception) -> bool:
    msg = str(err).lower()
    return any(
        token in msg
        for token in (
            "429",
            "quota",
            "rate limit",
            "rate-limit",
            "resource_exhausted",
            "too many requests",
        )
    )


def _on_gemini_retry_exhausted(retry_state):
    last_exc = None
    try:
        last_exc = retry_state.outcome.exception()
    except Exception:
        last_exc = None

    details = f"{last_exc}" if last_exc else "Unknown error."
    st.error(
        "❌ Unable to generate a LinkedIn post right now. "
        "All configured Gemini models were exhausted due to quota/rate limits.\n\n"
        f"Details: {details}"
    )
    return None


@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    reraise=False,
    retry_error_callback=_on_gemini_retry_exhausted,
)
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    last_retryable_error = None
    for model_name in GEMINI_MODEL_FALLBACK:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            convo = model.start_chat(history=[])
            convo.send_message(prompt)
            return convo.last.text
        except Exception as e:
            if _is_retryable_gemini_error(e):
                last_retryable_error = e
                continue
            raise

    if last_retryable_error is not None:
        raise last_retryable_error
    raise RuntimeError("All configured Gemini models failed.")
