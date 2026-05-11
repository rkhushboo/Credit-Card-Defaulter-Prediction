# ============================================================================
# UI COMPONENTS & STYLING
# ============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.config import *

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

def inject_custom_css():
    """Inject custom CSS for premium fintech styling"""
    custom_css = """
    <style>
    /* ===== ROOT STYLING ===== */
    :root {
        --primary: #0066FF;
        --secondary: #FF6B6B;
        --success: #2ECC71;
        --warning: #F39C12;
        --danger: #E74C3C;
        --info: #3498DB;
        --dark: #2C3E50;
        --light: #ECF0F1;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .main {
        padding: 2rem;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* ===== METRICS CARD ===== */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* ===== RISK BADGE ===== */
    .risk-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
    }
    
    .risk-very-low {
        background: #D5F4E6;
        color: #27AE60;
    }
    
    .risk-low {
        background: #D6EAF8;
        color: #2E86C1;
    }
    
    .risk-medium {
        background: #FCF3CF;
        color: #D68910;
    }
    
    .risk-high {
        background: #FADBD8;
        color: #C0392B;
    }
    
    .risk-very-high {
        background: #F1948A;
        color: #78281F;
    }
    
    /* ===== CARD CONTAINER ===== */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
        margin-bottom: 15px;
    }
    
    .card-header {
        border-bottom: 2px solid #0066FF;
        padding-bottom: 15px;
        margin-bottom: 15px;
        font-size: 1.2em;
        font-weight: bold;
        color: #2C3E50;
    }
    
    /* ===== HEADER STYLING ===== */
    h1, h2, h3 {
        color: #2C3E50;
        font-weight: 700;
    }
    
    h1 {
        border-bottom: 3px solid #0066FF;
        padding-bottom: 10px;
    }
    
    /* ===== BUTTON STYLING ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    /* ===== TABS ===== */
    [data-testid="stTabs"] [role="tablist"] button {
        border-radius: 8px;
        margin-right: 10px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        border-radius: 10px;
        border: 1px solid #E0E0E0;
    }
    
    [data-testid="stExpander"] [role="button"] {
        background: #F8F9FA;
        border-radius: 10px;
    }
    
    /* ===== ALERT BOXES ===== */
    .alert-success {
        background: #D5F4E6;
        border-left: 4px solid #27AE60;
        padding: 15px;
        border-radius: 5px;
        color: #27AE60;
    }
    
    .alert-danger {
        background: #FADBD8;
        border-left: 4px solid #C0392B;
        padding: 15px;
        border-radius: 5px;
        color: #C0392B;
    }
    
    .alert-warning {
        background: #FCF3CF;
        border-left: 4px solid #D68910;
        padding: 15px;
        border-radius: 5px;
        color: #D68910;
    }
    
    .alert-info {
        background: #D6EAF8;
        border-left: 4px solid #2E86C1;
        padding: 15px;
        border-radius: 5px;
        color: #2E86C1;
    }
    
    /* ===== STAT BOX ===== */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stat-box-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .stat-box-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 3em;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        opacity: 0.95;
        margin-bottom: 20px;
    }
    
    /* ===== KPI TILES ===== */
    .kpi-tile {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .kpi-tile:hover {
        border-color: #0066FF;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.1);
    }
    
    .kpi-value {
        font-size: 2em;
        font-weight: bold;
        color: #0066FF;
    }
    
    .kpi-label {
        font-size: 0.9em;
        color: #666;
        margin-top: 5px;
    }
    
    /* ===== DIVIDER ===== */
    .divider {
        border-bottom: 2px solid #E0E0E0;
        margin: 30px 0;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    .slide-in-left {
        animation: slideInLeft 0.5s ease;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# ============================================================================
# METRIC DISPLAY COMPONENTS
# ============================================================================

def display_metric_card(title: str, value, subtitle: str = "", color: str = "primary"):
    """Display a styled metric card"""
    color_map = {
        "primary": "#667eea",
        "success": "#2ECC71",
        "warning": "#F39C12",
        "danger": "#E74C3C",
        "info": "#3498DB"
    }
    
    col_color = color_map.get(color, "#667eea")
    
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, {col_color} 0%, rgba({col_color}, 0.6) 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid {col_color};
    '>
        <div style='font-size: 0.95em; opacity: 0.9; margin-bottom: 10px;'>{title}</div>
        <div style='font-size: 2.5em; font-weight: bold; margin-bottom: 5px;'>{value}</div>
        <div style='font-size: 0.85em; opacity: 0.8;'>{subtitle}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def display_kpi_tiles(kpi_data: dict):
    """Display multiple KPI tiles in a row"""
    cols = st.columns(len(kpi_data))
    
    for col, (label, value) in zip(cols, kpi_data.items()):
        with col:
            st.markdown(f"""
            <div class='kpi-tile'>
                <div class='kpi-value'>{value}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)


