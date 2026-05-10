import pandas as pd
import os
import shutil
import tempfile
import streamlit as st


def _normalize_skill_key(skill):
    """Normalize skill labels to make lookups resilient to case/spacing differences."""
    return " ".join(str(skill).strip().lower().split())

@st.cache_data(ttl=3600)
def load_skill_links(excel_path=os.path.join(os.path.dirname(__file__), "courses_recommendation.xlsx")):
    temp_path = None
    try:
        # Create a temp path
        fd, temp_path = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd) # Close it so PowerShell can write to it
        
        # Use PowerShell to copy the file - it bypasses some Windows locks that shutil can't
        copy_cmd = f'powershell -Command "Copy-Item \'{excel_path}\' \'{temp_path}\' -Force"'
        ret = os.system(copy_cmd)
        
        if ret != 0:
            # Fallback to shutil if powershell fails or isn't available
            shutil.copy2(excel_path, temp_path)
        
        # Load regular skills from the temp copy
        df = pd.read_excel(temp_path, sheet_name="Sheet1")
        skill_links = {}
        for skill in df["Missing_Skill"].dropna().unique():
            skill_key = _normalize_skill_key(skill)
            links = df[df["Missing_Skill"] == skill][["Platform", "Resource_Name", "Resource_URL", "Resource_Type"]].to_dict("records")
            skill_links[skill_key] = links
        
        # Load quiz links
        try:
            quiz_df = pd.read_excel(temp_path, sheet_name="quiz")
            quiz_links = {}
            for _, row in quiz_df.iterrows():
                skill = row["Required Skills"]
                link = row["Quiz link resource"]
                if pd.notna(skill) and pd.notna(link):
                    skill_key = _normalize_skill_key(skill)
                    if skill_key not in quiz_links:
                        quiz_links[skill_key] = []
                    quiz_links[skill_key].append({
                        "Platform": "Quiz/Assessment",
                        "Resource_Name": "Knowledge Check",
                        "Resource_URL": link,
                        "Resource_Type": "Quiz"
                    })
        except Exception:
            quiz_links = {}
            
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return {"study": {}, "quiz": {}}
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        
    return {"study": skill_links, "quiz": quiz_links}

def generate_learning_plan(missing_skills, skill_links_data):
    """Groups missing skills into a skill-wise structured 4-week progression."""
    study_links = skill_links_data.get("study", {})
    quiz_links = skill_links_data.get("quiz", {})
    
    skill_plans = {}
    
    for skill in missing_skills:
        skill_key = _normalize_skill_key(skill)
        week_plans = []
        for week_num in range(1, 5):
            week_resources = []
            week_quizzes = []
            
            # Study resources for this specific skill
            resources = study_links.get(skill_key, [])
            for res in resources:
                platform = str(res.get("Platform", "")).lower()
                
                # Filter by week focus for this skill
                should_add = False
                if week_num in [1, 2] and "youtube" in platform:
                    should_add = True
                elif week_num == 3 and "github" in platform:
                    should_add = True
                
                if should_add:
                    res_copy = res.copy()
                    res_copy['Skill'] = skill
                    week_resources.append(res_copy)
            
            # Quiz resources for this specific skill (Week 4 Focus)
            if week_num == 4:
                quizzes = quiz_links.get(skill_key, [])
                for q in quizzes:
                    q_copy = q.copy()
                    q_copy['Skill'] = skill
                    week_quizzes.append(q_copy)
            
            week_plans.append({
                "Week": week_num,
                "Resources": week_resources,
                "Quizzes": week_quizzes
            })
            
        skill_plans[skill] = week_plans
        
    return skill_plans


