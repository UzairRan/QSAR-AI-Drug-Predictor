"""
SHAP Explanation Page
"""

import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/api/v1"

def render():
    """Render the SHAP explanation page"""
    
    st.markdown("Understand why the model made its prediction using SHAP values")
    
    st.info(
        "SHAP (SHapley Additive exPlanations) shows how each molecular descriptor "
        "contributed to the predicted pIC50 value. Positive values increase the prediction, "
        "negative values decrease it."
    )
    
    smiles_input = st.text_input(
        "SMILES String",
        placeholder="Example: Cc1ccccc1",
        key="explain_smiles"
    )
    
    if st.button("Explain", type="primary"):
        if not smiles_input:
            st.warning("Please enter a SMILES string")
        else:
            with st.spinner("Generating explanation..."):
                try:
                    response = requests.post(
                        f"{API_URL}/explain",
                        json={"smiles": smiles_input},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        explanation = response.json()
                        
                        if 'error' in explanation:
                            st.error(explanation['error'])
                        else:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("""
                                <div class="prediction-card">
                                    <div class="prediction-label">Base Value</div>
                                    <div class="prediction-value">{:.3f}</div>
                                    <div style="font-size:0.8rem;color:#5f6368;margin-top:4px;">
                                        Expected pIC50 without features
                                    </div>
                                </div>
                                """.format(explanation.get('base_value', 0)), unsafe_allow_html=True)
                            
                            with col2:
                                pred_val = explanation.get('prediction', 0)
                                st.markdown("""
                                <div class="prediction-card">
                                    <div class="prediction-label">Predicted pIC50</div>
                                    <div class="prediction-value">{:.3f}</div>
                                    <div style="font-size:0.8rem;color:#5f6368;margin-top:4px;">
                                        Actual prediction including feature effects
                                    </div>
                                </div>
                                """.format(pred_val), unsafe_allow_html=True)
                            
                            st.markdown("### Feature Contributions")
                            
                            features = explanation.get('feature_importance', [])
                            if features:
                                for feat in features:
                                    norm_val = min(1.0, abs(feat['shap_value']) / 2)
                                    color = "#1a73e8" if feat['shap_value'] > 0 else "#d93025"
                                    direction = "increases" if feat['shap_value'] > 0 else "decreases"
                                    
                                    st.markdown(f"""
                                    <div style="margin-bottom:12px;">
                                        <div style="display:flex;justify-content:space-between;font-size:0.9rem;margin-bottom:2px;">
                                            <span style="font-weight:500;">{feat['feature']}</span>
                                            <span style="color:{color};">
                                                {feat['shap_value']:+.3f} ({direction})
                                            </span>
                                        </div>
                                        <div style="background:#e8eaed;border-radius:4px;height:8px;overflow:hidden;">
                                            <div style="background:{color};width:{norm_val*100:.0f}%;height:100%;border-radius:4px;"></div>
                                        </div>
                                        <div style="font-size:0.75rem;color:#5f6368;margin-top:2px;">
                                            Feature value: {feat['value']:.2f}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            with st.expander("Raw SHAP Data"):
                                st.json(explanation)
                            
                            st.download_button(
                                label="Download Explanation (JSON)",
                                data=json.dumps(explanation, indent=2),
                                file_name="shap_explanation_{}.json".format(smiles_input[:10]),
                                mime="application/json"
                            )
                            
                    else:
                        st.error("Explanation failed: {}".format(response.text))
                        
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure backend is running.")
                except Exception as e:
                    st.error("Error: {}".format(str(e)))  