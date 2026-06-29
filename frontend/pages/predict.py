"""
Single Prediction Page
"""

import streamlit as st
import requests
import json
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_URL = "http://localhost:8000/api/v1"

def get_molecule_name(smiles: str) -> str:
    """Get common name for a molecule if available"""
    common_names = {
        "Cc1ccc(-c2cc(C(F)(F)F)nn2-c2ccc(S(N)(=O)=O)cc2)cc1": "Celecoxib",
        "CS(=O)(=O)c1ccc(C2=C(C(=O)OC2)c3ccccc3)cc1": "Rofecoxib",
        "CC(C)Cc1ccc(C(C)C(=O)O)cc1": "Ibuprofen",
        "COc1ccc2cc([C@H](C)C(=O)O)ccc2c1": "Naproxen",
        "CC(=O)Oc1ccccc1C(=O)O": "Aspirin",
        "c1ccccc1": "Benzene",
        "Cc1ccccc1": "Toluene",
    }
    return common_names.get(smiles, None)

def render_molecule(smiles: str, size: tuple = (300, 300)):
    """Render a molecule from SMILES"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        from rdkit.Chem import AllChem
        AllChem.Compute2DCoords(mol)
        img = Draw.MolToImage(mol, size=size)
        return img
    except:
        return None

def render():
    """Render the single prediction page"""
    
    st.markdown("Enter a SMILES string to predict pIC50 and activity class")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        smiles_input = st.text_input(
            "SMILES String",
            value=st.session_state.get('current_smiles', ''),
            placeholder="Example: Cc1ccccc1",
            key="predict_smiles",
            label_visibility="collapsed"
        )
    
    with col2:
        include_explanation = st.checkbox("Include SHAP Explanation", value=False, key="predict_explain")
        predict_btn = st.button("Predict", type="primary", use_container_width=True)
    
    if smiles_input:
        mol = Chem.MolFromSmiles(smiles_input)
        if mol:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                img = render_molecule(smiles_input, size=(280, 280))
                if img:
                    st.image(img, caption="Molecule Structure", use_container_width=True)
            
            with col2:
                name = get_molecule_name(smiles_input)
                if name:
                    st.markdown(f"**Molecule Name:** {name}")
                
                st.markdown("**Molecular Properties:**")
                props = {
                    "Molecular Weight": f"{Descriptors.MolWt(mol):.2f} g/mol",
                    "LogP": f"{Descriptors.MolLogP(mol):.2f}",
                    "H-Bond Donors": Descriptors.NumHDonors(mol),
                    "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
                    "Rotatable Bonds": Descriptors.NumRotatableBonds(mol),
                    "Ring Count": Descriptors.RingCount(mol),
                }
                
                props_df = pd.DataFrame(list(props.items()), columns=["Property", "Value"])
                st.dataframe(props_df, hide_index=True, use_container_width=True)
        else:
            st.warning("Invalid SMILES string. Please check your input.")
    
    if predict_btn and smiles_input:
        with st.spinner("Making prediction..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={
                        "smiles": smiles_input,
                        "include_explanation": include_explanation
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    prediction = response.json()
                    st.session_state['current_smiles'] = smiles_input
                    
                    st.markdown("### Prediction Results")
                    qsar = prediction['qsar']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        <div class="prediction-card">
                            <div class="prediction-label">Predicted pIC50</div>
                            <div class="prediction-value">{:.3f}</div>
                        </div>
                        """.format(qsar['pIC50']), unsafe_allow_html=True)
                    
                    with col2:
                        activity_class = qsar['activity_class']
                        color_class = {
                            'Active': 'metric-active',
                            'Moderate': 'metric-moderate',
                            'Inactive': 'metric-inactive'
                        }.get(activity_class, '')
                        st.markdown("""
                        <div class="prediction-card">
                            <div class="prediction-label">Activity Class</div>
                            <div class="prediction-value {}">{}</div>
                        </div>
                        """.format(color_class, activity_class), unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div class="prediction-card">
                            <div class="prediction-label">Status</div>
                            <div style="font-size:1.1rem;font-weight:500;color:#1a73e8;">Prediction Complete</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if include_explanation and 'explanation' in prediction:
                        st.markdown("### Feature Importance (SHAP)")
                        for feat in prediction['explanation'].get('feature_importance', []):
                            st.progress(
                                min(1.0, abs(feat['shap_value']) / 2),
                                text="{}: {:.3f} (value: {:.2f})".format(
                                    feat['feature'],
                                    feat['shap_value'],
                                    feat['value']
                                )
                            )
                    
                    st.download_button(
                        label="Download Results (JSON)",
                        data=json.dumps(prediction, indent=2),
                        file_name="prediction_{}.json".format(smiles_input[:10]),
                        mime="application/json"
                    )
                    
                else:
                    st.error("Prediction failed: {}".format(response.text))
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure backend is running.")
            except Exception as e:
                st.error("Error: {}".format(str(e)))  