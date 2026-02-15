"""
Train a real XGBoost churn prediction model

This script:
1. Downloads Telco Customer Churn dataset from Kaggle
2. Preprocesses the data
3. Trains an XGBoost model
4. Saves the model for production use
5. Evaluates model performance

Requirements:
    pip install xgboost scikit-learn pandas numpy joblib kaggle

Usage:
    python train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb
import joblib
import os


def download_dataset():
    """
    Download Telco Customer Churn dataset from Kaggle
    
    Note: You need to set up Kaggle API credentials first:
    1. Go to https://www.kaggle.com/account
    2. Create API token (downloads kaggle.json)
    3. Place kaggle.json in ~/.kaggle/
    
    Or manually download from:
    https://www.kaggle.com/datasets/blastchar/telco-customer-churn
    """
    print("📥 Downloading dataset...")
    
    # Check if dataset already exists
    if os.path.exists('data/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
        print("✅ Dataset already exists")
        return
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    try:
        # Download using Kaggle API
        os.system('kaggle datasets download -d blastchar/telco-customer-churn -p data/ --unzip')
        print("✅ Dataset downloaded successfully")
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\n📝 Manual download instructions:")
        print("1. Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
        print("2. Download the dataset")
        print("3. Extract to: aura-backend/data/")
        raise


def load_and_preprocess_data():
    """
    Load and preprocess the Telco churn dataset
    
    Returns:
        X: Feature matrix
        y: Target variable (churn)
        feature_names: List of feature names
    """
    print("\n🔄 Loading and preprocessing data...")
    
    # Load dataset
    df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Churn rate: {df['Churn'].value_counts(normalize=True)['Yes']:.2%}")
    
    # Handle missing values
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    
    # Drop customerID (not a feature)
    df = df.drop('customerID', axis=1)
    
    # Encode target variable
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Save label encoders for later use
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    # Separate features and target
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    feature_names = X.columns.tolist()
    
    print(f"✅ Preprocessing complete")
    print(f"Features: {len(feature_names)}")
    print(f"Samples: {len(X)}")
    
    return X, y, feature_names


def train_xgboost_model(X, y, feature_names):
    """
    Train XGBoost model with hyperparameter tuning
    
    Args:
        X: Feature matrix
        y: Target variable
        feature_names: List of feature names
        
    Returns:
        model: Trained XGBoost model
        X_test: Test features
        y_test: Test labels
    """
    print("\n🎯 Training XGBoost model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # XGBoost parameters
    params = {
        'objective': 'binary:logistic',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'gamma': 1,
        'reg_alpha': 0.1,
        'reg_lambda': 1,
        'random_state': 42,
        'eval_metric': 'auc'
    }
    
    # Train model
    model = xgb.XGBClassifier(**params)
    
    model.fit(
        X_train_scaled, y_train,
        eval_set=[(X_test_scaled, y_test)],
        verbose=True
    )
    
    print("✅ Model training complete")
    
    return model, X_test_scaled, y_test, scaler


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
    """
    print("\n📊 Evaluating model...")
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n📈 Model Performance:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  ROC AUC:   {auc:.4f}")
    
    # Feature importance
    print(f"\n🔝 Top 10 Important Features:")
    feature_importance = pd.DataFrame({
        'feature': model.get_booster().feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc
    }


def save_model(model, metrics):
    """
    Save trained model and metadata
    
    Args:
        model: Trained model
        metrics: Performance metrics
    """
    print("\n💾 Saving model...")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model.save_model('models/churn_model.json')
    joblib.dump(model, 'models/churn_model.pkl')
    
    # Save metrics
    joblib.dump(metrics, 'models/model_metrics.pkl')
    
    print("✅ Model saved to models/churn_model.pkl")
    print("✅ Metrics saved to models/model_metrics.pkl")


def create_feature_mapping():
    """
    Create mapping between our database features and model features
    
    This helps translate our customer data to model input format
    """
    mapping = {
        'tenure': 'tenure',
        'monthly_charge': 'MonthlyCharges',
        'data_usage_gb': 'InternetService',  # Proxy
        'voice_minutes': 'PhoneService',  # Proxy
        'complaint_count': 'TechSupport',  # Proxy
        'support_calls_count': 'TechSupport',  # Proxy
        'payment_delays': 'PaymentMethod',  # Proxy
        'contract_type': 'Contract',
        'plan_type': 'InternetService'  # Proxy
    }
    
    joblib.dump(mapping, 'models/feature_mapping.pkl')
    print("✅ Feature mapping saved")


def main():
    """Main training pipeline"""
    print("🚀 Starting ML Model Training Pipeline\n")
    print("=" * 60)
    
    try:
        # Step 1: Download dataset
        download_dataset()
        
        # Step 2: Load and preprocess
        X, y, feature_names = load_and_preprocess_data()
        
        # Step 3: Train model
        model, X_test, y_test, scaler = train_xgboost_model(X, y, feature_names)
        
        # Step 4: Evaluate
        metrics = evaluate_model(model, X_test, y_test)
        
        # Step 5: Save model
        save_model(model, metrics)
        
        # Step 6: Create feature mapping
        create_feature_mapping()
        
        print("\n" + "=" * 60)
        print("✅ Training pipeline completed successfully!")
        print("\n📝 Next steps:")
        print("1. Update ChurnPredictor to load the trained model")
        print("2. Update ShapExplainer to use real SHAP values")
        print("3. Test the model with real customer data")
        
    except Exception as e:
        print(f"\n❌ Error in training pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
