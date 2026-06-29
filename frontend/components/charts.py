"""
Chart Components for Streamlit - QSAR Only
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_feature_importance_chart(features: list, values: list, title: str = "Feature Importance"):
    """
    Create a horizontal bar chart for feature importance
    """
    if not features or not values:
        return None
    
    # Sort by absolute value
    sorted_data = sorted(zip(features, values), key=lambda x: abs(x[1]), reverse=True)
    features_sorted, values_sorted = zip(*sorted_data) if sorted_data else ([], [])
    
    # Create colors based on positive/negative
    colors = ['#1a73e8' if v >= 0 else '#d93025' for v in values_sorted]
    
    fig = go.Figure(data=go.Bar(
        x=values_sorted,
        y=features_sorted,
        orientation='h',
        marker_color=colors,
        text=[f"{v:+.3f}" for v in values_sorted],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>SHAP Value: %{x:+.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        title=title,
        title_font_size=16,
        title_font_color="#1a73e8",
        xaxis_title="SHAP Value",
        xaxis_title_font_color="#5f6368",
        yaxis_title="Feature",
        yaxis_title_font_color="#5f6368",
        margin=dict(l=20, r=40, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#3c4043"),
        xaxis=dict(
            showgrid=True,
            gridcolor='#e8eaed',
            zeroline=True,
            zerolinecolor='#dadce0'
        ),
        yaxis=dict(
            showgrid=False
        )
    )
    
    return fig

def create_activity_distribution_chart(activity_counts: dict):
    """
    Create a pie chart for activity class distribution
    """
    if not activity_counts:
        return None
    
    labels = list(activity_counts.keys())
    values = list(activity_counts.values())
    colors = ['#0d652d', '#e37400', '#d93025']
    
    fig = go.Figure(data=go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='inside',
        hole=0.4,
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        title="Activity Distribution",
        title_font_size=14,
        title_font_color="#1a73e8",
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        font=dict(color="#3c4043")
    )
    
    return fig

def create_descriptor_table(descriptors: dict):
    """
    Create a formatted table of molecular descriptors
    """
    if not descriptors:
        return None
    
    df = pd.DataFrame({
        'Descriptor': list(descriptors.keys()),
        'Value': list(descriptors.values())
    })
    
    df['Value'] = df['Value'].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else str(x))
    
    return df

def display_prediction_summary(qsar_prediction: dict):
    """
    Display prediction results in a formatted summary
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background:#f8f9fa;padding:16px;border-radius:8px;border-left:4px solid #1a73e8;">
            <div style="font-size:0.8rem;color:#5f6368;">Predicted pIC50</div>
            <div style="font-size:1.8rem;font-weight:600;color:#1a73e8;">{:.3f}</div>
        </div>
        """.format(qsar_prediction.get('pIC50', 0)), unsafe_allow_html=True)
    
    with col2:
        activity = qsar_prediction.get('activity_class', 'Unknown')
        color = {
            'Active': '#0d652d',
            'Moderate': '#e37400',
            'Inactive': '#d93025'
        }.get(activity, '#5f6368')
        
        st.markdown("""
        <div style="background:#f8f9fa;padding:16px;border-radius:8px;border-left:4px solid {color};">
            <div style="font-size:0.8rem;color:#5f6368;">Activity Class</div>
            <div style="font-size:1.8rem;font-weight:600;color:{color};">{activity}</div>
        </div>
        """.format(color=color, activity=activity), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background:#f8f9fa;padding:16px;border-radius:8px;border-left:4px solid #1a73e8;">
            <div style="font-size:0.8rem;color:#5f6368;">Status</div>
            <div style="font-size:1.2rem;font-weight:500;color:#1a73e8;">Prediction Complete</div>
        </div>
        """, unsafe_allow_html=True)  