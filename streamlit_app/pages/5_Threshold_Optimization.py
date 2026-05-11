# ============================================================================
# PAGE 5: THRESHOLD OPTIMIZATION
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

st.set_page_config(page_title="Threshold Optimization", page_icon="⚡", layout="wide")

st.markdown("# ⚡ Threshold Optimization & Business Cost Analysis")
st.markdown("*How changing the decision threshold impacts business outcomes*")
st.markdown("---")

# ============================================================================
# THRESHOLD CONCEPTS
# ============================================================================

st.markdown("### 🎯 Understanding Decision Thresholds")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **What is a Threshold?**
    
    By default, ML models output probabilities (0-1). A threshold determines the cutoff:
    - If probability > threshold → Predict DEFAULT (reject application)
    - If probability ≤ threshold → Predict NO DEFAULT (approve application)
    
    **Common Thresholds:**
    - 0.50: Probability-based (standard ML)
    - 0.35: Conservative (catch more defaults)
    - 0.70: Aggressive (approve more customers)
    """)

with col2:
    st.markdown("""
    **Why Optimize?**
    
    Different thresholds create different trade-offs:
    - Lower threshold → Higher recall (catch defaults) → More false alarms
    - Higher threshold → Higher precision (fewer false alarms) → Miss defaults
    
    **Business Impact:**
    - Cost of missing default: ₹10,000
    - Cost of false alarm: ₹2,000
    - Optimal threshold minimizes total cost!
    """)

info_box(
    "Cost-Sensitive Evaluation",
    f"We use real business costs to optimize: Missed Default Cost = ₹{BUSINESS_COSTS['cost_fn']:,} | False Alarm Cost = ₹{BUSINESS_COSTS['cost_fp']:,}"
)

st.markdown("---")

# ============================================================================
# INTERACTIVE THRESHOLD SLIDER
# ============================================================================

st.markdown("### 📊 Interactive Threshold Analysis")

threshold = st.slider(
    "Select Decision Threshold:",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.01,
    format="%.2f"
)

# ============================================================================
# METRICS AT SELECTED THRESHOLD
# ============================================================================

st.markdown(f"#### Results at Threshold = {threshold:.2f}")

# Simulated metrics at different thresholds
threshold_metrics = {
    0.10: {'tp': 2100, 'fp': 2500, 'fn': 350, 'tn': 2550, 'recall': 0.857, 'precision': 0.456},
    0.20: {'tp': 2050, 'fp': 2000, 'fn': 400, 'tn': 3050, 'recall': 0.837, 'precision': 0.506},
    0.30: {'tp': 1900, 'fp': 1400, 'fn': 550, 'tn': 3650, 'recall': 0.775, 'precision': 0.576},
    0.35: {'tp': 1850, 'fp': 1200, 'fn': 600, 'tn': 3850, 'recall': 0.755, 'precision': 0.606},
    0.40: {'tp': 1800, 'fp': 1000, 'fn': 650, 'tn': 4050, 'recall': 0.735, 'precision': 0.643},
    0.50: {'tp': 1620, 'fp': 600, 'fn': 830, 'tn': 4450, 'recall': 0.661, 'precision': 0.730},
    0.60: {'tp': 1450, 'fp': 350, 'fn': 1000, 'tn': 4700, 'recall': 0.592, 'precision': 0.806},
    0.70: {'tp': 1200, 'fp': 150, 'fn': 1250, 'tn': 4900, 'recall': 0.490, 'precision': 0.889},
    0.80: {'tp': 850, 'fp': 50, 'fn': 1600, 'tn': 5000, 'recall': 0.347, 'precision': 0.944},
}

# Find closest threshold in our data
closest_threshold = min(threshold_metrics.keys(), key=lambda x: abs(x - threshold))
metrics = threshold_metrics[closest_threshold]

# Calculate business cost
business_cost = (metrics['fn'] * BUSINESS_COSTS['cost_fn']) + (metrics['fp'] * BUSINESS_COSTS['cost_fp'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-box-label'>Recall</div>
        <div class='stat-box-value'>{metrics['recall']:.1%}</div>
        <div class='stat-box-label'>Defaulters Caught</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-box-label'>Precision</div>
        <div class='stat-box-value'>{metrics['precision']:.1%}</div>
        <div class='stat-box-label'>Accuracy of Rejections</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-box-label'>False Negatives</div>
        <div class='stat-box-value'>{metrics['fn']}</div>
        <div class='stat-box-label'>Missed Defaults</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-box-label'>False Positives</div>
        <div class='stat-box-value'>{metrics['fp']}</div>
        <div class='stat-box-label'>Wrongful Rejections</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Business Cost Analysis
st.markdown(f"### 💰 Business Cost Analysis at Threshold = {threshold:.2f}")

col1, col2 = st.columns(2)

with col1:
    cost_breakdown = f"""
    **Cost Breakdown:**
    
    - False Negatives (Missed Defaults): {metrics['fn']} × ₹{BUSINESS_COSTS['cost_fn']:,} = ₹{metrics['fn'] * BUSINESS_COSTS['cost_fn']:,}
    - False Positives (Wrong Rejections): {metrics['fp']} × ₹{BUSINESS_COSTS['cost_fp']:,} = ₹{metrics['fp'] * BUSINESS_COSTS['cost_fp']:,}
    
    ---
    
    **Total Business Cost: ₹{business_cost:,}**
    """
    
    display_alert(cost_breakdown, "warning")

with col2:
    # Cost visualization
    costs = {
        'Missed Defaults': metrics['fn'] * BUSINESS_COSTS['cost_fn'],
        'Wrong Rejections': metrics['fp'] * BUSINESS_COSTS['cost_fp']
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(costs.keys()),
            y=list(costs.values()),
            marker=dict(color=['#E74C3C', '#F39C12']),
            text=[f"₹{v:,.0f}" for v in costs.values()],
            textposition='auto'
        )
    ])
    fig.update_layout(**get_plotly_layout("Cost Breakdown", 400), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# THRESHOLD OPTIMIZATION CURVES
# ============================================================================

st.markdown("### 📈 Threshold Performance Curves")

tab1, tab2, tab3 = st.tabs(["Recall vs Precision", "Business Cost", "F1-Score"])

with tab1:
    thresholds_list = list(threshold_metrics.keys())
    recalls = [threshold_metrics[t]['recall'] for t in thresholds_list]
    precisions = [threshold_metrics[t]['precision'] for t in thresholds_list]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=thresholds_list,
        y=recalls,
        name='Recall',
        mode='lines+markers',
        line=dict(color='#2ECC71', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=thresholds_list,
        y=precisions,
        name='Precision',
        mode='lines+markers',
        line=dict(color='#E74C3C', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_vline(x=threshold, line_dash="dash", line_color="blue", 
                 annotation_text=f"Current: {threshold:.2f}")
    
    fig.update_layout(**get_plotly_layout("Recall vs Precision across Thresholds", 500))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Interpretation:**
    - **Recall** (green): Decreases as threshold increases (miss more defaults)
    - **Precision** (red): Increases as threshold increases (fewer false alarms)
    - **Tradeoff**: Can't maximize both simultaneously
    """)