def display_risk_badge(risk_level: str, probability: float = None):
    """Display a risk level badge"""
    risk_levels = {
        "very_low": ("🟢 Very Low Risk", "risk-very-low"),
        "low": ("🔵 Low Risk", "risk-low"),
        "medium": ("🟡 Medium Risk", "risk-medium"),
        "high": ("🔴 High Risk", "risk-high"),
        "very_high": ("⛔ Very High Risk", "risk-very-high"),
    }
    
    if risk_level in risk_levels:
        label, css_class = risk_levels[risk_level]
        prob_text = f" ({probability:.1%})" if probability else ""
        st.markdown(
            f'<span class="risk-badge {css_class}">{label}{prob_text}</span>',
            unsafe_allow_html=True
        )


def display_alert(message: str, alert_type: str = "info"):
    """Display styled alert box"""
    alert_class = f"alert-{alert_type}"
    st.markdown(f'<div class="{alert_class}">{message}</div>', unsafe_allow_html=True)


# ============================================================================
# CHART STYLING
# ============================================================================

def get_plotly_layout(title: str = "", height: int = 500):
    """Get consistent Plotly layout styling"""
    return dict(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "color": "#2C3E50", "family": "Arial, sans-serif"}
        },
        height=height,
        hovermode="x unified",
        plot_bgcolor="#F8F9FA",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color="#2C3E50"),
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#E0E0E0",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#E0E0E0",
            zeroline=False
        ),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E0E0E0",
            borderwidth=1
        )
    )


def create_gradient_bar_chart(data: dict, title: str = ""):
    """Create a styled bar chart with gradient colors"""
    fig = go.Figure()
    
    colors = ["#667eea", "#764ba2", "#FF6B6B", "#F39C12", "#2ECC71"]
    
    fig.add_trace(go.Bar(
        x=list(data.keys()),
        y=list(data.values()),
        marker=dict(
            color=colors[:len(data)],
            line=dict(color="white", width=2)
        ),
        text=[f"{v:.2f}" for v in data.values()],
        textposition="auto",
    ))
    
    fig.update_layout(
        **get_plotly_layout(title),
        showlegend=False
    )
    
    return fig


def create_gauge_chart(value: float, max_value: float = 1.0, title: str = ""):
    """Create a gauge chart for probability/score display"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value * 100,
        title={"text": title},
        delta={"reference": 50},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#667eea"},
            "steps": [
                {"range": [0, 25], "color": "#2ECC71"},
                {"range": [25, 50], "color": "#F39C12"},
                {"range": [50, 75], "color": "#FF6B6B"},
                {"range": [75, 100], "color": "#C0392B"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 90
            }
        }
    ))
    
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
    return fig


# ============================================================================
# SECTION COMPONENTS
# ============================================================================

def section_header(title: str, emoji: str = "📊"):
    """Display a styled section header"""
    st.markdown(f"## {emoji} {title}")
    st.markdown("---")


def info_box(title: str, content: str, icon: str = "ℹ️"):
    """Display an information box"""
    st.info(f"{icon} **{title}**\n\n{content}")


def success_box(title: str, content: str):
    """Display a success box"""
    display_alert(f"✅ **{title}**\n\n{content}", "success")


def warning_box(title: str, content: str):
    """Display a warning box"""
    display_alert(f"⚠️ **{title}**\n\n{content}", "warning")


def error_box(title: str, content: str):
    """Display an error box"""
    display_alert(f"❌ **{title}**\n\n{content}", "danger")
