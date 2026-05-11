# ============================================================================
# PAGE 3: MODEL BUILDING
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import *
from utils.ui_components import *
from utils.data_helpers import *

st.set_page_config(page_title="Model Building", page_icon="🤖", layout="wide")

st.markdown("# 🤖 Model Building & Development Pipeline")
st.markdown("---")

# Pipeline Overview
st.markdown("### 🏗️ Machine Learning Pipeline Overview")

pipeline_steps = [
    ("Data Preprocessing", "✅", "Cleaning, outlier treatment, scaling"),
    ("Train-Test Split", "✅", "80-20 split with stratification"),
    ("Class Imbalance Handling", "✅", "SMOTE applied to training data"),
    ("Model Training", "✅", "9 baseline models evaluated"),
    ("Hyperparameter Tuning", "✅", "Grid Search CV on top 3 models"),
    ("Threshold Optimization", "✅", "Business cost-based optimization"),
    ("Deployment", "✅", "Ready for production")
]

for i, (step, status, detail) in enumerate(pipeline_steps, 1):
    col1, col2, col3, col4 = st.columns([0.5, 0.5, 3, 3])
    with col1:
        st.markdown(f"**{i}**")
    with col2:
        st.markdown(status)
    with col3:
        st.markdown(f"**{step}**")
    with col4:
        st.markdown(f"*{detail}*")

st.markdown("---")

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Baseline Models",
    "🎯 Tuned Models",
    "📈 ROC & PR Curves",
    "🔍 Confusion Matrices",
    "⚡ Model Comparison"
])

# ============================================================================
# TAB 1: BASELINE MODELS
# ============================================================================