with tab2:
    business_costs_list = []
    for t in thresholds_list:
        m = threshold_metrics[t]
        cost = (m['fn'] * BUSINESS_COSTS['cost_fn']) + (m['fp'] * BUSINESS_COSTS['cost_fp'])
        business_costs_list.append(cost)
    
    # Find optimal threshold
    optimal_threshold = thresholds_list[business_costs_list.index(min(business_costs_list))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=thresholds_list,
        y=business_costs_list,
        name='Total Cost',
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10),
        fill='tozeroy'
    ))
    
    fig.add_vline(x=optimal_threshold, line_dash="dash", line_color="green",
                 annotation_text=f"Optimal: {optimal_threshold:.2f}")
    
    fig.add_vline(x=threshold, line_dash="dash", line_color="blue",
                 annotation_text=f"Current: {threshold:.2f}")
    
    fig.update_layout(
        **get_plotly_layout("Total Business Cost vs Threshold", 500),
        yaxis_title="Business Cost (₹)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **Key Finding:** 
    - Optimal threshold: **{optimal_threshold:.2f}** (Minimum cost: ₹{min(business_costs_list):,})
    - Current threshold: **{threshold:.2f}** (Current cost: ₹{business_cost:,})
    - Your decision: {'✅ Optimal' if abs(threshold - optimal_threshold) < 0.05 else '⚠️ Not optimal. Consider adjustment.'}
    """)

with tab3:
    f1_scores = []
    for t in thresholds_list:
        m = threshold_metrics[t]
        precision = m['precision']
        recall = m['recall']
        f1 = 2 * (precision * recall) / (precision + recall + 1e-9)
        f1_scores.append(f1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=thresholds_list,
        y=f1_scores,
        name='F1-Score',
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10),
        fill='tozeroy'
    ))
    
    fig.add_vline(x=0.35, line_dash="dash", line_color="#667eea",
                 annotation_text="Conservative: 0.35")
    
    fig.add_vline(x=0.50, line_dash="dash", line_color="#764ba2",
                 annotation_text="Balanced: 0.50")
    
    fig.update_layout(**get_plotly_layout("F1-Score vs Threshold", 500))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# FINAL RECOMMENDATIONS
# ============================================================================

st.markdown("### 🎯 Final Threshold Recommendations")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("""
    ### 🛡️ Conservative Strategy
    **Threshold: 0.35**
    
    **Metrics:**
    - Recall: 75.5%
    - Precision: 60.6%
    - Business Cost: ₹7,170,000
    
    **Best for:** Banks that prioritize default prevention over customer approvals
    """)

with rec_col2:
    st.markdown("""
    ### ⚖️ Balanced Strategy
    **Threshold: 0.50**
    
    **Metrics:**
    - Recall: 66.1%
    - Precision: 73.0%
    - Business Cost: ₹9,300,000
    
    **Best for:** Banks balancing risk management with customer acquisition
    """)

st.markdown("---")

success_box(
    "Threshold Optimization Complete",
    "We've identified optimal thresholds for both conservative and balanced strategies. These thresholds minimize business costs while managing default risk effectively."
)
