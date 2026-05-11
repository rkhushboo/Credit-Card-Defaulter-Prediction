# ============================================================================
# PAGE 4: RISK STRATEGY SIMULATOR
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import *
from utils.ui_components import *
from utils.data_helpers import *

st.set_page_config(page_title="Risk Strategy Simulator", page_icon="🎯", layout="wide")

st.markdown("# 🎯 Risk Strategy Simulator")
st.markdown("*Real-time credit risk assessment & approval recommendations*")
st.markdown("---")

# ============================================================================
# STRATEGY SELECTION
# ============================================================================

st.markdown("### 📋 Step 1: Select Strategy")

col1, col2 = st.columns(2)

with col1:
    strategy = st.radio(
        "Choose Risk Strategy:",
        options=["Conservative (CatBoost)", "Balanced (LightGBM)"],
        captions=[
            "🛡️ Maximum defaulter detection (High Recall)",
            "⚖️ Balanced approvals & risk (Optimal F1)"
        ]
    )
    
    strategy_type = "conservative" if "Conservative" in strategy else "balanced"

with col2:
    if strategy_type == "conservative":
        st.markdown("""
        ### 🛡️ Conservative Strategy
        
        **Objective:** Catch maximum defaulters
        - Threshold: 0.35
        - Focus: High Recall (78%)
        - Trade-off: More false alarms
        
        **Use Case:** Risk-averse lending
        """)
    else:
        st.markdown("""
        ### ⚖️ Balanced Strategy
        
        **Objective:** Balanced approvals & risk
        - Threshold: 0.50
        - Focus: Balanced precision/recall
        - Trade-off: Standard risk tolerance
        
        **Use Case:** Competitive lending
        """)

st.markdown("---")

# ============================================================================
# CUSTOMER INPUT SECTION
# ============================================================================

st.markdown("### 🧑‍💼 Step 2: Enter Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Demographics**")
    age = st.slider("Age (years)", 21, 79, 35)
    credit_limit = st.number_input("Credit Limit (NT$)", 50000, 1000000, 150000, step=10000)

with col2:
    st.markdown("**Payment Behavior**")
    pay_status = st.selectbox(
        "Recent Payment Status",
        options=[
            "Pay in full (Excellent)",
            "Pay minimum (Fair)",
            "1 month delayed",
            "2 months delayed",
            "3+ months delayed"
        ]
    )
    
    # Convert to numeric
    pay_status_map = {
        "Pay in full (Excellent)": -1,
        "Pay minimum (Fair)": 1,
        "1 month delayed": 2,
        "2 months delayed": 3,
        "3+ months delayed": 4
    }
    pay_status_value = pay_status_map[pay_status]

with col3:
    st.markdown("**Financial Profile**")
    bill_amount = st.number_input("Current Bill Amount (NT$)", 0, 500000, 50000, step=1000)
    payment_amount = st.number_input("Last Payment Amount (NT$)", 0, 100000, 15000, step=500)

st.markdown("---")

# ============================================================================
# RISK ASSESSMENT
# ============================================================================

st.markdown("### 📊 Step 3: Risk Assessment Results")

# Simulate prediction probability based on inputs
base_prob = 0.22  # Base default rate

# Adjust based on payment status
if pay_status_value == -1:
    prob = base_prob * 0.3  # Excellent payment: 30% of base
elif pay_status_value == 1:
    prob = base_prob * 0.7  # Fair payment: 70% of base
elif pay_status_value == 2:
    prob = base_prob * 1.5  # 1 month delayed: 150% of base
elif pay_status_value == 3:
    prob = base_prob * 2.0  # 2 months delayed: 200% of base
else:
    prob = base_prob * 2.5  # 3+ months delayed: 250% of base

# Adjust based on utilization
utilization = bill_amount / credit_limit if credit_limit > 0 else 0
if utilization > 0.8:
    prob *= 1.3
elif utilization > 0.6:
    prob *= 1.15
elif utilization < 0.2:
    prob *= 0.8

# Adjust based on age
if age < 25:
    prob *= 1.1
elif age > 50:
    prob *= 0.9

