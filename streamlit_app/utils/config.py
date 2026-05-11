# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

import streamlit as st

# ============================================================================
# APP CONFIGURATION
# ============================================================================

APP_TITLE = "Credit Card Default Risk Platform"
APP_SUBTITLE = "Enterprise-Grade AI Risk Intelligence System"
APP_DESCRIPTION = "Advanced credit risk assessment powered by machine learning"

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

MODELS_CONFIG = {
    "CatBoost": {
        "name": "CatBoost (Conservative)",
        "description": "Conservative Risk Strategy - Maximum defaulter detection",
        "style": "danger",
        "emoji": "🛡️",
        "strategy": "Conservative",
        "recall_focus": True,
        "threshold": 0.35,  # Will be loaded from data
        "color": "#FF6B6B"
    },
    "LightGBM": {
        "name": "LightGBM (Balanced)",
        "description": "Balanced Approval Strategy - Controlled risk with better approvals",
        "style": "info",
        "emoji": "⚖️",
        "strategy": "Balanced",
        "recall_focus": False,
        "threshold": 0.50,  # Will be loaded from data
        "color": "#4ECDC4"
    }
}

# ============================================================================
# BUSINESS COSTS
# ============================================================================

BUSINESS_COSTS = {
    "cost_fn": 10000,  # Cost of missed defaulter
    "cost_fp": 2000     # Cost of false alarm (rejected creditworthy customer)
}

# ============================================================================
# THEME & STYLING
# ============================================================================

PRIMARY_COLOR = "#0066FF"
SECONDARY_COLOR = "#FF6B6B"
SUCCESS_COLOR = "#2ECC71"
WARNING_COLOR = "#F39C12"
DANGER_COLOR = "#E74C3C"
INFO_COLOR = "#3498DB"
DARK_COLOR = "#2C3E50"
LIGHT_COLOR = "#ECF0F1"

RISK_COLORS = {
    "very_low": "#2ECC71",      # Green
    "low": "#3498DB",            # Blue
    "medium": "#F39C12",         # Orange
    "high": "#E74C3C",          # Red
    "very_high": "#C0392B"      # Dark Red
}

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

PAGE_CONFIG = {
    "page_title": "Credit Risk Platform",
    "page_icon": "🏦",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ============================================================================
# FEATURE NAMES (After Preprocessing)
# ============================================================================

FEATURE_NAMES = [
    'LIMIT_BAL', 'AGE', 'PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]

# ============================================================================
# INSIGHT TEMPLATES
# ============================================================================

INSIGHT_TEMPLATES = {
    "high_probability": "⚠️ **High Risk Alert**: This customer has a {prob:.1%} probability of default. Our model identifies high-risk behavioral patterns.",
    "medium_probability": "⚠️ **Medium Risk**: Default probability at {prob:.1%}. Recommend enhanced monitoring.",
    "low_probability": "✅ **Low Risk**: Strong approval signals. Default probability only {prob:.1%}.",
    "approval": "✅ **RECOMMENDED: APPROVE** - Strong credit profile with {recall:.1%} confidence.",
    "rejection": "❌ **RECOMMENDED: REVIEW** - Risk level exceeds threshold. Manual review suggested.",
}
