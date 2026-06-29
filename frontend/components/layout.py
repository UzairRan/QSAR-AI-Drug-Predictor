"""
Layout Components for Streamlit
"""

import streamlit as st

def set_page_config():
    """Set page configuration for Streamlit"""
    st.set_page_config(
        page_title="QSAR Predictor",
        page_icon=":microscope:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        /* Main header */
        .main-header {
            font-size: 2.2rem;
            font-weight: 600;
            color: #1a73e8;
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        .sub-header {
            font-size: 1rem;
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
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: #f1f3f4;
            border-radius: 8px;
            padding: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 8px 20px;
            font-weight: 500;
            color: #5f6368;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            color: #1a73e8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Button styling */
        .stButton button {
            background-color: #1a73e8;
            color: white;
            border-radius: 8px;
            font-weight: 500;
            border: none;
            padding: 8px 24px;
        }
        .stButton button:hover {
            background-color: #1557b0;
            color: white;
        }
        
        /* Metric styling */
        [data-testid="stMetric"] {
            background: #f8f9fa;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #e8eaed;
        }
        [data-testid="stMetric"] label {
            font-size: 0.85rem;
            color: #5f6368;
        }
        [data-testid="stMetric"] div {
            font-weight: 600;
        }
        
        /* Input styling */
        .stTextInput input {
            border-radius: 8px;
            border: 1px solid #dadce0;
        }
        .stTextInput input:focus {
            border-color: #1a73e8;
            box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar information"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">About</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-text">
        This tool predicts binding affinity and activity class for COX-2 inhibitors using machine learning models trained on experimental bioactivity data.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">How to Use</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-text">
        1. Enter a SMILES string in the input field<br>
        2. Click Predict to see results<br>
        3. Upload CSV for batch predictions<br>
        4. Use Explain tab for SHAP analysis
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">Model Performance</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Regression", "R² = 0.298", help="XGBoost Regressor")
        with col2:
            st.metric("Classification", "AUC = 0.771", help="XGBoost Classifier")
        
        st.markdown('<div class="sidebar-title">Input Format</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-text">
        <strong>SMILES</strong> (Simplified Molecular Input Line Entry System)<br>
        Example: <code>Cc1ccccc1</code> for Toluene
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">Output</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-text">
        • Predicted pIC50 value<br>
        • Activity class (Active / Moderate / Inactive)<br>
        • SHAP feature importance<br>
        • Molecular descriptors
        </div>
        """, unsafe_allow_html=True)

def display_footer():
    """Display footer"""
    # Footer removed as requested

def create_sidebar_metrics():
    """Create sidebar metrics for model performance"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Model Performance</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Regression", "R² = 0.298", help="XGBoost Regressor")
        with col2:
            st.metric("Classification", "AUC = 0.771", help="XGBoost Classifier")  