import streamlit as st
from openai import OpenAI
import json
import os
import re
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd 
import ast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
roles_df = pd.read_csv(os.path.join(BASE_DIR, "roles.csv"))

from config import get_llm_client, get_llm_model




def fallback_skills(text, role_name):
    # Convert resume text to lowercase
    text_lower = text.lower()
    
    # Get skills for this role from CSV
    role_row = roles_df[roles_df['role'] == role_name]
    if role_row.empty:
        return []  # No role found
    
    role_skills = role_row.iloc[0]['skills'].split(',')  # Assuming skills are comma-separated
    
    # Match skills against resume text
    found = []
    for skill in role_skills:
        pattern = r"\b" + re.escape(skill.strip().lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill.strip())

    
    return found[:8]


from sentence_transformers import SentenceTransformer, util
import torch

# Load SBERT model (cached)
@st.cache_resource
def load_sbert():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def get_cached_embedding(_model, text):
    """Cache individual skill embeddings to avoid redundant CPU/GPU cycles."""
    return _model.encode(text, convert_to_tensor=True)

SKILL_ALIASES = {
    "sql": ["mysql", "postgresql", "oracle", "sql server", "sqlite", "mariadb"],
    "machine learning": ["ml", "deep learning", "dl", "neural networks", "scikit-learn"],
    "artificial intelligence": ["ai", "machine learning", "nlp", "computer vision"],
    "cloud": ["aws", "azure", "gcp", "cloud computing"],
    "frontend": ["html", "css", "javascript", "react", "angular", "vue"],
    "backend": ["python", "node", "java", "php", "go", "sql"],
}

def get_semantic_match(target_skill, resume_skills, model, threshold=0.55):
    """
    Checks if target_skill exists in resume_skills using 
    combined semantic similarity + high-confidence aliases.
    """
    if not resume_skills:
        return False
        
    t_lower = target_skill.lower()
    
    # Pass 1: Simple Alias Match (High Precision)
    # If the target is "SQL", and resume has "MySQL"...
    if t_lower in SKILL_ALIASES:
        for r_skill in resume_skills:
            if r_skill.lower() in SKILL_ALIASES[t_lower]:
                return True

    # Pass 2: Semantic Similarity (General Case)
    skill_embedding = get_cached_embedding(model, target_skill)
    # Note: resume_skills is a list, so we encode it together which is already efficient
    # but we can't easily cache the list encoding without extra logic. 
    # For now, we'll keep the list encoding but cache the target.
    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(skill_embedding, resume_embeddings)
    max_score = torch.max(cosine_scores).item()
    
    return max_score >= threshold

@st.cache_data
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def ai_extract_skills(resume_text, selected_role):
    """AI extracts skills - BROADER EXTRACTION"""
    try:
        client = get_llm_client()
        model = get_llm_model()
        
        prompt = f"""Extract ALL technical skills and tools from this resume as a Python list.
Focus on skills relevant to the role of a '{selected_role}'.
Include everything: languages, frameworks, databases, cloud, libraries.
Format: ['Skill1', 'Skill2', ...]
Resume: {resume_text[:4000]}""" 
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            timeout=30.0,
            max_tokens=400
        )
        
        skills_str = response.choices[0].message.content.strip()
        
        # Robustly extract the list using regex
        list_match = re.search(r'\[.*\]', skills_str, re.DOTALL)
        if list_match:
            try:
                skills = ast.literal_eval(list_match.group(0))
            except:
                skills = [s.strip().strip("'\"") for s in list_match.group(0)[1:-1].split(',') if s.strip()]
        else:
            # Fallback to comma split if no brackets found
            skills_str = re.sub(r'```[a-zA-Z]*|```', '', skills_str).strip()
            skills = [s.strip() for s in skills_str.split(',') if s.strip()]
            
        return [s.strip().title() for s in skills if s.strip()]
        
    except Exception as e:
        return fallback_skills(resume_text, selected_role)

