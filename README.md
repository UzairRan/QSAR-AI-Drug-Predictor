[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)
[![RDKit](https://img.shields.io/badge/RDKit-2022.09.5-FF6F00.svg)](https://www.rdkit.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
[![Drug Discovery](https://img.shields.io/badge/Drug_Discovery-AI-8A2BE2.svg)](https://en.wikipedia.org/wiki/Drug_discovery)
[![Computational Chemistry](https://img.shields.io/badge/Computational_Chemistry-ML-FF1493.svg)](https://en.wikipedia.org/wiki/Computational_chemistry)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.7.6-FF6F00.svg)](https://xgboost.ai/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7.svg)](https://render.com/)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-Deployed-FF4B4B.svg)](https://streamlit.io/cloud)


## QSAR Prediction System using Machine Learning  

Predict molecular bioactivity from chemical structures using Machine Learning and Computational Chemistry.

- This project implements an end-to-end QSAR (Quantitative Structure–Activity Relationship) workflow that predicts the biological activity of molecules from their SMILES representation. 

- It combines Machine Learning, RDKit, FastAPI, Streamlit, and Docker to provide a complete prediction application from model training to deployment.


--------------------------------------------------------------------------

--------------------------------------------------------------------------


# Project Overview

The application predicts molecular bioactivity using two Machine Learning models.

**Regression Model**

- Predicts: pIC50 value of a molecule

**Classification Model**

Predicts whether a molecule is:

- Active
  
- Inactive

Users simply enter a SMILES string, and the application returns:

- Predicted pIC50
- Activity Classification
- SHAP Feature Explanation

  
# 📊 Dataset

Source: ChEMBL Database

Each molecule contains:

- SMILES representation
  
- Experimental pIC50 value

--------------------------------------------------------------------------

--------------------------------------------------------------------------

# What is QSAR?

- QSAR (Quantitative Structure-Activity Relationship) is a computational method that relates the chemical structure of molecules to their biological activity. 

- In this project, QSAR models are used to predict how strongly a molecule binds to the COX-2 enzyme, which is a target for anti-inflammatory drugs.


# Project Architecture

```mermaid
flowchart TD
    A["**Data Collection**"] --> B["**Data Preprocessing**"]
    B --> C["**Feature Engineering (RDKit)**"]
    C --> D["**Train/Test Split**"]
    D --> E["**Feature Scaling**"]
    E --> F["**Model Training**"]
    F --> G["**Model Evaluation**"]
    G --> H["**Best Model Selection**"]
    H --> I["**Model Serialization**"]
    I --> J["**FastAPI Backend**"]
    J --> K["**REST API Development**"]
    K --> L["**Streamlit Frontend**"]
    L --> M["**SHAP Explainability**"]
    M --> N["**Docker Containerization**"]
    N --> O["**Deployment**"]

    style A fill:#1a73e8,color:#fff,stroke:#0d47a1,stroke-width:2px
    style B fill:#1a73e8,color:#fff,stroke:#0d47a1,stroke-width:2px
    style C fill:#1a73e8,color:#fff,stroke:#0d47a1,stroke-width:2px
    style D fill:#1a73e8,color:#fff,stroke:#0d47a1,stroke-width:2px
    style E fill:#1a73e8,color:#fff,stroke:#0d47a1,stroke-width:2px
    style F fill:#fbbc04,color:#000,stroke:#f9ab00,stroke-width:2px
    style G fill:#fbbc04,color:#000,stroke:#f9ab00,stroke-width:2px
    style H fill:#fbbc04,color:#000,stroke:#f9ab00,stroke-width:2px
    style I fill:#fbbc04,color:#000,stroke:#f9ab00,stroke-width:2px
    style J fill:#34a853,color:#fff,stroke:#1e8e3e,stroke-width:2px
    style K fill:#34a853,color:#fff,stroke:#1e8e3e,stroke-width:2px
    style L fill:#ea4335,color:#fff,stroke:#c5221f,stroke-width:2px
    style M fill:#ea4335,color:#fff,stroke:#c5221f,stroke-width:2px
    style N fill:#8A2BE2,color:#fff,stroke:#6a1b9a,stroke-width:2px
    style O fill:#8A2BE2,color:#fff,stroke:#6a1b9a,stroke-width:2px
```


--------------------------------------------------------------------------

--------------------------------------------------------------------------

## 📊 Model Performance

### Data Overview

| Parameter | Value |
|-----------|-------|
| Data Source | ChEMBL Database |
| Target | COX-2 (Cyclooxygenase-2) |
| Total Molecules | 15,314 (raw) → 4,392 (cleaned) |
| Features | 8 RDKit Molecular Descriptors |
| Activity Classes | Active (28.8%), Moderate (56.7%), Inactive (14.5%) |

---

### Model Selection

After comparing multiple algorithms, **XGBoost** was selected for both regression and classification tasks based on performance metrics:

| Model Type | Algorithm | Metric | Value |
|------------|-----------|--------|-------|
| Regression (pIC50) | XGBoost Regressor | **R²** | **0.298** |
| | | RMSE | 0.985 |
| | | MAE | 0.762 |
| Classification | XGBoost Classifier | **AUC** | **0.771** |
| | | Accuracy | 75.8% |
| | | Precision | 0.678 |
| | | Recall | 0.435 |
| | | F1-Score | 0.530 |

---

### Descriptors Used

The model was trained on these 8 molecular descriptors:

| Descriptor | Description |
|------------|-------------|
| **MolWt** | Molecular weight (g/mol) |
| **NumHDonors** | Number of hydrogen bond donors |
| **NumHAcceptors** | Number of hydrogen bond acceptors |
| **TPSA** | Topological polar surface area (Å²) |
| **NumRotatableBonds** | Number of rotatable bonds |
| **RingCount** | Total number of rings |
| **HeavyAtomCount** | Number of non-hydrogen atoms |
| **NumAromaticRings** | Number of aromatic rings |

---

### Activity Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| **Active** (pIC50 ≥ 7.0) | 1,264 | 28.8% |
| **Moderate** (pIC50 5.0–7.0) | 2,492 | 56.7% |
| **Inactive** (pIC50 < 5.0) | 636 | 14.5% |

---

### Evaluation Metrics Summary

| Task | Best Model | Key Metric | Value |
|------|------------|------------|-------|
| **Regression** | XGBoost Regressor | R² | **0.298** |
| **Classification** | XGBoost Classifier | AUC | **0.771** |

  
