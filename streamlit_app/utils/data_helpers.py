# ============================================================================
# DATA & MODEL UTILITIES
# ============================================================================

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from utils.config import *

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

def get_project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent


def load_trained_models():
    """Load trained models from disk"""
    data_path = get_project_root() / "data"
    
    models = {
        "CatBoost": joblib.load(data_path / "catboost_model.pkl") if (data_path / "catboost_model.pkl").exists() else None,
        "LightGBM": joblib.load(data_path / "lightgbm_model.pkl") if (data_path / "lightgbm_model.pkl").exists() else None,
    }
    
    return models


def load_scaler():
    """Load feature scaler"""
    data_path = get_project_root() / "data"
    scaler_path = data_path / "scaler.pkl"
    
    if scaler_path.exists():
        return joblib.load(scaler_path)
    return None


def load_training_data():
    """Load preprocessed training data"""
    data_path = get_project_root() / "data"
    
    X_train_path = data_path / "X_train.pkl"
    X_test_path = data_path / "X_test.pkl"
    y_train_path = data_path / "y_train.pkl"
    y_test_path = data_path / "y_test.pkl"
    
    if all(p.exists() for p in [X_train_path, X_test_path, y_train_path, y_test_path]):
        return {
            "X_train": joblib.load(X_train_path),
            "X_test": joblib.load(X_test_path),
            "y_train": joblib.load(y_train_path),
            "y_test": joblib.load(y_test_path),
        }
    return None


def load_metrics():
    """Load precomputed metrics"""
    data_path = get_project_root() / "data"
    metrics_path = data_path / "metrics.pkl"
    
    if metrics_path.exists():
        return joblib.load(metrics_path)
    return None


def load_threshold_analysis():
    """Load threshold optimization results"""
    data_path = get_project_root() / "data"
    threshold_path = data_path / "threshold_analysis.pkl"
    
    if threshold_path.exists():
        return joblib.load(threshold_path)
    return None


# ============================================================================
# PREDICTION & EXPLANATION
# ============================================================================

def get_risk_level(probability: float) -> tuple:
    """
    Get risk level based on probability
    Returns: (risk_level, color, emoji)
    """
    if probability < 0.15:
        return "very_low", "#2ECC71", "🟢"
    elif probability < 0.30:
        return "low", "#3498DB", "🔵"
    elif probability < 0.50:
        return "medium", "#F39C12", "🟡"
    elif probability < 0.75:
        return "high", "#E74C3C", "🔴"
    else:
        return "very_high", "#C0392B", "⛔"


def get_risk_recommendation(probability: float, model_type: str = "balanced") -> dict:
    """
    Get approval recommendation based on probability and model type
    """
    if model_type == "conservative":
        # Conservative: Lower threshold for approval
        if probability < 0.35:
            recommendation = "APPROVED"
            confidence = 1 - probability
            reason = "Strong credit profile with minimal default risk."
        else:
            recommendation = "REVIEW"
            confidence = probability
            reason = "Significant default risk detected. Manual review recommended."
    else:
        # Balanced: Standard threshold
        if probability < 0.50:
            recommendation = "APPROVED"
            confidence = 1 - probability
            reason = "Acceptable credit profile with controlled risk."
        else:
            recommendation = "DENIED"
            confidence = probability
            reason = "High default probability. Application recommended for denial."
    
    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "reason": reason
    }


def calculate_business_cost(tp: int, fp: int, fn: int, tn: int) -> dict:
    """Calculate business cost metrics"""
    cost_fn = BUSINESS_COSTS["cost_fn"]
    cost_fp = BUSINESS_COSTS["cost_fp"]
    
    total_cost = (fn * cost_fn) + (fp * cost_fp)
    
    return {
        "total_cost": total_cost,
        "fn_cost": fn * cost_fn,
        "fp_cost": fp * cost_fp,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn
    }


# ============================================================================
# AI INSIGHTS GENERATION
# ============================================================================

