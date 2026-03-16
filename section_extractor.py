import streamlit as st
import openai
import json
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import re

from config import get_llm_client, get_llm_model

@st.cache_data
@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=8))
def ai_extract_sections(resume_text):
    """AI extracts sections even from messy PDFs"""
    client = get_llm_client()
    model = get_llm_model()
    
    prompt = f"""Extract these sections from resume as VALID JSON ONLY:
{{
    "education": "all education text OR empty string",
    "projects": "all projects text OR empty string", 
    "experience": "all experience text OR empty string"
}}

Resume text:
{resume_text[:5000]}"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    # Clean and parse JSON response
    content = response.choices[0].message.content.strip()
    
    # Robustly find JSON structure
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
            
    # Final fallback attempt: strip markdown if regex failed
    content = re.sub(r'```json|```', '', content).strip()
    try:
        return json.loads(content)
    except:
        return {"education": "", "projects": "", "experience": ""}
