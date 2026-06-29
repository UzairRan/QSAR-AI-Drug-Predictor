## 📁 **Updated `pages/batch_predict.py`**

"""
Batch Prediction Page
"""

import streamlit as st 
import pandas as pd
import requests
import json
from rdkit import Chem

# API_URL = "http://localhost:8000/api/v1"
API_URL = "https://qsar-ai-drug-predictor.onrender.com/api/v1" 

def render():
    """Render the batch prediction page"""
    
    st.markdown("Upload a CSV file with multiple SMILES strings for bulk prediction")
    
    with st.expander("CSV Format Requirements"):
        st.markdown("""
        Your CSV file must contain a column named **smiles** with one SMILES string per row.
        
        **Example CSV content:**
        ```
        smiles
        Cc1ccccc1
        CC(C)Cc1ccc(C(C)C(=O)O)cc1
        COc1ccc2cc([C@H](C)C(=O)O)ccc2c1
        ```
        
        **Optional columns:** You can include additional columns (e.g., name, id) which will be preserved in the output.
        """)
        
        example_df = pd.DataFrame({
            'smiles': [
                'Cc1ccc(-c2cc(C(F)(F)F)nn2-c2ccc(S(N)(=O)=O)cc2)cc1',
                'CC(C)Cc1ccc(C(C)C(=O)O)cc1',
                'COc1ccc2cc([C@H](C)C(=O)O)ccc2c1',
                'CC(=O)Oc1ccccc1C(=O)O',
                'c1ccccc1'
            ],
            'name': ['Celecoxib', 'Ibuprofen', 'Naproxen', 'Aspirin', 'Benzene']
        })
        csv_data = example_df.to_csv(index=False)
        st.download_button(
            label="Download Example CSV",
            data=csv_data,
            file_name="example_batch.csv",
            mime="text/csv"
        )
    
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=['csv'],
        help="CSV must contain a 'smiles' column"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("**File Preview:**")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption("Total molecules: {}".format(len(df)))
            
            if 'smiles' not in df.columns:
                st.error("CSV must contain a 'smiles' column")
                return
            
            valid_count = 0
            invalid_count = 0
            valid_smiles_list = []
            for smiles in df['smiles'].dropna():
                try:
                    if Chem.MolFromSmiles(str(smiles)):
                        valid_count += 1
                        valid_smiles_list.append(str(smiles))
                    else:
                        invalid_count += 1
                except:
                    invalid_count += 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valid SMILES", valid_count)
            with col2:
                st.metric("Invalid SMILES", invalid_count, delta_color="off" if invalid_count == 0 else "inverse")
            
            if invalid_count > 0:
                st.warning("Some SMILES strings appear invalid. Please check your input.")
            
            if st.button("Predict All", type="primary", use_container_width=True):
                if valid_count == 0:
                    st.error("No valid SMILES found. Please check your input file.")
                    return
                
                with st.spinner("Processing {} molecules...".format(valid_count)):
                    try:
                        payload = {
                            "smiles_list": valid_smiles_list,
                            "include_explanation": False
                        }
                        
                        response = requests.post(
                            f"{API_URL}/predict/batch",
                            json=payload,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            results = response.json()
                            
                            st.success("Prediction completed for {} molecules".format(results['successful']))
                            
                            if results['successful'] > 0:
                                results_data = []
                                for r in results['results']:
                                    results_data.append({
                                        'smiles': r['smiles'],
                                        'pIC50': r['qsar']['pIC50'],
                                        'activity_class': r['qsar']['activity_class']
                                    })
                                
                                results_df = pd.DataFrame(results_data)
                                st.dataframe(results_df, use_container_width=True)
                                
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="Download Results CSV",
                                    data=csv,
                                    file_name="batch_predictions.csv",
                                    mime="text/csv"
                                )
                            
                            if results['failed'] > 0:
                                st.warning("Failed predictions: {}".format(results['failed']))
                                for error in results['errors']:
                                    st.error("Row {}: {} - {}".format(
                                        error['index'],
                                        error['smiles'][:50] + '...' if len(error['smiles']) > 50 else error['smiles'],
                                        error['error']
                                    ))
                                    
                        else:
                            st.error("Batch prediction failed: {}".format(response.text))
                            
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to API. Make sure backend is running.")
                    except Exception as e:
                        st.error("Error: {}".format(str(e)))
                        
        except Exception as e:
            st.error("Error reading CSV file: {}".format(str(e)))
