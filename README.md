# Credit Card Defaulter Prediction 💳

A comprehensive machine learning project for predicting credit card default risk using advanced classification models (CatBoost & LightGBM) with SHAP explainability. Features an interactive Streamlit dashboard for risk assessment and model analysis.

---

## 📊 Project Overview

**Objective:** Build a robust classification model to predict credit card default risk with high recall on defaulters.

**Dataset:** Taiwan Credit Card Client Default Data
- **Records:** 30,000 customers
- **Features:** 18 (after VIF-based reduction)
- **Target:** Default status (0 = Non-default, 1 = Default)
- **Class Distribution:** 78% Non-default, 22% Default (imbalanced)

**Business Problem:**
- **Cost of False Negative (Missed Defaulter):** ₹10,000
- **Cost of False Positive (False Alarm):** ₹2,000
- Minimize total business cost while maintaining acceptable recall

---

## 🎯 Key Features

### 🤖 Two Optimized Models

1. **CatBoost (Conservative Strategy)**
   - Optimized for: Maximum recall (catch all defaulters)
   - Optimal Threshold: 0.35
   - Use Case: Risk-averse lending decisions

2. **LightGBM (Balanced Strategy)**
   - Optimized for: Optimal F1-Score & ROC-AUC
   - Optimal Threshold: 0.50
   - Use Case: Balanced precision-recall tradeoff

### 📈 Model Performance

| Metric | CatBoost | LightGBM |
|--------|----------|----------|
| ROC-AUC | ~0.76 | ~0.74 |
| Recall | ~0.82 | ~0.75 |
| Precision | ~0.47 | ~0.55 |
| F1-Score | ~0.60 | ~0.64 |

### 🎛️ Interactive Streamlit Dashboard

**7-Page Application:**

1. **📊 Dataset Overview** - Data composition, quality metrics, feature breakdown
2. **🔍 EDA & Analysis** - Correlation analysis, distributions, relationships
3. **🤖 Model Building** - Baseline vs tuned models, performance comparison
4. **🎯 Risk Simulator** - Real-time customer risk assessment with approval recommendations
5. **⚡ Threshold Optimization** - Cost-benefit analysis for threshold tuning
6. **🧠 Explainability** - SHAP global & local explanations for model predictions
7. **📋 Project Summary** - Deployment checklist, project narrative

---

## 🔧 Technical Stack

**Data Processing:**
- Pandas, NumPy
- Scikit-learn (preprocessing, metrics)
- SMOTE (class imbalance handling)
- StandardScaler (feature normalization)

**Models:**
- CatBoost 1.2.10
- LightGBM 4.6.0
- GridSearchCV (hyperparameter tuning)

**Explainability:**
- SHAP 0.51.0 (feature importance, waterfall plots)

**Dashboard:**
- Streamlit 1.57.0
- Plotly 6.7.0 (interactive visualizations)

**Environment:**
- Python 3.12.0
- Conda (virtual environment)

---

## 📁 Project Structure

```
Credit_Card_Defaulter/
│
├── streamlit_app/
│   ├── app.py                          # Homepage/main entry point
│   ├── train_export.py                 # Model training pipeline
│   ├── requirements.txt                # Python dependencies
│   ├── .streamlit/
│   │   └── config.toml                 # Streamlit configuration
│   ├── data/                           # Model artifacts (trained models, scalers)
│   │   ├── catboost_model.pkl
│   │   ├── lightgbm_model.pkl
│   │   ├── scaler.pkl
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   ├── y_test.pkl
│   │   ├── X_train_res.pkl             # SMOTE-balanced training data
│   │   ├── y_train_res.pkl
│   │   ├── thresholds_catboost.pkl
│   │   ├── thresholds_lightgbm.pkl
│   │   ├── metrics.pkl
│   │   └── vif_df.pkl
│   ├── utils/
│   │   ├── config.py                   # Configuration & constants
│   │   ├── ui_components.py            # Reusable UI components
│   │   └── data_helpers.py             # Data loading utilities
│   └── pages/
│       ├── 1_Dataset_Overview.py       # Page 1
│       ├── 2_EDA_Analysis.py           # Page 2
│       ├── 3_Model_Building.py         # Page 3
│       ├── 4_Risk_Simulator.py         # Page 4 ⭐
│       ├── 5_Threshold_Optimization.py # Page 5
│       ├── 6_Explainability.py         # Page 6 ⭐ (SHAP)
│       └── 7_Project_Summary.py        # Page 7
│
├── Credit_Card_Default_Capstone_Report.ipynb  # Original analysis notebook
├── Credit_Card_Default.csv                     # Dataset (30K records)
├── requirements.txt                            # Root dependencies
├── .gitignore                                  # Git ignore rules
└── README.md                                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git
- Conda (optional, for virtual environment)

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/rkhushboo/Credit-Card-Defaulter-Prediction.git
   cd Credit_Card_Defaulter
   ```

2. **Create Virtual Environment (Optional)**
   ```bash
   # Using Conda
   conda create -n credit_risk python=3.12
   conda activate credit_risk
   
   # OR using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r streamlit_app/requirements.txt
   ```

4. **Launch Streamlit App**
   ```bash
   cd streamlit_app
   streamlit run app.py
   ```

5. **Access Dashboard**
   - Open browser → `http://localhost:8501`
   - Navigate through 7-page dashboard
   - Use **Risk Simulator** to test predictions

---

## 📊 Dataset Information

**Source:** UCI Machine Learning Repository - Taiwan Credit Card Dataset