@st.cache_data
@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=8))
def ai_analyze_match(resume_text, role_name, role_skills_str):
    """SBERT + Regex Double-Pass match analysis - MAXIMUM ACCURACY"""
    try:
        # 1. Get ALL skills from resume
        resume_skills = ai_extract_skills(resume_text, role_name)
        resume_lower = resume_text.lower()
        
        # 2. Get target skills for the role
        target_skills = [s.strip() for s in role_skills_str.split(',') if s.strip()]
        
        # 3. Load SBERT
        model = load_sbert()
        
        matched_skills = []
        missing_skills = []
        
        for target in target_skills:
            target_clean = target.strip()
            if not target_clean: continue
            
            # PASS 1: Semantic Match (SBERT)
            if get_semantic_match(target_clean, resume_skills, model, threshold=0.55):
                matched_skills.append(target_clean.title())
                continue
            
            # PASS 2: Literal Match (Regex on raw text)
            # This handles cases where AI extraction might have missed an exact keyword
            pattern = r"\b" + re.escape(target_clean.lower()).replace(r"\ ", r"[ \-]?") + r"\b"
            if re.search(pattern, resume_lower):
                matched_skills.append(target_clean.title())
            else:
                missing_skills.append(target_clean.title())

        return {
            "matched_skills": list(set(matched_skills)),
            "missing_skills": list(set(missing_skills))
        }
    except Exception as e:
        print("Accuracy match failed, using basic fallback:", e)
        # Final Keyword Fallback
        role_skills = [s.strip() for s in role_skills_str.split(',') if s.strip()]
        resume_lower = resume_text.lower()
        matched, missing = [], []
        for s in role_skills:
            pattern = r"\b" + re.escape(s.lower()) + r"\b"
            if re.search(pattern, resume_lower):
                matched.append(s.title())
            else:
                missing.append(s.title())
        return {"matched_skills": matched, "missing_skills": missing}

@st.cache_data
@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=8))
def ai_generate_project_ideas(skill_name):
    """AI generates 2-3 mini-project ideas for a specific skill"""
    try:
        client = get_llm_client()
        model = get_llm_model()
        prompt = f"""Generate 2 specific mini-project ideas for a beginner to learn {skill_name}.
Keep each description under 20 words.
Format as a Python list: ["Project 1: ...", "Project 2: ..."]"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=15.0,
            max_tokens=150
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r'```python|```', '', content).strip()
        return ast.literal_eval(content)[:2]
    except Exception:
        return [f"Build a small tool using {skill_name}", f"Create a GitHub repo for {skill_name} exercises"]

@st.cache_data
def ai_get_top_matches(resume_text, roles_df):
    """
    Optimized: Extracts resume skills once and performs local semantic 
    matching against all roles to avoid redundant LLM/SBERT calls.
    """
    if roles_df.empty:
        return pd.DataFrame(columns=["Role", "Match %"])

    # 1. Extract resume skills ONCE
    # We use a placeholder role just for the extraction context
    resume_skills = ai_extract_skills(resume_text, roles_df.iloc[0]["role"])
    resume_lower = resume_text.lower()
    
    # 2. Pre-load SBERT and encode resume skills once
    model = load_sbert()
    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True) if resume_skills else None
    
    scores = []
    for _, row in roles_df.iterrows():
        role_name = row["role"]
        role_skills_str = str(row["skills"]) if pd.notna(row["skills"]) else ""
        target_skills = [s.strip() for s in role_skills_str.split(',') if s.strip()]
        
        if not target_skills:
            scores.append({"Role": role_name, "Match %": 0.0})
            continue

        # 3. FAST match analysis (Local only)
        matched_count = 0
        for target in target_skills:
            target_clean = target.strip()
            # Pass 1: Semantic Match (Local tensor comparison)
            if resume_embeddings is not None:
                target_emb = get_cached_embedding(model, target_clean)
                cosine_scores = util.cos_sim(target_emb, resume_embeddings)
                if torch.max(cosine_scores).item() >= 0.55:
                    matched_count += 1
                    continue
            
            # Pass 2: Regex Fallback
            pattern = r"\b" + re.escape(target_clean.lower()).replace(r"\ ", r"[ \-]?") + r"\b"
            if re.search(pattern, resume_lower):
                matched_count += 1

        raw_score = (matched_count / len(target_skills)) * 100.0
        score = float(int(raw_score * 10)) / 10.0
        scores.append({"Role": role_name, "Match %": score})

    return pd.DataFrame(scores).sort_values("Match %", ascending=False).head(5)


