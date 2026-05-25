<div align="center">

  # AI-Driven Framework for Early Career Skill Gap Analysis and Recommendation

### *Upload your resume. Pick your dream role. Get your personalized 30-day roadmap.*

**A Final Year Project**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20Here-FF4B4B?style=for-the-badge)](https://ai-skill-gap-analyzer-njnvh23mz9pmwsxh3rofuq.streamlit.app)

</div>

---
## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Module Breakdown](#-module-breakdown)
- [Team](#-team)

---

## 🧠 Overview

**AI-Driven Framework for Early Career Skill Gap Analysis and Recommendation** is a full-stack AI web application designed to help early-career job seekers understand exactly where they stand against industry role requirements — and what to do about it.

The user uploads their **resume (PDF or DOCX)**, selects a **target job role and department**, and the system:

1. Extracts skills from the resume using **LLM + SBERT semantic matching**
2. Compares them against a curated **roles dataset** with required skills
3. Identifies **matched and missing skills** with a % match score
4. Generates a **personalized 4-week learning roadmap** with YouTube, GitHub, and quiz resources
5. Suggests **alternative roles** in the same department where the user is a better fit
6. Uses AI to **enhance and rebuild the resume** as a downloadable `.docx` — ATS-optimized

> Built entirely on the Python standard ecosystem with no paid APIs required in local mode (uses Ollama + TinyLlama locally, or any OpenAI-compatible endpoint in production).

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 **Resume Parsing** | Extracts text from PDF (PyMuPDF) and DOCX files, preserving hyperlinks |
| 🤖 **AI Skill Extraction** | LLM-powered skill extraction from resume text, with regex fallback |
| 🔍 **Semantic Skill Matching** | SBERT (`all-MiniLM-L6-v2`) + alias dictionary for fuzzy skill matching |
| 📊 **Match Score Dashboard** | Visual % match with matched vs. missing skill cards |
| 🗺️ **30-Day Learning Roadmap** | Phase-wise plan: YouTube → GitHub Projects → Quiz/Assessment |
| 🏆 **Alternative Role Finder** | Scans all roles in the selected department for better-fit suggestions |
| ✨ **AI Resume Enhancer** | Injects missing keywords into resume, live preview + `.docx` download |
| 🎨 **Aurora UI Design** | Custom dark glassmorphism theme built with CSS injected via Streamlit |

---

## 🏗️ System Architecture

<img width="1960" height="1180" alt="image" src="https://github.com/user-attachments/assets/f6b54b33-a0e3-4833-b0fb-807c3f60676e" />

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit, Custom CSS (Aurora Glassmorphism Design System) |
| **AI / NLP** | OpenAI-compatible LLM (local: Ollama/TinyLlama, cloud: GPT-4o-mini or similar) |
| **Semantic Matching** | Sentence-BERT (`all-MiniLM-L6-v2`) via `sentence-transformers` |
| **PDF Parsing** | PyMuPDF (`fitz`) — text + hyperlink extraction |
| **DOCX Parsing & Generation** | `python-docx` |
| **Data** | `pandas`, `openpyxl` — roles CSV + Excel course recommendations |
| **Retry Logic** | `tenacity` — exponential backoff on LLM API calls |
| **Config / Secrets** | `python-dotenv` |
| **Deployment** | Streamlit Community Cloud |

---

## 📁 Module Breakdown

```
ai-skill-gap-analyzer/
│
├── app.py                      Main Streamlit app — UI, routing, tab logic
├── config.py                   LLM client factory (local Ollama ↔ cloud OpenAI)
├── skill_matcher.py            Core AI: skill extraction, match analysis,
│                               SBERT semantic matching, top role finder
├── section_extractor.py        LLM-based resume section parser
│                               (education, projects, experience)
├── skills_links.py             Excel loader + 4-week learning plan generator
├── resume_builder.py           AI resume enhancer + python-docx builder
├── style_utils.py              Aurora CSS design system injection
├── roles.csv                   Job roles database (department, role, skills)
├── courses_recommendation.xlsx Learning resource database
│                               Sheet1 — Missing_Skill → Platform, URL, Type
│                               quiz   — Skill → Quiz link
└── requirements.txt
```
**Key Design Decisions:**

**Dual-mode LLM** — `config.py` switches between local Ollama (free, no internet) and any OpenAI-compatible cloud API using environment variables. Zero code changes needed between environments.

**Two-pass skill matching** — Alias dictionary first (high precision for known equivalents like SQL/MySQL), then SBERT cosine similarity at 0.55 threshold (catches semantic variants). Dramatically reduces false negatives.

**Embedding cache** — `@st.cache_resource` on the SBERT model and `@st.cache_data` on individual skill embeddings. The 80MB model loads once per session; embeddings are never recomputed.

**Retry with backoff** — All LLM calls use `@retry(stop_after_attempt(2), wait=wait_exponential(...))` via `tenacity`. Handles transient API failures without crashing the UI.

**Robust JSON parsing** — LLM responses cleaned with `re.search(r'\{.*\}', content, re.DOTALL)` before `json.loads()`, with a markdown-strip fallback. Prevents crashes from verbose LLM outputs.

---

---
## 👥 Team

This project was built as a Final Year Project by a team of 3:

| Name | GitHub |
|---|---|
| **Ashika** | [@Ashi2806](https://github.com/Ashi2806) |
| **Bhuvanesh S** | [@Bhuvanesh1609](https://github.com/bhuvanesh1609) |
| **Anitta V** | [@Anitta10](https://github.com/Anitta10) |

---

## ⚠️ Note on Live Demo

Hosted on **Streamlit Community Cloud** free tier. The app may sleep after inactivity — click **"Yes, get this app back up!"** to wake it (~30 seconds). 

---