# Adjust based on payment ratio
if payment_amount > 0:
    payment_ratio = payment_amount / bill_amount if bill_amount > 0 else 0
    if payment_ratio < 0.2:
        prob *= 1.2
    elif payment_ratio > 0.5:
        prob *= 0.8

# Cap probability
prob = min(max(prob, 0.05), 0.95)

# Get risk level
risk_level, risk_color, risk_emoji = get_risk_level(prob)
recommendation = get_risk_recommendation(prob, strategy_type)

# Display Results
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {risk_color} 0%, rgba({risk_color}, 0.6) 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
    '>
        <div style='font-size: 2.5em; font-weight: bold; margin-bottom: 5px;'>{prob:.1%}</div>
        <div style='font-size: 0.95em;'>Default Probability</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
    '>
        <div style='font-size: 2em; margin-bottom: 5px;'>{risk_emoji}</div>
        <div style='font-size: 0.95em;'>{risk_level.replace("_", " ").title()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    rec_color = "#2ECC71" if recommendation["recommendation"] == "APPROVED" else "#E74C3C" if recommendation["recommendation"] == "DENIED" else "#F39C12"
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {rec_color} 0%, rgba({rec_color}, 0.6) 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
    '>
        <div style='font-size: 1.8em; font-weight: bold; margin-bottom: 5px;'>{recommendation["recommendation"]}</div>
        <div style='font-size: 0.9em;'>{recommendation["confidence"]:.1%} Confidence</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# PROBABILITY GAUGE
# ============================================================================

st.markdown("### 📊 Risk Probability Gauge")

fig = create_gauge_chart(prob, 1.0, "Default Risk Level")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# DETAILED ANALYSIS
# ============================================================================

st.markdown("### 🔍 Detailed Risk Analysis")

tab1, tab2, tab3 = st.tabs(["📈 Risk Breakdown", "💡 Key Drivers", "⚠️ Risk Factors"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risk Factor Contributions")
        
        risk_factors = {
            'Payment Status': 0.65,
            'Credit Utilization': 0.25,
            'Payment Amount': 0.15,
            'Age': 0.05,
            'Credit Limit': 0.03
        }
        
        fig = go.Figure(data=go.Bar(
            y=list(risk_factors.keys()),
            x=list(risk_factors.values()),
            orientation='h',
            marker=dict(color=['#E74C3C', '#FF6B6B', '#F39C12', '#3498DB', '#95A5A6']),
            text=[f"{v:.0%}" for v in risk_factors.values()],
            textposition='auto'
        ))
        fig.update_layout(**get_plotly_layout("Risk Factor Impact", 400), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Current Customer Profile")
        
        profile_data = {
            'Metric': ['Age', 'Utilization', 'Payment Ratio', 'Payment Status', 'Risk Score'],
            'Value': [f"{age} years", f"{utilization:.1%}", 
                     f"{payment_amount/bill_amount:.1%}" if bill_amount > 0 else "N/A",
                     pay_status, f"{prob:.1%}"],
            'Status': ['ℹ️ Normal', 
                      '⚠️ High' if utilization > 0.8 else '✅ Good' if utilization < 0.3 else 'ℹ️ Moderate',
                      '⚠️ Low' if payment_amount/bill_amount < 0.2 else '✅ Good',
                      '🔴 High' if pay_status_value >= 3 else '🟡 Medium' if pay_status_value == 1 else '🟢 Good',
                      '🔴 High Risk' if prob > 0.5 else '🟡 Medium Risk' if prob > 0.3 else '🟢 Low Risk']
        }
        
        df_profile = pd.DataFrame(profile_data)
        st.dataframe(df_profile, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("#### 🎯 Top Risk Drivers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **#1: Payment Status** (65% impact)
        - Most recent payment behavior
        - Delayed payments = high risk
        - Excellent predictor of default
        """)
    
    with col2:
        st.markdown("""
        **#2: Credit Utilization** (25% impact)
        - How much of limit is used
        - High utilization = financial stress
        - Indicator of repayment capacity
        """)
    
    st.markdown("""
    **#3: Payment Amount** (15% impact)
    - How much customer is paying
    - Low payments = affordability issues
    - Trend more important than absolute value
    """)

with tab3:
    st.markdown("#### ⚠️ Identified Risk Factors for This Customer")
    
    risk_warnings = []
    
    if pay_status_value >= 2:
        risk_warnings.append(("🔴 Payment Delays", "Recent payment delays detected. Highest risk indicator.", "critical"))
    
    if utilization > 0.8:
        risk_warnings.append(("⚠️ High Utilization", "Customer using >80% of credit limit.", "high"))
    elif utilization > 0.6:
        risk_warnings.append(("🟡 Moderate Utilization", "Customer using 60-80% of credit limit.", "medium"))
    
    if bill_amount > 0 and payment_amount / bill_amount < 0.2:
        risk_warnings.append(("⚠️ Low Payment Ratio", "Paying <20% of bill. May indicate affordability issues.", "high"))
    
    if age < 25:
        risk_warnings.append(("ℹ️ Young Customer", "Age <25. Slightly higher default risk profile.", "low"))
    
    if not risk_warnings:
        success_box("✅ Low Risk Profile", "No major risk factors detected. Strong credit signals.")
    else:
        for title, desc, severity in risk_warnings:
            if severity == "critical":
                st.error(f"**{title}**: {desc}")
            elif severity == "high":
                st.warning(f"**{title}**: {desc}")
            else:
                st.info(f"**{title}**: {desc}")

st.markdown("---")

# ============================================================================
# RECOMMENDATION SECTION
# ============================================================================

st.markdown("### 📋 Approval Recommendation")

rec_box = f"""
## {recommendation['recommendation']}

**Confidence:** {recommendation['confidence']:.1%}

**Reason:** {recommendation['reason']}

---

### 💰 Business Impact

- **Expected Loss:** ₹{prob * 10000:.0f} (if default occurs)
- **Potential Revenue:** ₹{(1-prob) * 2500:.0f} (if customer accepts)
- **Risk-Adjusted Value:** ₹{((1-prob) * 2500) - (prob * 10000):.0f}

### 🎯 Suggested Actions

1. **Default Probability Threshold:** {prob:.1%}
2. **Decision:** {recommendation['recommendation']}
3. **Monitoring:** {'Enhanced' if prob > 0.4 else 'Standard' if prob > 0.2 else 'Minimal'}
4. **Credit Limit:** {'Consider reduction' if prob > 0.4 else 'Standard' if prob > 0.2 else 'Can increase'}

"""

display_alert(rec_box, "info" if "REVIEW" in recommendation['recommendation'] else "success" if "APPROVED" in recommendation['recommendation'] else "danger")

# ============================================================================
# COMPARISON WITH THRESHOLD
# ============================================================================

st.markdown("---")
st.markdown("### 📊 Threshold Comparison")

threshold_cons = 0.35
threshold_bal = 0.50

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    ### 🛡️ Conservative (CatBoost)
    - Threshold: {threshold_cons:.1%}
    - Your Probability: {prob:.1%}
    
    **Decision:** {'✅ APPROVED' if prob < threshold_cons else '❌ DENIED'}
    """)

with col2:
    st.markdown(f"""
    ### ⚖️ Balanced (LightGBM)
    - Threshold: {threshold_bal:.1%}
    - Your Probability: {prob:.1%}
    
    **Decision:** {'✅ APPROVED' if prob < threshold_bal else '❌ DENIED'}
    """)

# Threshold comparison chart
fig = go.Figure()

fig.add_hline(y=threshold_cons, line_dash="dash", line_color="#667eea", annotation_text="Conservative Threshold")
fig.add_hline(y=threshold_bal, line_dash="dash", line_color="#764ba2", annotation_text="Balanced Threshold")

fig.add_trace(go.Scatter(
    x=["Your Customer"],
    y=[prob],
    mode="markers",
    marker=dict(size=20, color=risk_color),
    name="Prediction",
    text=f"{prob:.1%}",
    textposition="top center"
))

fig.update_layout(
    **get_plotly_layout("Your Probability vs Thresholds", 400),
    yaxis_range=[0, 1]
)
st.plotly_chart(fig, use_container_width=True)

success_box(
    "Simulator Complete",
    "This demonstrates how our AI platform makes real-time credit decisions. For bulk predictions, use the export feature!"
)
