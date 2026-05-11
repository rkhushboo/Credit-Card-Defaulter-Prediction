import os
import time
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from statsmodels.stats.outliers_influence import variance_inflation_factor
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = ROOT.parent / "Credit_Card_Default.csv"

MODEL_CONFIGS = {
    "CatBoost": {
        "model": CatBoostClassifier(verbose=0, random_state=42),
        "param_grid": {
            "iterations": [100, 200],
            "learning_rate": [0.03, 0.05, 0.1],
            "depth": [4, 5, 6]
        }
    },
    "LightGBM": {
        "model": LGBMClassifier(random_state=42),
        "param_grid": {
            "n_estimators": [100, 150, 200],
            "learning_rate": [0.03, 0.05, 0.1],
            "max_depth": [4, 5, 6]
        }
    }
}

THRESHOLDS = np.arange(0.10, 0.91, 0.05)


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def cap_outliers(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "default.payment.next.month" in numeric_cols:
        numeric_cols.remove("default.payment.next.month")
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    return df


def drop_high_vif_cols(df: pd.DataFrame) -> pd.DataFrame:
    features = df.drop(columns=["default.payment.next.month"])
    feature_cols = features.columns
    X = features.values
    vif_df = pd.DataFrame({
        "Feature": feature_cols,
        "VIF": [variance_inflation_factor(X, i) for i in range(X.shape[1])]
    }).sort_values("VIF", ascending=False)
    cols_to_drop = [col for col in ["BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"] if col in df.columns]
    return df.drop(columns=cols_to_drop), vif_df


def preprocess_features(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "default.payment.next.month" in numeric_cols:
        numeric_cols.remove("default.payment.next.month")
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df, scaler


def train_test_split_data(df: pd.DataFrame):
    X = df.drop(columns=["default.payment.next.month"])
    y = df["default.payment.next.month"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test


def balance_training_data(X_train, y_train):
    smote = SMOTE(random_state=42)
    return smote.fit_resample(X_train, y_train)


def tune_model(name: str, estimator, param_grid, X, y):
    grid = GridSearchCV(
        estimator=estimator,
        param_grid=param_grid,
        scoring='roc_auc',
        cv=5,
        n_jobs=-1,
        verbose=1,
        return_train_score=True
    )
    grid.fit(X, y)
    return grid.best_estimator_, grid.best_params_, grid.best_score_


def evaluate_model(estimator, X_test, y_test):
    y_pred = estimator.predict(X_test)
    y_probs = estimator.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_probs)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return {
        "roc_auc": roc_auc,
        "recall": recall,
        "precision": precision,
        "f1": f1,
        "y_pred": y_pred,
        "y_probs": y_probs
    }


def threshold_analysis(y_test, y_probs):
    records = []
    for threshold in THRESHOLDS:
        y_pred = (y_probs >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        total_cost = fn * 10000 + fp * 2000
        recall = recall_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        records.append({
            "threshold": threshold,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "recall": recall,
            "precision": precision,
            "f1": f1,
            "total_cost": total_cost
        })
    return pd.DataFrame(records)


def save_artifacts(artifacts: dict):
    for name, obj in artifacts.items():
        path = DATA_DIR / f"{name}.pkl"
        joblib.dump(obj, path)
        print(f"Saved {name} to {path}")


def main():
    print("Loading data...")
    df = load_data(CSV_PATH)
    print(f"Dataset shape: {df.shape}")

    df = cap_outliers(df)
    df, vif_df = drop_high_vif_cols(df)
    df, scaler = preprocess_features(df)

    X_train, X_test, y_train, y_test = train_test_split_data(df)
    X_train_res, y_train_res = balance_training_data(X_train, y_train)

    artifacts = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_res": X_train_res,
        "y_train_res": y_train_res,
        "scaler": scaler,
        "vif_df": vif_df,
    }
    save_artifacts(artifacts)

    tuned_results = []
    best_models = {}

    for model_name, config in MODEL_CONFIGS.items():
        print(f"Tuning {model_name}...")
        estimator = config["model"]
        best_estimator, best_params, best_score = tune_model(
            model_name,
            estimator,
            config["param_grid"],
            X_train_res,
            y_train_res
        )
        print(f"Best params for {model_name}: {best_params}")
        best_models[model_name] = best_estimator
        metrics = evaluate_model(best_estimator, X_test, y_test)
        tuned_results.append({
            "model": model_name,
            "best_params": best_params,
            "cv_roc_auc": best_score,
            "test_roc_auc": metrics["roc_auc"],
            "test_recall": metrics["recall"],
            "test_precision": metrics["precision"],
            "test_f1": metrics["f1"]
        })
        print(f"Test ROC-AUC for {model_name}: {metrics['roc_auc']:.4f}")

        thresholds_df = threshold_analysis(y_test, metrics["y_probs"])
        save_artifacts({f"thresholds_{model_name.lower()}": thresholds_df})

    # Save best models
    save_artifacts({
        "catboost_model": best_models["CatBoost"],
        "lightgbm_model": best_models["LightGBM"],
        "metrics": pd.DataFrame(tuned_results)
    })

    print("Training complete. All artifacts saved.")


if __name__ == "__main__":
    main()
