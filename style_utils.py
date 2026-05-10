import streamlit as st

def inject_custom_css():
    """Injects the Aurora Design System - High Fidelity, Premium, State-of-the-Art."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    :root {
        --aurora-bg: #030712;
        --accent-indigo: #6366f1;
        --accent-cyan: #22d3ee;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
        --glass-white: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-pure: #ffffff;
        --text-dim: #94a3b8;
        --neon-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }

    /* Aurora Background Layer */
    .stApp {
        background: 
            radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 100% 100%, rgba(34, 211, 238, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.08) 0%, transparent 65%),
            var(--aurora-bg);
        color: var(--text-pure);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://grainy-gradients.vercel.app/noise.svg');
        opacity: 0.04;
        pointer-events: none;
        z-index: 10;
        filter: contrast(150%) brightness(150%);
    }

    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes glow {
        0% { filter: drop-shadow(0 0 5px rgba(99, 102, 241, 0.2)); }
        50% { filter: drop-shadow(0 0 25px rgba(99, 102, 241, 0.5)); }
        100% { filter: drop-shadow(0 0 5px rgba(99, 102, 241, 0.2)); }
    }

    .animate-float { animation: float 6s ease-in-out infinite; }
    .animate-glow { animation: glow 4s infinite alternate; }
    .animate-in { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both; }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(135deg, #fff 30%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.04em !important;
        font-weight: 800 !important;
    }

    /* High-Impact Header */
    .header-wrapper {
        padding: 6rem 2rem;
        background: radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 5rem;
        text-align: center;
        border-radius: 0 0 50px 50px;
    }

    .main-title {
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.2));
    }

    .subtitle {
        color: var(--text-dim);
        font-size: 1.4rem;
        max-width: 800px;
        margin: 0 auto;
        font-weight: 300;
        letter-spacing: 0.01em;
        line-height: 1.6;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(3, 7, 18, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }

    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.02);
        padding: 8px;
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        gap: 10px;
        margin-bottom: 4rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 14px;
        padding: 12px 28px !important;
        color: var(--text-dim) !important;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-indigo) !important;
        color: white !important;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }

    /* Aurora Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 28px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }

    .glass-card::after {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(99, 102, 241, 0.03) 0%, transparent 70%);
        pointer-events: none;
    }

    .glass-card:hover {
        transform: translateY(-5px) scale(1.005);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
    }

    /* Neon Badges */
    .badge {
        padding: 10px 20px;
        border-radius: 14px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 6px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        text-transform: none;
        letter-spacing: 0;
    }

    .badge-match {
        background: rgba(16, 185, 129, 0.08);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
    }

    .badge-miss {
        background: rgba(244, 63, 94, 0.08);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.2);
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.1);
    }

    .badge:hover {
        transform: translateY(-2px) scale(1.05);
        border-color: currentColor;
    }

    /* Buttons - The Aurora Pulse */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-indigo) 0%, #4f46e5 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.8rem 2.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        color: white !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2) !important;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4) !important;
        filter: brightness(1.1);
    }

    /* Roadmap UI */
    .roadmap-step {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
        padding: 16px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }

    .roadmap-step:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: var(--glass-border);
    }

    .step-num {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        font-weight: 800;
        font-size: 0.9rem;
        color: white;
    }

    /* Custom File Uploader */
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(255, 255, 255, 0.01) !important;
        border: 2px dashed rgba(99, 102, 241, 0.15) !important;
        border-radius: 24px !important;
        transition: all 0.3s ease !important;
        padding: 40px !important;
    }

    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--accent-indigo) !important;
        background: rgba(99, 102, 241, 0.03) !important;
    }

    /* Select Inputs */
    div[data-baseweb="select"] {
        background: var(--glass-bg) !important;
        border-radius: 16px !important;
        border: 1px solid var(--glass-border) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { 
        background: rgba(255, 255, 255, 0.1); 
        border-radius: 20px;
        border: 3px solid #030712;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-indigo); }

    /* Hide Elements */
    #MainMenu, footer { visibility: hidden; }

    </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle):
    st.markdown(f"""
    <div class="header-wrapper animate-in">
        <h1 class="main-title">{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def skill_card(title, skills, is_matched=True):
    badge_class = "badge-match" if is_matched else "badge-miss"
    color_hex = "#34d399" if is_matched else "#fb7185"
    icon = "✅" if is_matched else "❌"
    
    skills_html = "".join([f'<span class="badge {badge_class}">{s}</span>' for s in skills])
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="padding: 2.5rem;">
        <div style="display: flex; align-items: center; margin-bottom: 2rem; gap: 20px;">
            <div style="
                background: rgba({ '52, 211, 153' if is_matched else '251, 113, 133'}, 0.08); 
                padding: 12px; border-radius: 16px;
                border: 1px solid rgba({ '52, 211, 153' if is_matched else '251, 113, 133'}, 0.2);
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 0 15px rgba({ '52, 211, 153' if is_matched else '251, 113, 133'}, 0.1);
            ">
                <span style="font-size: 1.3rem;">{icon}</span>
            </div>
            <h3 style="margin: 0; color: #fff; font-size: 1.15rem; text-transform: uppercase; letter-spacing: 0.2em; font-weight: 700; opacity: 0.9;">
                {title}
            </h3>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            {skills_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
