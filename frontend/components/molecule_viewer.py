"""
Molecule Visualization Component
"""

import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, AllChem, Descriptors
import pandas as pd

# Common molecule names for display
COMMON_NAMES = {
    "Cc1ccc(-c2cc(C(F)(F)F)nn2-c2ccc(S(N)(=O)=O)cc2)cc1": "Celecoxib",
    "CS(=O)(=O)c1ccc(C2=C(C(=O)OC2)c3ccccc3)cc1": "Rofecoxib",
    "CC(C)Cc1ccc(C(C)C(=O)O)cc1": "Ibuprofen",
    "COc1ccc2cc([C@H](C)C(=O)O)ccc2c1": "Naproxen",
    "CC(=O)Oc1ccccc1C(=O)O": "Aspirin",
    "c1ccccc1": "Benzene",
    "Cc1ccccc1": "Toluene",
    "CCO": "Ethanol",
}

def get_molecule_name(smiles: str) -> str:
    """
    Get common name for a molecule if available
    """
    if smiles in COMMON_NAMES:
        return COMMON_NAMES[smiles]
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
            if formula:
                return formula
    except:
        pass
    
    return None

def render_molecule(smiles: str, size: tuple = (300, 300)):
    """
    Render a molecule from SMILES
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        AllChem.Compute2DCoords(mol)
        img = Draw.MolToImage(mol, size=size)
        return img
        
    except Exception as e:
        st.error(f"Failed to render molecule: {str(e)}")
        return None

def display_molecule(smiles: str, caption: str = "Molecule Structure"):
    """
    Display molecule in Streamlit
    """
    img = render_molecule(smiles)
    if img:
        st.image(img, caption=caption, use_container_width=True)
    else:
        st.warning("Could not render molecule")

def get_molecular_descriptors(smiles: str) -> dict:
    """
    Get molecular descriptors as a dictionary
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    
    return {
        "MolWt": round(Descriptors.MolWt(mol), 2),
        "LogP": round(Descriptors.MolLogP(mol), 2),
        "NumHDonors": Descriptors.NumHDonors(mol),
        "NumHAcceptors": Descriptors.NumHAcceptors(mol),
        "TPSA": round(Descriptors.TPSA(mol), 2),
        "NumRotatableBonds": Descriptors.NumRotatableBonds(mol),
        "RingCount": Descriptors.RingCount(mol),
        "HeavyAtomCount": Descriptors.HeavyAtomCount(mol),
        "NumAromaticRings": Descriptors.NumAromaticRings(mol),
    }

def display_molecule_with_info(smiles: str):
    """
    Display molecule with its name and properties
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        st.warning("Invalid SMILES string")
        return None
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img = render_molecule(smiles, size=(280, 280))
        if img:
            st.image(img, caption="Molecule Structure", use_container_width=True)
    
    with col2:
        name = get_molecule_name(smiles)
        if name:
            st.markdown(f"**Molecule Name:** {name}")
        else:
            st.markdown("**Molecule:** Unknown")
        
        st.markdown("**Molecular Properties:**")
        props = {
            "Molecular Weight": f"{Descriptors.MolWt(mol):.2f} g/mol",
            "LogP": f"{Descriptors.MolLogP(mol):.2f}",
            "H-Bond Donors": Descriptors.NumHDonors(mol),
            "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
            "Rotatable Bonds": Descriptors.NumRotatableBonds(mol),
            "Ring Count": Descriptors.RingCount(mol),
            "Heavy Atoms": Descriptors.HeavyAtomCount(mol),
            "Aromatic Rings": Descriptors.NumAromaticRings(mol),
        }
        
        for key, value in props.items():
            st.markdown(f"**{key}:** {value}")
    
    return mol

def display_descriptor_table(smiles: str):
    """
    Display molecular descriptors in a formatted table
    """
    descriptors = get_molecular_descriptors(smiles)
    if descriptors is None:
        return
    
    df = pd.DataFrame(list(descriptors.items()), columns=["Descriptor", "Value"])
    st.dataframe(df, hide_index=True, use_container_width=True)   