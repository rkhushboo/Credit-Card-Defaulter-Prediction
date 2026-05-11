# ============================================================================
# CREDIT CARD DEFAULT RISK PLATFORM
# Main Streamlit Application
# ============================================================================

import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import *
from utils.ui_components import inject_custom_css

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=PAGE_CONFIG["page_title"],
    page_icon=PAGE_CONFIG["page_icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state=PAGE_CONFIG["initial_sidebar_state"]
)

# ============================================================================
# INJECT CUSTOM STYLING
# ============================================================================

inject_custom_css()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; color: white; padding: 20px 0;'>
        <h1 style='font-size: 2.5em; margin: 0;'>🏦</h1>
        <h2 style='margin: 10px 0 5px 0;'>Credit Risk</h2>
        <p style='margin: 0; opacity: 0.9;'>AI Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN DASHBOARD LAYOUT (HOME PAGE)
# ============================================================================

def main():
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>🏦 Credit Card Default Risk Platform</div>
        <div class='hero-subtitle'>Enterprise-Grade AI Risk Intelligence System</div>
        <p style='font-size: 1.1em; opacity: 0.95; margin-top: 20px;'>
            Advanced machine learning platform for predicting credit card defaults and optimizing lending decisions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-box-label'>Total Records Analyzed</div>
            <div class='stat-box-value'>30,000</div>
            <div class='stat-box-label'>Credit Card Clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-box-label'>Model Performance</div>
            <div class='stat-box-value'>0.82</div>
            <div class='stat-box-label'>ROC-AUC Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-box-label'>Default Rate</div>
            <div class='stat-box-value'>22%</div>
            <div class='stat-box-label'>Class Imbalance</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Model Strategies", "📊 Platform Features", "🚀 Quick Start"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🛡️ Conservative Strategy
            **CatBoost Model**
            
            - **Objective:** Maximum defaulter detection
            - **Threshold Optimized:** 0.35
            - **Focus:** High Recall (~75%)
            - **Use Case:** Risk-averse lending
            
            Best for banks prioritizing default prevention over approvals.
            """)
        
        with col2:
            st.markdown("""
            ### ⚖️ Balanced Strategy
            **LightGBM Model**
            
            - **Objective:** Controlled risk with better approvals
            - **Threshold Optimized:** 0.50
            - **Focus:** Balanced Precision-Recall
            - **Use Case:** Competitive lending
            
            Best for banks balancing risk management with customer acquisitions.
            """)
    
    with tab2:
        st.markdown("""
        #### 🌟 Platform Capabilities
        
        1. **Dataset Analysis**
           - 30,000 credit card client records
           - Comprehensive EDA & visualization
           - Class imbalance analysis
        
        2. **Model Building**
           - 9 baseline models evaluated
           - Hyperparameter tuning (Grid Search CV)
           - SMOTE for imbalance handling
           - Threshold optimization for business costs
        
        3. **Risk Assessment**
           - Real-time credit default prediction
           - SHAP model explainability
           - Feature contribution analysis
        
        4. **Business Decision Support**
           - Cost-sensitive evaluation
           - Approval/rejection recommendations
           - Risk-based pricing intelligence
        """)
    
    with tab3:
        st.markdown("""
        #### 🚀 Getting Started
        
        **Navigation:** Use the sidebar to explore:
        
        - 📈 **Dataset Overview** - Understand the data structure
        - 🔍 **EDA & Analysis** - Explore patterns and insights
        - 🤖 **Model Building** - See how we built the models
        - 🎯 **Risk Strategy Simulator** - Make predictions
        - ⚡ **Threshold Optimization** - Understand business tradeoffs
        - 🧠 **Model Explainability** - SHAP analysis
        - 📋 **Project Summary** - Complete workflow overview
        
        **Tip:** Start with Dataset Overview for context!
        """)
    
    st.markdown("---")
    
    # Key Achievements
    st.markdown("### 🏆 Key Project Achievements")
    
    achievement_cols = st.columns(4)
    achievements = [
        ("High AUC", "0.82+", "Excellent discrimination"),
        ("Optimal Recall", "75%", "Catch defaulters"),
        ("Cost-Optimized", "₹320K", "Business value"),
        ("Enterprise-Ready", "✅", "Production grade")
    ]
    
    for col, (title, value, subtitle) in zip(achievement_cols, achievements):
        with col:
            st.markdown(f"""
            <div class='kpi-tile'>
                <div style='font-size: 1.3em; font-weight: bold; color: #667eea;'>{title}</div>
                <div style='font-size: 1.8em; font-weight: bold; color: #764ba2; margin: 10px 0;'>{value}</div>
                <div style='font-size: 0.85em; color: #666;'>{subtitle}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Stack
    st.markdown("### 🛠️ Technical Stack")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        **ML Models**
        - CatBoost
        - LightGBM
        - XGBoost
        - Random Forest
        
        **Data Processing**
        - Pandas
        - NumPy
        - Scikit-learn
        
        **Explainability**
        - SHAP
        """)
    
    with tech_col2:
        st.markdown("""
        **Imbalance Handling**
        - SMOTE
        - Stratified K-Fold
        
        **Hyperparameter Tuning**
        - Grid Search CV
        - Cross-Validation
        
        **Visualization**
        - Plotly
        - Matplotlib
        - Seaborn
        """)

if __name__ == "__main__":
    main()