**Features (18 after preprocessing):**
- **Demographics:** Age, Sex, Education, Marital Status
- **Credit Limits:** Credit Limit
- **Billing & Payment:** 
  - Last 6 months billing amounts (BILL_AMT1,...)
  - Last 6 months repayment amounts (PAY_AMT1, ...)
  - Last 6 months payment status (PAY_1, ..., PAY_6)

**Data Preprocessing:**
✅ Outlier capping (IQR method)
✅ Multicollinearity reduction (VIF analysis)
✅ Class imbalance handling (SMOTE)
✅ Feature scaling (StandardScaler)

---

## 🔄 Model Training Pipeline

### Step 1: Data Preparation
```
Raw Data → Cleaning → Outlier Handling → Feature Selection
```

### Step 2: Train-Test Split
```
70% Training (23,972 samples after SMOTE)
30% Testing (5,993 samples)
Stratified split to preserve class ratios
```

### Step 3: Class Imbalance Handling
```
SMOTE applied to training data only (prevents data leakage)
Balanced ratio: 1:1 (from original 3.5:1)
```

### Step 4: Hyperparameter Tuning
```
GridSearchCV with 5-fold cross-validation
Scoring metric: ROC-AUC
Best parameters identified for both models
```

### Step 5: Threshold Optimization
```
Search thresholds 0.10 to 0.90
Calculate business cost for each threshold
Select threshold with minimum total cost
CatBoost: 0.35 (maximize recall)
LightGBM: 0.50 (balanced approach)
```

---

## 🧠 Key Insights

### Feature Importance (SHAP)
Top features affecting default prediction:
1. **Payment Status (PAY_1)** - Most recent payment history
2. **Credit Limit** - Customer credit capacity
3. **Age** - Demographics
4. **Repay Amount** - Customer payment behavior
5. **Bill Amount** - Credit utilization

### Class Imbalance Handling
- **Before SMOTE:** 3.5:1 imbalance (model biased toward non-default)
- **After SMOTE:** 1:1 balanced (improved minority class recall)
- **Result:** Recall improved from ~0.45 to ~0.82 (CatBoost)

### Model Comparison
- **CatBoost:** Best for maximizing default detection (high recall)
- **LightGBM:** Better for balanced precision-recall (lower false alarms)

---

## 💼 Business Application

### Use Cases

1. **Credit Card Approval Decision**
   - Use LightGBM (balanced strategy) for new applicants
   - Threshold 0.50 balances risk and business cost

2. **High-Risk Customer Identification**
   - Use CatBoost (conservative strategy) for existing customers
   - Threshold 0.35 catches potential defaulters early
   - Lower cost of prevention vs collection

3. **Credit Limit Adjustment**
   - Risk score helps determine credit limit adjustments
   - Higher risk → lower credit limit

### Expected Business Impact
- **Prevent Losses:** Catch ~82% of defaulters with CatBoost
- **Minimize False Alarms:** ~47% precision (cost ₹2,000 per false alarm)
- **Total Business Cost:** Optimized by threshold selection

---

## 🛠️ Development & Customization

### Retraining Models
```bash
cd streamlit_app
python train_export.py
```
This will:
- Load raw data from `Credit_Card_Default.csv`
- Preprocess & balance data
- Train both models with GridSearchCV
- Export model artifacts to `data/` directory
- Update all .pkl files

### Modifying Streamlit Dashboard
- Edit pages in `streamlit_app/pages/` directory
- Changes auto-reload when files are saved
- Restart server with `Ctrl+C` then `streamlit run app.py` if needed

### Hyperparameter Tuning
Edit `train_export.py` to modify:
- GridSearchCV parameter grids
- Cross-validation folds
- Scoring metrics

---

## 📝 Known Issues & Fixes

### ✅ Issue #1: Page Navigation
**Status:** Fixed
- Pages renamed to remove emoji from filenames
- Streamlit requires `number_name.py` format
- Emoji still display in UI via `page_icon` config

### ✅ Issue #2: SHAP Visualization Error
**Status:** Fixed
- Resolved Plotly `yaxis` duplicate parameter error
- Corrected layout dictionary merging in Page 6

---

## 🔐 Security Notes

- **No API Keys/Credentials:** All code is safe to share
- **Secrets:** Place sensitive configs in `.streamlit/secrets.toml` (excluded by .gitignore)
- **Data Privacy:** Synthetic SMOTE data - no real customer PII leaked

---

## 📚 References & Resources

**Datasets:**
- [UCI ML Repository - Taiwan Credit Card Dataset](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients)

**Libraries Documentation:**
- [Streamlit Docs](https://docs.streamlit.io/)
- [SHAP GitHub](https://github.com/shap/shap)
- [CatBoost Docs](https://catboost.ai/docs/)
- [LightGBM Docs](https://lightgbm.readthedocs.io/)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👥 Author

**Khushboo Rai**  
Data Science & Machine Learning  
GitHub: [@rkhushboo](https://github.com/rkhushboo)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## ⭐ Acknowledgments

- Dataset: UCI Machine Learning Repository
- Frameworks: Scikit-learn, CatBoost, LightGBM, SHAP
- Dashboard: Streamlit community
- Special thanks to everyone who uses or contributes to this project!

---

## 📞 Support & Questions

For questions or issues:
- Open an issue on GitHub
- Check existing documentation in this README
- Review Streamlit app pages for feature explanations

---

## 🎓 Learning Resources

This project demonstrates:
- ✅ Class imbalance handling (SMOTE)
- ✅ Hyperparameter tuning (GridSearchCV)
- ✅ Threshold optimization with business costs
- ✅ Model explainability (SHAP)
- ✅ Interactive dashboards (Streamlit)
- ✅ Production-ready code structure

Perfect for learning or portfolio building!

---

**Last Updated:** May 11, 2026  
**Status:** ✅ Production Ready
