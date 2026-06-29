"""
QSAR Predictor - Main Streamlit App
"""

import streamlit as st

st.set_page_config(
    page_title="QSAR Predictor",
    page_icon=":microscope:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for better styling
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #5f6368;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Prediction card */
    .prediction-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 12px 0;
        border: 1px solid #e8eaed;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .prediction-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a73e8;
    }
    .prediction-label {
        font-size: 0.85rem;
        color: #5f6368;
    }
    
    /* Metric colors */
    .metric-active { color: #0d652d; font-weight: 600; }
    .metric-moderate { color: #e37400; font-weight: 600; }
    .metric-inactive { color: #d93025; font-weight: 600; }
    
    /* Footer removal */
    footer { visibility: hidden; }
    .stApp footer { display: none; }
    
    /* Tab styling - larger, colorful */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #f1f3f4;
        border-radius: 12px;
        padding: 6px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1.05rem;
        color: #5f6368;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(26, 115, 232, 0.3);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(26, 115, 232, 0.1);
    }
    .stTabs [aria-selected="true"]:hover {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
    }
    
    /* Remove sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Center content */
    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">QSAR Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predict pIC50 and activity class from molecular structure</div>', unsafe_allow_html=True)

# ============================================
# MAIN CONTENT - Tabs Only
# ============================================
from pages.predict import render as predict_render
from pages.batch_predict import render as batch_render
from pages.explain import render as explain_render
from pages.about_model import render as about_render

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Single Prediction",
    "Batch Upload",
    "Explanation",
    "About the Model"
])

with tab1:
    predict_render()

with tab2:
    batch_render()

with tab3:
    explain_render()

with tab4:
    about_render()  