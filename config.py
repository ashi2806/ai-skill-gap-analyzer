import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_llm_client():
    """
    Centralized function to get an OpenAI-compatible client.
    Priority:
    1. Environment variables (OPENAI_API_KEY, LLM_BASE_URL)
    2. Default to local Ollama (http://localhost:11434/v1)
    """
    api_key = os.getenv("OPENAI_API_KEY", "ollama")
    base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    
    return OpenAI(
        base_url=base_url,
        api_key=api_key
    )

def get_llm_model():
    """Returns the configured model name, defaulting to tinyllama."""
    return os.getenv("LLM_MODEL", "tinyllama")
