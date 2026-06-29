"""
About the Model Page
"""

import streamlit as st

def render():
    """Render the About the Model page"""
    
    with st.expander("What is QSAR?", expanded=True):
        st.markdown("""
        **QSAR** (Quantitative Structure-Activity Relationship) is a computational method that 
        relates the chemical structure of molecules to their biological activity.
        
        In this project, we use QSAR to predict how strongly a molecule binds to the COX-2 enzyme, 
        which is a target for anti-inflammatory drugs.
        """)
    
    with st.expander("How Does the Model Work?", expanded=True):
        st.markdown("""
        The model follows this process:
        
        1. **Input**: You provide a SMILES string (text representation of a molecule)
        2. **Feature Extraction**: RDKit calculates 8 molecular descriptors
        3. **Prediction**: XGBoost models predict pIC50 and activity class
        4. **Output**: You receive the predicted values with SHAP explanations
        
        The model was trained on experimental data from ChEMBL for COX-2 inhibitors.
        """)
    
    with st.expander("What are the 8 Molecular Descriptors?", expanded=True):
        st.markdown("""
        The model uses these 8 descriptors calculated by RDKit:
        
        | Descriptor | What it Measures |
        |-----------|------------------|
        | **MolWt** | Molecular weight (g/mol) |
        | **NumHDonors** | Number of hydrogen bond donors |
        | **NumHAcceptors** | Number of hydrogen bond acceptors |
        | **TPSA** | Topological polar surface area (A2) |
        | **NumRotatableBonds** | Number of rotatable bonds |
        | **RingCount** | Total number of rings |
        | **HeavyAtomCount** | Number of non-hydrogen atoms |
        | **NumAromaticRings** | Number of aromatic rings |
        
        These descriptors capture key physicochemical properties of molecules.
        """)
    
    with st.expander("How Well Does the Model Perform?", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Regression (pIC50 Prediction)**")
            st.metric("R2", "0.298", help="Coefficient of determination")
            st.metric("RMSE", "0.985", help="Root mean squared error")
            st.metric("MAE", "0.762", help="Mean absolute error")
            st.caption("XGBoost Regressor")
        
        with col2:
            st.markdown("**Classification (Activity Class)**")
            st.metric("AUC", "0.771", help="Area under ROC curve")
            st.metric("Accuracy", "75.8%", help="Correct predictions")
            st.metric("F1-Score", "0.530", help="Harmonic mean of precision and recall")
            st.caption("XGBoost Classifier")
        
        st.info("""
        **Interpretation:** For an academic QSAR project, these scores are reasonable. 
        The model captures meaningful structure-activity relationships, though industrial 
        models typically achieve higher performance with larger datasets and more features.
        """)
    
    with st.expander("What Does the Model Predict?", expanded=True):
        st.markdown("""
        The model predicts two things:
        
        **1. pIC50 (Predicted)**
        - Higher values = stronger binding = better inhibitor
        - Range: Typically 0-10, with higher being better
        
        | pIC50 Range | Interpretation |
        |-------------|----------------|
        | >= 7.0 | Active (strong inhibitor) |
        | 5.0 - 7.0 | Moderate |
        | < 5.0 | Inactive (weak inhibitor) |
        
        **2. Activity Class (Predicted)**
        - Active: Strong inhibitor (pIC50 >= 7.0)
        - Moderate: Moderate inhibitor (pIC50 5.0-7.0)  
        - Inactive: Weak inhibitor (pIC50 < 5.0)
        """)
    
    with st.expander("What Data Was Used for Training?", expanded=True):
        st.markdown("""
        **Data Source:** ChEMBL database
        
        **Target:** COX-2 (Cyclooxygenase-2) enzyme
        
        **Data Size:** 4,392 molecules after cleaning
        
        **Data Filtering:**
        - IC50 measurements only
        - Human enzyme data only
        - Valid pIC50 values only
        - Unique molecules only
        
        **Activity Distribution:**
        - Active: 1,264 molecules (28.8%)
        - Moderate: 2,492 molecules (56.7%)
        - Inactive: 636 molecules (14.5%)
        """)
    
    with st.expander("How to Use This Tool", expanded=True):
        st.markdown("""
        **Single Prediction**
        1. Enter a SMILES string in the input field
        2. Click "Predict"
        3. View results: pIC50, activity class, and SHAP explanation
        
        **Batch Prediction**
        1. Prepare a CSV file with a 'smiles' column
        2. Upload the file
        3. Download results with predictions for all molecules
        
        **Explanation**
        1. Enter a SMILES string
        2. Click "Explain"
        3. See how each descriptor contributed to the prediction
        
        **Input Format: SMILES**
        - Example: `Cc1ccccc1` (Toluene)
        - Valid SMILES strings only
        - No empty strings or invalid characters
        """)
    
    with st.expander("Limitations", expanded=True):
        st.warning("""
        **Important Limitations:**
        1. The model is trained on COX-2 data only
        2. Performance is moderate (R2 = 0.298)
        3. Predictions are computational, not experimental
        4. Results should be validated experimentally
        5. Not suitable for clinical or regulatory decisions
        """)
    
    with st.expander("References", expanded=False):
        st.markdown("""
        **Data Source:**
        - ChEMBL database: https://www.ebi.ac.uk/chembl/
        
        **Tools Used:**
        - RDKit: Cheminformatics toolkit
        - XGBoost: Gradient boosting library
        - SHAP: Model explainability
        - FastAPI: API framework
        - Streamlit: Web interface
        
        **Model Training:**
        - Python 3.10
        - Scikit-learn, Pandas, NumPy
        - 80/20 train/test split
        - 10-fold cross-validation
        """)  