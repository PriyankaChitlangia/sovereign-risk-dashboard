import pandas as pd
import numpy as np
import os
import joblib
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, classification_report, roc_curve

DATA_FILE = "data/processed_data.csv"
MODEL_DIR = "models"
OUTPUT_PRED_FILE = "data/predictions.csv"

def load_data():
    print("Loading data...")
    df = pd.read_csv(DATA_FILE)
    return df

def preprocess_and_split(df):
    print("Preprocessing and splitting data...")
    
    # Identify features
    exclude_cols = ['ISO', 'Country', 'Year', 'Crisis_Next_3_Years']
    features = [c for c in df.columns if c not in exclude_cols]
    
    # Train/Test Split (Time-based: Train 2001-2018, Test 2019-2023)
    train_df = df[df['Year'] <= 2018].copy()
    test_df = df[(df['Year'] >= 2019) & (df['Year'] <= 2023)].copy()
    
    X_train = train_df[features]
    y_train = train_df['Crisis_Next_3_Years']
    
    X_test = test_df[features]
    y_test = test_df['Crisis_Next_3_Years']
    
    # Impute missing values
    print("Imputing missing values...")
    imputer = IterativeImputer(random_state=42, max_iter=10)
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)
    
    # Clip outliers (1st and 99th percentiles) based on training data
    print("Clipping outliers...")
    lower_bounds = np.percentile(X_train_imputed, 1, axis=0)
    upper_bounds = np.percentile(X_train_imputed, 99, axis=0)
    
    X_train_imputed = np.clip(X_train_imputed, lower_bounds, upper_bounds)
    X_test_imputed = np.clip(X_test_imputed, lower_bounds, upper_bounds)
    
    # Scale features robustly
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, train_df, test_df, imputer, scaler, features, lower_bounds, upper_bounds

def train_models(X_train, y_train):
    print("Training Logistic Regression...")
    lr = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
    lr.fit(X_train, y_train)
    
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(random_state=42, n_estimators=100)
    gb.fit(X_train, y_train)
    
    return lr, gb

def evaluate_models(lr, gb, X_test, y_test):
    print("\n--- Evaluation ---")
    
    # Predict probabilities
    lr_probs = lr.predict_proba(X_test)[:, 1]
    gb_probs = gb.predict_proba(X_test)[:, 1]
    
    # Ensemble (average)
    ensemble_probs = (lr_probs + gb_probs) / 2
    
    # AUC
    print(f"LR ROC-AUC: {roc_auc_score(y_test, lr_probs):.4f}")
    print(f"GB ROC-AUC: {roc_auc_score(y_test, gb_probs):.4f}")
    print(f"Ensemble ROC-AUC: {roc_auc_score(y_test, ensemble_probs):.4f}")
    
    # Classify based on thresholds
    # > 0.6 is High Risk (Class 1)
    ensemble_preds = (ensemble_probs > 0.5).astype(int)
    print("\nClassification Report (Ensemble Threshold > 0.5):")
    print(classification_report(y_test, ensemble_preds))
    
    return ensemble_probs

def save_artifacts(df, imputer, scaler, lr, gb, features, test_df, ensemble_probs, lower_bounds, upper_bounds):
    print(f"Saving models to {MODEL_DIR}...")
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    joblib.dump(imputer, os.path.join(MODEL_DIR, "imputer.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(lr, os.path.join(MODEL_DIR, "lr_model.pkl"))
    joblib.dump(gb, os.path.join(MODEL_DIR, "gb_model.pkl"))
    joblib.dump(features, os.path.join(MODEL_DIR, "features.pkl"))
    joblib.dump({'lower': lower_bounds, 'upper': upper_bounds}, os.path.join(MODEL_DIR, "clip_bounds.pkl"))
    
    # Save predictions
    # Impute and score the ENTIRE dataset so the dashboard can use it
    X_all = df[features]
    X_all_imputed = imputer.transform(X_all)
    X_all_imputed = np.clip(X_all_imputed, lower_bounds, upper_bounds)
    X_all_scaled = scaler.transform(X_all_imputed)
    
    df['LR_Prob'] = lr.predict_proba(X_all_scaled)[:, 1]
    df['GB_Prob'] = gb.predict_proba(X_all_scaled)[:, 1]
    df['Ensemble_Prob'] = (df['LR_Prob'] + df['GB_Prob']) / 2
    
    def get_risk_level(prob):
        if prob < 0.2: return "Low"
        elif prob < 0.4: return "Mild Low"
        elif prob < 0.6: return "Moderate"
        elif prob < 0.8: return "High"
        else: return "Extreme"
        
    df['Risk_Level'] = df['Ensemble_Prob'].apply(get_risk_level)
    
    df.to_csv(OUTPUT_PRED_FILE, index=False)
    print(f"Predictions saved to {OUTPUT_PRED_FILE}")

def main():
    df = load_data()
    X_train, X_test, y_train, y_test, train_df, test_df, imputer, scaler, features, lower_bounds, upper_bounds = preprocess_and_split(df)
    lr, gb = train_models(X_train, y_train)
    ensemble_probs = evaluate_models(lr, gb, X_test, y_test)
    save_artifacts(df, imputer, scaler, lr, gb, features, test_df, ensemble_probs, lower_bounds, upper_bounds)

if __name__ == "__main__":
    main()
