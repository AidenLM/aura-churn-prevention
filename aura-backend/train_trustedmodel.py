"""
TrustedModel Yaklaşımı ile Telco Customer Churn Prediction
Tam olarak TrustedModel notebook'unu takip ediyoruz
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

# Models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier

print("=" * 80)
print("TRUSTEDMODEL YAKLAŞIMI - TELCO CUSTOMER CHURN PREDICTION")
print("=" * 80)

# 1. Load Data
print("\n1. Loading data...")
df = pd.read_csv('TrustedModel/WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# 2. Data Exploration
print("\n2. Data Exploration...")
print(f"\nFirst 5 rows:")
print(df.head())

print(f"\nData types:")
print(df.dtypes)

print(f"\nMissing values:")
print(df.isnull().sum())

print(f"\nChurn distribution:")
print(df['Churn'].value_counts())
print(f"Churn rate: {df['Churn'].value_counts(normalize=True)['Yes']:.2%}")

# 3. Data Cleaning
print("\n3. Data Cleaning...")

# TotalCharges'ı numeric'e çevir (boşluklar var)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Missing values'ları doldur
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

print(f"Missing values after cleaning: {df.isnull().sum().sum()}")

# 4. Feature Engineering
print("\n4. Feature Engineering...")

# Churn'ü binary'ye çevir
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# customerID'yi drop et (unique identifier, model için gereksiz)
df_model = df.drop('customerID', axis=1)

print(f"Features after engineering: {df_model.shape[1]}")

# 5. Encoding Categorical Variables
print("\n5. Encoding Categorical Variables...")

# Kategorik kolonları bul
categorical_cols = df_model.select_dtypes(include=['object']).columns.tolist()
print(f"Categorical columns: {categorical_cols}")

# Label Encoding
le = LabelEncoder()
for col in categorical_cols:
    df_model[col] = le.fit_transform(df_model[col])

print("Encoding completed!")

# 6. Feature Scaling
print("\n6. Feature Scaling...")

# Numerik kolonlar
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']

# StandardScaler
scaler = StandardScaler()
df_model[numeric_cols] = scaler.fit_transform(df_model[numeric_cols])

print("Scaling completed!")

# 7. Train/Test Split
print("\n7. Train/Test Split...")

X = df_model.drop('Churn', axis=1)
y = df_model['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=40, stratify=y
)

print(f"Train set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# 8. Model Training
print("\n" + "=" * 80)
print("8. MODEL TRAINING")
print("=" * 80)

models = {}
results = {}

# 8.1 KNN
print("\n8.1 Training KNN...")
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
models['KNN'] = knn
results['KNN'] = {
    'accuracy': accuracy_score(y_test, y_pred_knn),
    'precision': precision_score(y_test, y_pred_knn),
    'recall': recall_score(y_test, y_pred_knn),
    'f1': f1_score(y_test, y_pred_knn)
}
print(f"KNN Accuracy: {results['KNN']['accuracy']:.4f}")

# 8.2 SVM
print("\n8.2 Training SVM...")
svm = SVC(random_state=1, probability=True)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
models['SVM'] = svm
results['SVM'] = {
    'accuracy': accuracy_score(y_test, y_pred_svm),
    'precision': precision_score(y_test, y_pred_svm),
    'recall': recall_score(y_test, y_pred_svm),
    'f1': f1_score(y_test, y_pred_svm)
}
print(f"SVM Accuracy: {results['SVM']['accuracy']:.4f}")

# 8.3 Random Forest
print("\n8.3 Training Random Forest...")
rf = RandomForestClassifier(
    n_estimators=500,
    oob_score=True,
    n_jobs=-1,
    random_state=50,
    max_features="sqrt",
    max_leaf_nodes=30
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
models['Random Forest'] = rf
results['Random Forest'] = {
    'accuracy': accuracy_score(y_test, y_pred_rf),
    'precision': precision_score(y_test, y_pred_rf),
    'recall': recall_score(y_test, y_pred_rf),
    'f1': f1_score(y_test, y_pred_rf)
}
print(f"Random Forest Accuracy: {results['Random Forest']['accuracy']:.4f}")

# 8.4 Logistic Regression
print("\n8.4 Training Logistic Regression...")
lr = LogisticRegression(random_state=1, max_iter=1000)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
models['Logistic Regression'] = lr
results['Logistic Regression'] = {
    'accuracy': accuracy_score(y_test, y_pred_lr),
    'precision': precision_score(y_test, y_pred_lr),
    'recall': recall_score(y_test, y_pred_lr),
    'f1': f1_score(y_test, y_pred_lr)
}
print(f"Logistic Regression Accuracy: {results['Logistic Regression']['accuracy']:.4f}")

# 8.5 Decision Tree
print("\n8.5 Training Decision Tree...")
dt = DecisionTreeClassifier(random_state=1)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
models['Decision Tree'] = dt
results['Decision Tree'] = {
    'accuracy': accuracy_score(y_test, y_pred_dt),
    'precision': precision_score(y_test, y_pred_dt),
    'recall': recall_score(y_test, y_pred_dt),
    'f1': f1_score(y_test, y_pred_dt)
}
print(f"Decision Tree Accuracy: {results['Decision Tree']['accuracy']:.4f}")

# 8.6 AdaBoost
print("\n8.6 Training AdaBoost...")
ada = AdaBoostClassifier(random_state=1)
ada.fit(X_train, y_train)
y_pred_ada = ada.predict(X_test)
models['AdaBoost'] = ada
results['AdaBoost'] = {
    'accuracy': accuracy_score(y_test, y_pred_ada),
    'precision': precision_score(y_test, y_pred_ada),
    'recall': recall_score(y_test, y_pred_ada),
    'f1': f1_score(y_test, y_pred_ada)
}
print(f"AdaBoost Accuracy: {results['AdaBoost']['accuracy']:.4f}")

# 8.7 Gradient Boosting
print("\n8.7 Training Gradient Boosting...")
gb = GradientBoostingClassifier(random_state=1)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
models['Gradient Boosting'] = gb
results['Gradient Boosting'] = {
    'accuracy': accuracy_score(y_test, y_pred_gb),
    'precision': precision_score(y_test, y_pred_gb),
    'recall': recall_score(y_test, y_pred_gb),
    'f1': f1_score(y_test, y_pred_gb)
}
print(f"Gradient Boosting Accuracy: {results['Gradient Boosting']['accuracy']:.4f}")

# 8.8 Voting Classifier (Ensemble)
print("\n8.8 Training Voting Classifier (Ensemble)...")
voting = VotingClassifier(
    estimators=[
        ('rf', rf),
        ('gb', gb),
        ('lr', lr)
    ],
    voting='soft'
)
voting.fit(X_train, y_train)
y_pred_voting = voting.predict(X_test)
models['Voting Classifier'] = voting
results['Voting Classifier'] = {
    'accuracy': accuracy_score(y_test, y_pred_voting),
    'precision': precision_score(y_test, y_pred_voting),
    'recall': recall_score(y_test, y_pred_voting),
    'f1': f1_score(y_test, y_pred_voting)
}
print(f"Voting Classifier Accuracy: {results['Voting Classifier']['accuracy']:.4f}")

# 9. Results Summary
print("\n" + "=" * 80)
print("9. RESULTS SUMMARY")
print("=" * 80)

results_df = pd.DataFrame(results).T
results_df = results_df.sort_values('accuracy', ascending=False)

print("\n📊 Model Performance Comparison:")
print(results_df.to_string())

# Best model
best_model_name = results_df.index[0]
best_model = models[best_model_name]
best_accuracy = results_df.iloc[0]['accuracy']

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   Accuracy: {best_accuracy:.4f}")
print(f"   Precision: {results_df.iloc[0]['precision']:.4f}")
print(f"   Recall: {results_df.iloc[0]['recall']:.4f}")
print(f"   F1-Score: {results_df.iloc[0]['f1']:.4f}")

# 10. Detailed Evaluation of Best Model
print("\n" + "=" * 80)
print(f"10. DETAILED EVALUATION - {best_model_name}")
print("=" * 80)

y_pred_best = best_model.predict(X_test)
y_pred_proba_best = best_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred_best))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_best)
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"\nTrue Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives: {tp}")

# ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba_best)
print(f"\nROC-AUC Score: {roc_auc:.4f}")

# 11. Save Models
print("\n" + "=" * 80)
print("11. SAVING MODELS")
print("=" * 80)

import pickle
import os

# Create models directory
os.makedirs('models', exist_ok=True)

# Save best model
with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print(f"✅ Best model ({best_model_name}) saved to models/best_model.pkl")

# Save scaler
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✅ Scaler saved to models/scaler.pkl")

# Save feature names
feature_names = X.columns.tolist()
with open('models/feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f)
print("✅ Feature names saved to models/feature_names.pkl")

# Save model metadata
metadata = {
    'model_name': best_model_name,
    'accuracy': float(best_accuracy),
    'precision': float(results_df.iloc[0]['precision']),
    'recall': float(results_df.iloc[0]['recall']),
    'f1_score': float(results_df.iloc[0]['f1']),
    'roc_auc': float(roc_auc),
    'features': feature_names,
    'n_features': len(feature_names),
    'train_size': len(X_train),
    'test_size': len(X_test)
}

import json
with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("✅ Model metadata saved to models/model_metadata.json")

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 80)