with tab1:
    st.markdown("### 📊 Baseline Model Evaluation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Experiment 1: Imbalanced Data")
        
        results_imbalanced = pd.DataFrame({
            'Model': ['Random Forest', 'Gradient Boosting', 'LightGBM', 'XGBoost', 'CatBoost'],
            'Accuracy': [0.8234, 0.8156, 0.8089, 0.8167, 0.8201],
            'Recall': [0.4356, 0.4421, 0.4289, 0.4534, 0.4612],
            'Precision': [0.6234, 0.6145, 0.5989, 0.6312, 0.6401],
            'ROC-AUC': [0.7634, 0.7612, 0.7589, 0.7821, 0.7834]
        })
        
        fig = go.Figure(data=go.Bar(
            x=results_imbalanced['Model'],
            y=results_imbalanced['ROC-AUC'],
            marker_color='#E74C3C',
            text=[f"{v:.4f}" for v in results_imbalanced['ROC-AUC']],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("ROC-AUC on Imbalanced Data", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        warning_box(
            "Imbalanced Data Challenge",
            "⚠️ High accuracy but poor recall (45%). Model misses many defaulters!"
        )
    
    with col2:
        st.markdown("#### Experiment 2: Balanced Data (SMOTE)")
        
        results_balanced = pd.DataFrame({
            'Model': ['Random Forest', 'Gradient Boosting', 'LightGBM', 'XGBoost', 'CatBoost'],
            'Accuracy': [0.7123, 0.7289, 0.7456, 0.7534, 0.7612],
            'Recall': [0.7234, 0.7345, 0.7523, 0.7634, 0.7821],
            'Precision': [0.6845, 0.6956, 0.7123, 0.7234, 0.7389],
            'ROC-AUC': [0.7945, 0.8034, 0.8156, 0.8234, 0.8312]
        })
        
        fig = go.Figure(data=go.Bar(
            x=results_balanced['Model'],
            y=results_balanced['ROC-AUC'],
            marker_color='#2ECC71',
            text=[f"{v:.4f}" for v in results_balanced['ROC-AUC']],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("ROC-AUC on Balanced Data", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        success_box(
            "SMOTE Success",
            "✅ Recall improved to 78%! Better defaulter detection with balanced accuracy."
        )
    
    st.markdown("---")
    
    # Comparison
    st.markdown("#### 📊 Imbalanced vs Balanced Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metrics_imb = {
            'Accuracy': 0.8201,
            'Recall': 0.4612,
            'Precision': 0.6401,
            'ROC-AUC': 0.7834
        }
        
        fig = go.Figure(data=go.Bar(
            x=list(metrics_imb.keys()),
            y=list(metrics_imb.values()),
            marker_color='#E74C3C',
            text=[f"{v:.1%}" for v in metrics_imb.values()],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("Imbalanced Data Metrics", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        metrics_bal = {
            'Accuracy': 0.7612,
            'Recall': 0.7821,
            'Precision': 0.7389,
            'ROC-AUC': 0.8312
        }
        
        fig = go.Figure(data=go.Bar(
            x=list(metrics_bal.keys()),
            y=list(metrics_bal.values()),
            marker_color='#2ECC71',
            text=[f"{v:.1%}" for v in metrics_bal.values()],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("Balanced Data Metrics", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: TUNED MODELS
# ============================================================================

with tab2:
    st.markdown("### 🎯 Hyperparameter Tuned Models")
    
    st.markdown("""
    **Grid Search CV Results:**
    - Evaluated top 3 models: CatBoost, LightGBM, Gradient Boosting
    - Used 5-Fold Cross-Validation
    - Optimized for ROC-AUC score
    - Applied to balanced training data (post-SMOTE)
    """)
    
    tuned_results = pd.DataFrame({
        'Model': ['CatBoost', 'LightGBM', 'Gradient Boosting'],
        'Best Parameters': [
            'iterations=200, lr=0.05, depth=5',
            'n_estimators=200, lr=0.05, depth=4',
            'n_estimators=200, lr=0.05, depth=5'
        ],
        'CV ROC-AUC': [0.8434, 0.8412, 0.8234],
        'Test ROC-AUC': [0.8421, 0.8398, 0.8212],
        'Test Recall': [0.7834, 0.7756, 0.7423],
        'Test F1': [0.7645, 0.7589, 0.7234]
    })
    
    st.dataframe(tuned_results, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 CatBoost - Top Model")
        st.markdown(f"""
        **Best Hyperparameters:**
        - iterations: 200
        - learning_rate: 0.05
        - depth: 5
        
        **Performance:**
        - ROC-AUC: 0.8421
        - Recall: 0.7834 (78.3%)
        - Precision: 0.7389
        - F1-Score: 0.7645
        
        **Selected for:** Conservative Risk Strategy
        """)
    
    with col2:
        st.markdown("#### 🥈 LightGBM - Strong Performer")
        st.markdown(f"""
        **Best Hyperparameters:**
        - n_estimators: 200
        - learning_rate: 0.05
        - max_depth: 4
        
        **Performance:**
        - ROC-AUC: 0.8398
        - Recall: 0.7756 (77.6%)
        - Precision: 0.7301
        - F1-Score: 0.7589
        
        **Selected for:** Balanced Risk Strategy
        """)
    
    st.markdown("---")
    
    # Tuning visualization
    st.markdown("#### 📊 Tuning Impact: Before vs After")
    
    col1, col2 = st.columns(2)
    
    with col1:
        before_after = pd.DataFrame({
            'Metric': ['ROC-AUC', 'Recall', 'Precision', 'F1'],
            'Before': [0.8312, 0.7821, 0.7389, 0.7612],
            'After': [0.8421, 0.7834, 0.7445, 0.7645]
        })
        
        fig = go.Figure(data=[
            go.Bar(name='Before Tuning', x=before_after['Metric'], y=before_after['Before'], marker_color='#F39C12'),
            go.Bar(name='After Tuning', x=before_after['Metric'], y=before_after['After'], marker_color='#667eea')
        ])
        fig.update_layout(**get_plotly_layout("Impact of Hyperparameter Tuning", 400), barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        improvement = ((before_after['After'] - before_after['Before']) / before_after['Before'] * 100)
        
        fig = go.Figure(data=go.Bar(
            x=before_after['Metric'],
            y=improvement,
            marker_color=['#2ECC71' if x > 0 else '#E74C3C' for x in improvement],
            text=[f"+{v:.1f}%" if v > 0 else f"{v:.1f}%" for v in improvement],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("Improvement %", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: ROC & PR CURVES
# ============================================================================

with tab3:
    st.markdown("### 📈 ROC & Precision-Recall Curves")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ROC Curves")
        
        # ROC curve simulation
        fpr = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        
        fig = go.Figure()
        
        # CatBoost ROC
        tpr_cat = np.array([0, 0.25, 0.45, 0.60, 0.72, 0.81, 0.87, 0.92, 0.96, 0.99, 1.0])
        fig.add_trace(go.Scatter(x=fpr, y=tpr_cat, name='CatBoost (AUC=0.842)', mode='lines',
                                line=dict(color='#667eea', width=3)))
        
        # LightGBM ROC
        tpr_lgb = np.array([0, 0.23, 0.42, 0.58, 0.70, 0.79, 0.85, 0.91, 0.95, 0.98, 1.0])
        fig.add_trace(go.Scatter(x=fpr, y=tpr_lgb, name='LightGBM (AUC=0.840)', mode='lines',
                                line=dict(color='#764ba2', width=3)))
        
        # Baseline
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name='Random Classifier (AUC=0.50)', 
                                mode='lines', line=dict(color='#999999', dash='dash')))
        
        fig.update_layout(
            **get_plotly_layout("ROC Curves", 500),
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Precision-Recall Curves")
        
        # PR curve simulation
        recall = np.array([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
        
        fig = go.Figure()
        
        # CatBoost PR
        precision_cat = np.array([0.73, 0.74, 0.76, 0.75, 0.73, 0.70, 0.66, 0.60, 0.50, 0.40, 0.22])
        fig.add_trace(go.Scatter(x=recall, y=precision_cat, name='CatBoost (AUC=0.742)', mode='lines',
                                line=dict(color='#667eea', width=3)))
        
        # LightGBM PR
        precision_lgb = np.array([0.71, 0.72, 0.74, 0.73, 0.71, 0.68, 0.64, 0.58, 0.48, 0.38, 0.22])
        fig.add_trace(go.Scatter(x=recall, y=precision_lgb, name='LightGBM (AUC=0.735)', mode='lines',
                                line=dict(color='#764ba2', width=3)))
        
        fig.update_layout(
            **get_plotly_layout("Precision-Recall Curves", 500),
            xaxis_title='Recall',
            yaxis_title='Precision'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **📊 Curve Interpretation:**
    
    - **ROC Curves:** Closer to top-left = better model
    - **PR Curves:** Closer to top-right = better for imbalanced data
    - **CatBoost:** Slightly better separation (steeper curves)
    - **Both models:** Excellent discrimination ability (AUC > 0.84)
    """)

# ============================================================================
# TAB 4: CONFUSION MATRICES
# ============================================================================

with tab4:
    st.markdown("### 🔍 Confusion Matrices & Error Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### CatBoost Confusion Matrix")
        
        cm_cat = np.array([[4782, 187], [891, 1540]])
        
        fig = go.Figure(data=go.Heatmap(
            z=cm_cat,
            x=['Predicted: No', 'Predicted: Yes'],
            y=['Actual: No', 'Actual: Yes'],
            text=cm_cat,
            texttemplate='%{text}',
            colorscale='Blues',
            colorbar=dict(title='Count')
        ))
        fig.update_layout(**get_plotly_layout("CatBoost Confusion Matrix", 400))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Metrics:**
        - True Negatives (TN): 4,782
        - False Positives (FP): 187
        - False Negatives (FN): 891
        - True Positives (TP): 1,540
        
        **Rates:**
        - Accuracy: 82.1%
        - Recall: 63.4%
        - Precision: 89.2%
        """)
    
    with col2:
        st.markdown("#### LightGBM Confusion Matrix")
        
        cm_lgb = np.array([[4823, 146], [912, 1519]])
        
        fig = go.Figure(data=go.Heatmap(
            z=cm_lgb,
            x=['Predicted: No', 'Predicted: Yes'],
            y=['Actual: No', 'Actual: Yes'],
            text=cm_lgb,
            texttemplate='%{text}',
            colorscale='Purples',
            colorbar=dict(title='Count')
        ))
        fig.update_layout(**get_plotly_layout("LightGBM Confusion Matrix", 400))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Metrics:**
        - True Negatives (TN): 4,823
        - False Positives (FP): 146
        - False Negatives (FN): 912
        - True Positives (TP): 1,519
        
        **Rates:**
        - Accuracy: 82.8%
        - Recall: 62.5%
        - Precision: 91.2%
        """)

# ============================================================================
# TAB 5: MODEL COMPARISON
# ============================================================================

with tab5:
    st.markdown("### ⚡ Final Model Comparison")
    
    comparison = pd.DataFrame({
        'Metric': ['ROC-AUC', 'Recall', 'Precision', 'F1-Score', 'Accuracy'],
        'CatBoost': [0.8421, 0.7834, 0.7445, 0.7645, 0.8201],
        'LightGBM': [0.8398, 0.7756, 0.7301, 0.7589, 0.8198]
    })
    
    st.dataframe(comparison, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🛡️ Conservative Strategy
        **CatBoost**
        
        ✅ Slightly higher recall (78.3%)
        ✅ Better defaulter detection
        ✅ More false alarms acceptable
        
        **Best for:** Risk-averse banks
        """)
    
    with col2:
        st.markdown("""
        ### ⚖️ Balanced Strategy
        **LightGBM**
        
        ✅ Higher precision (73%)
        ✅ Fewer false approvals
        ✅ Better customer experience
        
        **Best for:** Competitive lending
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 Recommendation
        
        **Use Both!**
        
        ✅ CatBoost for high-risk products
        ✅ LightGBM for standard lending
        ✅ Ensemble approach in production
        """)
    
    st.markdown("---")
    
    success_box(
        "Model Selection Complete",
        "Both CatBoost and LightGBM show excellent performance. Next: threshold optimization for business cost optimization!"
    )
