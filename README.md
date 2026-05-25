<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenAI%20Compatible-412991?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/SBERT-orange?style=for-the-badge&logo=huggingface&logoColor=white"/>

<br/><br/>

# 🎯 AI-Driven Framework for Early Career Skill Gap Analysis and Recommendation

### *Upload your resume. Pick your dream role. Get your personalized 30-day roadmap.*

**A Final Year Project by Team [Your Team Name] — [Your College Name]**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge)](https://your-streamlit-link-here.streamlit.app)

</div>

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Module Breakdown](#-module-breakdown)
- [Local Setup](#-local-setup)
- [Environment Variables](#-environment-variables)
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
