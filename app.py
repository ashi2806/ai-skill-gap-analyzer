import warnings
import os
import logging
warnings.filterwarnings("ignore")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("streamlit").setLevel(logging.ERROR)

import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
from skill_matcher import ai_extract_skills, ai_analyze_match, ai_get_top_matches, ai_generate_project_ideas
from resume_builder import ai_enhance_resume_text, convert_text_to_docx
from dotenv import load_dotenv
load_dotenv()
from skills_links import load_skill_links, generate_learning_plan
from config import get_llm_client, get_llm_model

# Page config must be the first Streamlit command.
st.set_page_config(
    page_title="Early Career Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = get_llm_client()
model = get_llm_model()

from style_utils import inject_custom_css, render_header, skill_card

# Apply global styling
inject_custom_css()

# Load roles.csv
@st.cache_data(ttl=3600)
def load_roles():
    return pd.read_csv(os.path.join(BASE_DIR, "roles.csv"))

roles_df = load_roles()

# PDF text extraction
@st.cache_data
def extract_text_from_file(file_content, file_name):
    """Extract text from PDF OR DOCX, preserving hyperlinks where possible"""
    try:
        if file_name.endswith('.pdf'):
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                page_text = page.get_text()
                links = page.get_links()
                link_text = ""
                for link in links:
                    if 'uri' in link:
                        uri = link['uri']
                        if uri not in page_text:
                            link_text += f"\n {uri}"
                text += page_text + link_text + "\n"
            doc.close()
            return text
        
        elif file_name.endswith('.docx'):
            import io
            from docx import Document
            doc = Document(io.BytesIO(file_content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
            
    except Exception as e:
        st.error(f"❌ File Error: {str(e)}")
        
    return ""


# Custom Header
render_header("AI-Powered Early Career Skill Gap Analyzer", "Architecting your career path with precision AI analysis and high-fidelity roadmaps.")

st.sidebar.markdown(f"""
<div style="padding: 10px;">
    <h3 style="color: #fff; margin-bottom: 30px; font-size: 1rem; letter-spacing: 0.2em; font-weight: 800; opacity: 0.8;">WORKFLOW</h3>
    <div class="roadmap-step">
        <div class="step-num" style="background: var(--accent-indigo);">01</div>
        <div style="font-weight: 600; font-size: 0.95rem; opacity: 0.9;">Resume Input</div>
    </div>
    <div class="roadmap-step">
        <div class="step-num" style="background: var(--accent-emerald);">02</div>
        <div style="font-weight: 600; font-size: 0.95rem; opacity: 0.9;">Skill Analysis</div>
    </div>
    <div class="roadmap-step">
        <div class="step-num" style="background: #818CF8;">03</div>
        <div style="font-weight: 600; font-size: 0.95rem; opacity: 0.9;">30-Day Mastery</div>
    </div>
    <div class="roadmap-step">
        <div class="step-num" style="background: var(--accent-rose);">04</div>
        <div style="font-weight: 600; font-size: 0.95rem; opacity: 0.9;">Export ATS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# UI
uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

departments = sorted(roles_df["department"].dropna().unique())
selected_department = st.selectbox(
    "🏢 Select Department",
    ["Select a department"] + list(departments)
)
if selected_department != "Select a department":
    filtered_roles = roles_df[roles_df["department"] == selected_department]
else:
    filtered_roles = roles_df

roles_list = sorted(filtered_roles["role"].dropna().unique())
selected_role = st.selectbox(
    "💼 Target Role",
    ["Select a role"] + list(roles_list)
)

# Main analysis
if uploaded_file is not None and selected_role != "Select a role":
    with st.spinner("🔍 Analyzing your resume..."):
        # Extract text once (CACHED)
        file_bytes = uploaded_file.getvalue()
        resume_text = extract_text_from_file(file_bytes, uploaded_file.name)
        
        if not resume_text.strip():
            st.warning("⚠️ No text extracted from PDF.")
            st.stop()
        
        with st.status("🚀 **Initiating AI Analysis...**", expanded=True) as status:
            # Skill extraction (CACHED)
            st.write("📥 Reading resume talent profile...")
            resume_skills = ai_extract_skills(resume_text, selected_role)
            
            # Match analysis (CACHED)
            st.write("🤖 Aligning with market requirements...")
            role_row = roles_df[roles_df["role"] == selected_role].iloc[0]
            role_skills_str = str(role_row["skills"]) if pd.notna(role_row["skills"]) else ""
            analysis = ai_analyze_match(resume_text, selected_role, role_skills_str)
            
            st.write("✨ Finalizing architectural roadmap...")
            missing_skills = analysis.get("missing_skills", [])
            matched_skills = analysis.get("matched_skills", [])
            
            status.update(label="✅ **Analysis Complete!**", state="complete", expanded=False)
        
        st.balloons()
        st.toast("Analysis synchronized successfully!", icon="✨")

    st.markdown("---")
    
    # Organize content into clean Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Skill Analysis", "🚀 30-Day Plan", "🏆 Alternative Roles", "📄 Enhanced Resume"])

    with tab1:
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        
        col_match, col_miss = st.columns(2)
        
        with col_match:
            # st.success(f"✅ MATCHED SKILLS ({len(matched_skills)})")
            if matched_skills:
                skill_card("Matched Skills", matched_skills, is_matched=True)
            else:
                st.info("No matched skills found.")
                
        with col_miss:
            if missing_skills:
                # st.error(f"❌ MISSING SKILLS ({len(missing_skills)})")
                skill_card("Missing Skills", missing_skills, is_matched=False)
            else:
                st.success("✅ No missing skills found! You are a great match for this role.")

    with tab2:
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        if missing_skills:
            st.markdown("""
            <div class="glass-card animate-in" style="border-left: 4px solid var(--accent-cyan); padding: 20px;">
                <p style="margin:0; font-weight: 700; color: var(--accent-cyan); font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em;">🎯 Personalized Roadmap</p>
                <p style="margin:5px 0 0 0; font-size: 1rem; color: var(--text-muted);">We've engineered a high-impact curriculum to bridge your skill gaps in 4 weeks.</p>
            </div>
            """, unsafe_allow_html=True)
            
            skill_links = load_skill_links(os.path.join(BASE_DIR, "courses_recommendation.xlsx"))
            skill_plans = generate_learning_plan(missing_skills, skill_links)

            week_focuses = {
                1: "Phase 1: Fundamental Mastery (Week 1-2)",
                2: "Phase 1: Fundamental Mastery (Week 1-2)",
                3: "Phase 2: Build the Project (Week 3)",
                4: "Phase 3: Final Assessment (Week 4)"
            }

            for skill, weeks in skill_plans.items():
                st.markdown(f"### 🛡️ Skill Roadmap: {skill.title()}")
                
                # Consolidate Week 1 & 2 for UI
                w1_2_resources = weeks[0]["Resources"] + weeks[1]["Resources"]
                w3_item = weeks[2]
                w4_item = weeks[3]

                # Phase 1: Weeks 1-2 (YouTube)
                with st.expander(f"📍 {week_focuses[1]}", expanded=True):
                    st.markdown(f"#### 📺 YouTube Lessons")
                    if w1_2_resources:
                        # Deduplicate YouTube links (keep only unique URLs)
                        unique_youtube = {}
                        for res in w1_2_resources:
                            url = res.get('Resource_URL')
                            if url and url not in unique_youtube:
                                unique_youtube[url] = res
                        
                        # Show only the first unique YouTube link as per user request
                        first_res = list(unique_youtube.values())[0] if unique_youtube else None
                        if first_res:
                            st.markdown(f"  - 📺 [{first_res['Resource_Name']}]({first_res['Resource_URL']})")
                    else:
                        st.markdown(f"*(No specific YouTube lessons found, recommended search: [YouTube](https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial))*")

                # Phase 2: Week 3 (GitHub / Build)
                with st.expander(f"📍 {week_focuses[3]}", expanded=False):
                    st.markdown(f"#### 💻 GitHub Projects (Build the Project)")
                    if w3_item["Resources"]:
                        for res in w3_item["Resources"]:
                            st.markdown(f"  - 🐱 [{res['Resource_Name']}]({res['Resource_URL']})")
                    else:
                        st.markdown(f"*(No specific GitHub projects found)*")
                    
                    st.markdown("---")
                    st.markdown(f"#### 💡 Hands-on project ideas for {skill.title()}")
                    projects = ai_generate_project_ideas(skill)
                    for proj in projects:
                        st.markdown(f"- {proj}")

                # Phase 3: Week 4 (Quiz)
                with st.expander(f"📍 {week_focuses[4]}", expanded=False):
                    if w4_item.get("Quizzes"):
                        st.markdown(f"**🎯 Technical Interview Prep (Quiz)**")
                        for quiz in w4_item["Quizzes"]:
                            st.markdown(f"  - 📝 practice quiz for the '{skill}': [Start Assessment]({quiz['Resource_URL']})")
                    else:
                        st.markdown(f"**🎯 Technical Interview Prep** (LeetCode / HackerRank)")
                        st.markdown(f"*(Final review and preparation for {skill.title()})*")
                
                st.markdown("---")
            
            st.success("✅ **Ready to execute!** Start your mastery journey today! 🚀")
        else:
            st.balloons()
            st.success("Incredible! You matched all the required skills for this role. You are ready to apply!")

    with tab3:
        st.header("Alternative Career Paths")
        st.markdown("We scanned other roles in exactly the same department to see if your skills are a better fit elsewhere.")
        try:
            dept_roles_df = roles_df[roles_df["department"] == selected_department] 
            top_scores = ai_get_top_matches(resume_text, dept_roles_df)
            st.dataframe(top_scores, width='stretch', hide_index=True)
            st.bar_chart(top_scores.set_index("Role"))
        except Exception as e:
            st.error(f"⚠️ Top matches temporarily unavailable: {str(e)}")

    with tab4:
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card animate-in" style="padding: 30px; margin-bottom: 30px; border-left: 4px solid var(--accent-violet);">
            <h2 style="color: var(--accent-violet); font-size: 1.6rem; margin-top: 0;">✨ AI Optimization</h2>
            <p style="color: var(--text-muted); font-size: 1.1rem; line-height: 1.6;">Our engine surgically weaves target keywords into your resume, ensuring maximum ATS compatibility while preserving your unique professional voice.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate basic info for filename generation
        import re
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
        phone = re.search(r'(?<!\d)(?:\+?\d{1,3}[\s\-]?)?(?:[6-9]\d{9})(?!\d)', resume_text)
        lines = [l.strip() for l in resume_text.splitlines() if l.strip() and len(l.strip()) < 50]
        name = lines[0][:40] if lines else "Candidate"
        basic_info = {
            "name": name.title().strip(),
            "email": email.group(0) if email else "candidate@email.com",
            "phone": phone.group(0).strip() if phone else "+91-XXXXXXXXXX"
        }

        if "enhanced_text" not in st.session_state:
            st.session_state.enhanced_text = ""

        if st.button("✨ Generate Enhanced Resume Text", key="gen_btn"):
            with st.spinner("Injecting missing skills..."):
                try:
                    enhanced_text = ai_enhance_resume_text(resume_text, missing_skills)
                    st.session_state.enhanced_text = enhanced_text
                except Exception as e:
                    st.error(f"Failed to generate: {e}")
                
        if st.session_state.enhanced_text:
            st.success("✅ Enhancement Complete!")
            
            # --- NEW PREMIUM PREVIEW AREA ---
            st.markdown("### 👁️ Resume Preview")
            
            # Helper to style headers in preview
            def style_resume_for_preview(text):
                section_patterns = [
                    r'^(EDUCATION|EXPERIENCE|WORK\s+EXPERIENCE|PROJECTS|TECHNICAL\s+SKILLS|SKILLS|CERTIFICATIONS|ACHIEVEMENTS|LANGUAGES|SUMMARY|OBJECTIVE):?\s*$',
                    r'^[A-Z\s]{5,20}$'
                ]
                lines = text.splitlines()
                styled_html = ""
                for line in lines:
                    clean = line.strip()
                    if not clean:
                        styled_html += "<br>"
                        continue
                    
                    is_header = False
                    for pattern in section_patterns:
                        if re.match(pattern, clean, re.IGNORECASE) and len(clean) < 30:
                            is_header = True
                            break
                    
                    if is_header:
                        styled_html += f'<div style="font-weight: 700; font-size: 16px; margin-top: 15px; text-transform: uppercase; border-bottom: 2px solid #EEE; padding-bottom: 2px; margin-bottom: 8px;">{clean}</div>'
                    elif clean.startswith('•') or clean.startswith('-') or clean.startswith('*'):
                        styled_html += f'<div style="margin-left: 15px; margin-bottom: 4px;">• {clean.lstrip("•-* ")}</div>'
                    else:
                        styled_html += f'<div style="margin-bottom: 4px;">{clean}</div>'
                return styled_html

            with st.container():
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    background-color: var(--secondary-bg);
                    padding: 40px;
                    border-radius: 20px;
                    border: 1px solid var(--border-soft);
                ">
                    <div style="
                        background-color: white;
                        color: #111;
                        padding: 60px;
                        width: 100%;
                        max-width: 800px;
                        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                        border-radius: 4px;
                        font-family: 'Times New Roman', serif;
                        line-height: 1.6;
                        font-size: 14px;
                        white-space: normal;
                    ">
                        {style_resume_for_preview(st.session_state.enhanced_text)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
            # ------------------------
            
            enhanced_doc = convert_text_to_docx(st.session_state.enhanced_text)
            import tempfile
            tmp_enhanced = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            enhanced_doc.save(tmp_enhanced.name)
            tmp_enhanced.close()

            with open(tmp_enhanced.name, "rb") as f:
                # Specific requested format: 'Ashika's Imported Resume-hackerresume.pdf'
                # We will use the extracted name and original filename
                clean_name = basic_info['name'].replace('\n', '').strip()
                orig_filename = uploaded_file.name
                formatted_filename = f"{clean_name}'s Imported Resume-{orig_filename}.docx"
                
                st.download_button(
                    label="📥 Download Enhanced Resume (.docx)",
                    data=f.read(),
                    file_name=formatted_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    width='stretch'
                )
            import os
            os.unlink(tmp_enhanced.name)

else:
    # Empty state styling
    st.markdown("""
    <div class="glass-card animate-in" style="text-align: center; padding: 120px 40px; margin: 40px 0;">
        <div style="
            width: 100px; 
            height: 100px; 
            background: var(--accent-soft); 
            border-radius: 30px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin: 0 auto 40px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        ">
            <span style="font-size: 3rem;">⚡</span>
        </div>
        <h2 style="color: var(--text-main); font-size: 2.8rem; margin-top: 0; font-family: 'Outfit', sans-serif;">Unfold Your Potential</h2>
        <p style="color: var(--text-muted); font-size: 1.25rem; max-width: 600px; margin: 0 auto; line-height: 1.7; font-weight: 400;">
            Upload your professional resume to begin a deep-dive analysis. We'll identify your gaps and build a 30-day mastery curriculum tailored for your target role.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: small;'><em>AI-Powered Early Career Skill Gap Analyzer</em></div>", unsafe_allow_html=True)

