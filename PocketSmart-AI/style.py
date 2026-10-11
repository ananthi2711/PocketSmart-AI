"""
PocketSmart AI - Styling Module
Injects a modern, dark 'glow' dashboard theme with emerald/cyan gradient accents,
glowing metric cards, sleek buttons, and responsive layouts.
"""

import streamlit as st


def apply_custom_styles():
    """Injects custom CSS to style Streamlit into a modern glow dashboard."""
    glow_css = """
    <style>
    /* =====================================================================
       GLOBAL THEME & TYPOGRAPHY
       ===================================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Main background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #111827 0%, #0B0F19 100%) !important;
        color: #F3F4F6 !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #F9FAFB !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Gradient header text */
    .glow-header {
        background: linear-gradient(135deg, #10B981 0%, #06B6D4 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        display: inline-block;
        filter: drop-shadow(0 0 18px rgba(16, 185, 129, 0.35));
    }

    .glow-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.8rem;
    }

    /* =====================================================================
       SIDEBAR STYLING
       ===================================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #070B14 100%) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.15) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #E2E8F0 !important;
    }

    /* =====================================================================
       METRIC CARDS & CONTAINERS WITH GLOW
       ===================================================================== */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35), 0 0 15px rgba(16, 185, 129, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(12px);
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(16, 185, 129, 0.55);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 25px rgba(16, 185, 129, 0.25);
    }

    .metric-card-title {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }

    .metric-card-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-card-caption {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 0.3rem;
    }

    /* Glow Container */
    .glow-box,
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 24, 39, 0.65) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), 0 0 12px rgba(16, 185, 129, 0.08) !important;
    }

    /* Badges */
    .glow-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
    }

    .badge-live {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }

    .badge-demo {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }

    /* =====================================================================
       STREAMLIT TABS STYLING
       ===================================================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0 20px;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 41, 59, 0.8);
        color: #E2E8F0;
        border-color: rgba(16, 185, 129, 0.3);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(6, 182, 212, 0.18) 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.5) !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.25) !important;
    }

    /* =====================================================================
       BUTTONS WITH GRADIENTS & HOVER EFFECTS
       ===================================================================== */
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Secondary buttons (Download, Clear, Sample) */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* =====================================================================
       INPUT FIELDS & TEXTAREAS
       ===================================================================== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
    }

    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stTextArea label,
    .stSelectbox label,
    .stFileUploader label {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] section {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px dashed rgba(16, 185, 129, 0.4) !important;
        border-radius: 14px !important;
    }

    /* Alert / Callout Boxes */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }
    </style>
    """
    st.markdown(glow_css, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, caption: str = "", border_color: str = "#10B981"):
    """Renders a custom HTML metric card with glow and hover animation."""
    html_code = f"""
    <div class="metric-card" style="border-color: {border_color}40;">
        <div class="metric-card-title">{title}</div>
        <div class="metric-card-value" style="color: {border_color};">{value}</div>
        {f'<div class="metric-card-caption">{caption}</div>' if caption else ''}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