def generate_graph_insight(chart_type: str, data_summary: dict) -> str:
    """Generate AI-powered insight for a graph"""
    
    insights_map = {
        "class_distribution": f"""
        **📊 What This Shows:** The dataset shows a class imbalance with {data_summary.get('non_default', 'N/A')}% 
        non-defaulters and {data_summary.get('default', 'N/A')}% defaulters.
        
        **💡 Business Insight:** This severe imbalance is typical in credit risk - defaults are rare events. 
        Our models use SMOTE (Synthetic Minority Over-sampling Technique) to handle this imbalance.
        
        **⚠️ Risk Implication:** The model must have high recall to catch defaulters, not just high accuracy.
        """,
        
        "correlation": """
        **📊 What This Shows:** Feature correlations reveal relationships between customer attributes.
        
        **💡 Business Insight:** Strong correlations with default indicate key risk drivers:
        - Payment history (PAY_1, PAY_2): Most critical predictor
        - Bill amount trends: Shows affordability
        - Age: Behavioral patterns by demographics
        
        **⚠️ Risk Implication:** We drop highly correlated features to avoid multicollinearity.
        """,
        
        "roc_curve": """
        **📊 What This Shows:** ROC curve plots True Positive Rate vs False Positive Rate at different thresholds.
        
        **💡 Business Insight:** The curve's proximity to the top-left corner indicates model quality.
        Higher AUC means better discrimination between defaulters and non-defaulters.
        
        **⚠️ Risk Implication:** Different strategies trade off recall (catching defaults) vs precision (reducing false alarms).
        """,
        
        "confusion_matrix": """
        **📊 What This Shows:** Breakdown of predictions:
        - True Positives (TP): Correctly identified defaulters
        - False Positives (FP): Creditworthy rejected (business loss)
        - True Negatives (TN): Correctly approved
        - False Negatives (FN): Missed defaulters (bank loss)
        
        **💡 Business Insight:** The cost of FN (₹10,000) >> FP (₹2,000), so we optimize for recall.
        
        **⚠️ Risk Implication:** Business costs drive threshold optimization, not just accuracy.
        """,
        
        "feature_importance": """
        **📊 What This Shows:** Which features most influence model predictions.
        
        **💡 Business Insight:** Top drivers typically:
        1. Payment status (recent payment behavior)
        2. Credit limit & utilization
        3. Age & income level
        
        **⚠️ Risk Implication:** SHAP values show individual customer contributions to risk score.
        """,
    }
    
    return insights_map.get(chart_type, "📊 Advanced model analysis insight.")


def generate_prediction_insight(probability: float, risk_level: str, features_dict: dict = None) -> str:
    """Generate AI-powered prediction explanation"""
    
    if probability < 0.20:
        base_insight = f"""
        ✅ **Strong Approval Signal**
        
        This customer exhibits minimal default risk at **{probability:.1%}** probability. 
        Key positive signals indicate:
        - Consistent payment history
        - Appropriate credit utilization
        - Good demographic profile
        
        **Recommendation:** APPROVE with confidence
        """
    elif probability < 0.40:
        base_insight = f"""
        🟢 **Good Credit Profile**
        
        Default probability of **{probability:.1%}** falls in the acceptable range.
        The customer shows:
        - Generally positive payment patterns
        - Manageable debt levels
        - Stable behavioral indicators
        
        **Recommendation:** APPROVE
        """
    elif probability < 0.60:
        base_insight = f"""
        🟡 **Moderate Risk**
        
        Default probability of **{probability:.1%}** suggests monitoring needed.
        Risk factors include:
        - Some payment delays or irregular behavior
        - Higher credit utilization
        - Mixed behavioral signals
        
        **Recommendation:** APPROVE with enhanced monitoring
        """
    elif probability < 0.80:
        base_insight = f"""
        🔴 **High Risk**
        
        Default probability of **{probability:.1%}** indicates elevated concern.
        Red flags include:
        - Consistent payment delays
        - High credit utilization
        - Negative trend in behavior
        
        **Recommendation:** MANUAL REVIEW REQUIRED
        """
    else:
        base_insight = f"""
        ⛔ **Very High Risk**
        
        Default probability of **{probability:.1%}** signals severe risk.
        Critical issues:
        - Severe payment delinquency
        - Maxed-out credit limits
        - Strong default indicators
        
        **Recommendation:** DENY or require significant risk mitigation
        """
    
    return base_insight


def generate_business_insight(metric_name: str, value: float, context: str = "") -> str:
    """Generate business interpretation of metrics"""
    
    insights = {
        "recall": f"""
        **Recall: {value:.1%}** - {context}
        
        This means we catch **{value:.1%}** of actual defaulters. A recall of ~70% is typical for 
        conservative strategies. Trade-off: May reject some good customers (false positives).
        """,
        
        "precision": f"""
        **Precision: {value:.1%}** - {context}
        
        Of customers we flag as defaulters, **{value:.1%}** actually default. Higher precision = 
        fewer false alarms but may miss some actual defaulters.
        """,
        
        "roc_auc": f"""
        **ROC-AUC: {value:.4f}** - {context}
        
        AUC of **{value:.1%}** indicates excellent discrimination ability. (Benchmark: 0.75+ is good, 
        0.85+ is excellent). Our models distinguish defaulters from non-defaulters effectively.
        """,
        
        "f1_score": f"""
        **F1-Score: {value:.4f}** - {context}
        
        Harmonic mean of precision and recall = **{value:.1%}**. Balances both metrics for 
        overall model quality. Higher is better (max = 1.0).
        """,
    }
    
    return insights.get(metric_name.lower(), f"Metric: {metric_name} = {value:.4f}")
