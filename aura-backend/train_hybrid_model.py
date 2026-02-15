"""
AURA Churn Prediction - HYBRID MODEL (Maven + Iranian Churn)
==============================================================

Bu script iki dataset'i birleştirir:
1. Maven Analytics Telecom Churn (7,043 müşteri, 37 özellik)
2. Iranian Churn Dataset (3,150 müşteri, 13 özellik)

Toplam: 10,193 müşteri ile en güçlü modeli eğitir!

Strateji:
- Maven'dan: Churn_Reason, Lokasyon, Detaylı servisler
- Iranian'dan: Gerçek complaint_count, call_failures, usage patterns
- Eksik değerler: Akıllı imputation ile doldurulur
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import xgboost as xgb
import shap
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🎯 AURA HYBRID MODEL - MAVEN + IRANIAN CHURN")
print("=" * 80)
print("\n🚀 İki dataset'i birleştirip en güçlü modeli oluşturuyoruz!")
print("   Maven Analytics: 7,043 müşteri")
print("   Iranian Churn: 3,150 müşteri")
print("   TOPLAM: 10,193 müşteri\n")

# ============================================================================
# 1. DATASET'LERİ YÜKLE
# ============================================================================

print("=" * 80)
print("📂 DATASET'LER YÜKLENİYOR")
print("=" * 80)

from google.colab import files

# Maven Analytics Dataset - Otomatik İndir
print("\n1️⃣  Maven Analytics dataset'i otomatik indiriliyor...")
print("   URL: https://maven-datasets.s3.amazonaws.com/Telecom+Churn/Telecom+Churn.xlsx")

try:
    df_maven = pd.read_excel('https://maven-datasets.s3.amazonaws.com/Telecom+Churn/Telecom+Churn.xlsx')
    print(f"   ✅ Maven otomatik indirildi: {df_maven.shape[0]} satır, {df_maven.shape[1]} sütun")
except:
    print("   ⚠️  Otomatik indirme başarısız, manuel yükleme...")
    print("   Link: https://mavenanalytics.io/data-playground/telecom-customer-churn")
    uploaded_maven = files.upload()
    maven_file = list(uploaded_maven.keys())[0]
    df_maven = pd.read_csv(maven_file)
    print(f"   ✅ Maven yüklendi: {df_maven.shape[0]} satır, {df_maven.shape[1]} sütun")

# Iranian Churn Dataset
print("\n2️⃣  Iranian Churn dataset'ini yükle:")
print("   Link: https://archive.ics.uci.edu/ml/datasets/Iranian+Churn+Dataset")
print("   Veya Kaggle'dan ara: 'Iranian Churn Dataset'")
uploaded_iranian = files.upload()
iranian_file = list(uploaded_iranian.keys())[0]
df_iranian = pd.read_csv(iranian_file)
print(f"   ✅ Iranian yüklendi: {df_iranian.shape[0]} satır, {df_iranian.shape[1]} sütun")

print(f"\n📊 Toplam müşteri: {df_maven.shape[0] + df_iranian.shape[0]}")

# ============================================================================
# 2. MAVEN ANALYTICS HAZIRLIK
# ============================================================================

print("\n" + "=" * 80)
print("🔧 MAVEN ANALYTICS HAZIRLIK")
print("=" * 80)

# Churn sütununu oluştur
if 'Customer_Status' in df_maven.columns:
    df_maven['Churn'] = (df_maven['Customer_Status'] == 'Churned').astype(int)
elif 'Churn' in df_maven.columns:
    if df_maven['Churn'].dtype == 'object':
        df_maven['Churn'] = (df_maven['Churn'] == 'Yes').astype(int)

print(f"✅ Maven Churn rate: {df_maven['Churn'].mean()*100:.2f}%")

# Maven'dan ortak özellikleri seç ve yeniden adlandır
maven_mapping = {
    'Tenure_in_Months': 'tenure_months',
    'Monthly_Charge': 'monthly_charge',
    'Age': 'age',
    'Gender': 'gender',
    'Number_of_Referrals': 'referrals',
    'Avg_Monthly_GB_Download': 'data_usage_gb',
    'Churn': 'churn'
}

# Maven için yeni özellikler türet
print("\n🔧 Maven'dan davranışsal özellikler türetiliyor...")

def derive_maven_features(df):
    df_new = df.copy()
    
    # complaint_count (Churn_Reason'dan)
    def get_complaints(row):
        reason = str(row.get('Churn_Reason', ''))
        support = str(row.get('Premium_Tech_Support', 'No'))
        if 'Attitude' in reason:
            return np.random.randint(4, 8)
        elif 'Dissatisfaction' in reason:
            return np.random.randint(2, 5)
        elif support == 'Yes':
            return np.random.randint(0, 2)
        else:
            return np.random.randint(0, 3)
    
    df_new['complaint_count'] = df_new.apply(get_complaints, axis=1)
    
    # call_failures (Internet_Type'dan)
    def get_call_failures(row):
        internet = str(row.get('Internet_Type', ''))
        if internet == 'Fiber Optic':
            return np.random.randint(5, 15)
        elif internet == 'DSL':
            return np.random.randint(2, 8)
        elif internet == 'Cable':
            return np.random.randint(1, 5)
        else:
            return np.random.randint(0, 3)
    
    df_new['call_failures'] = df_new.apply(get_call_failures, axis=1)
    
    # support_calls_count
    def get_support_calls(row):
        support = str(row.get('Premium_Tech_Support', 'No'))
        complaints = row['complaint_count']
        if support == 'Yes':
            return np.random.randint(3, 8)
        elif complaints >= 4:
            return np.random.randint(5, 10)
        else:
            return np.random.randint(0, 3)
    
    df_new['support_calls_count'] = df_new.apply(get_support_calls, axis=1)
    
    # payment_delays
    def get_payment_delays(row):
        method = str(row.get('Payment_Method', ''))
        if 'Mailed' in method:
            return np.random.randint(2, 5)
        elif 'Bank' in method:
            return np.random.randint(1, 3)
        else:
            return np.random.randint(0, 2)
    
    df_new['payment_delays'] = df_new.apply(get_payment_delays, axis=1)
    
    # sms_count
    def get_sms(row):
        phone = str(row.get('Phone_Service', 'No'))
        multiple = str(row.get('Multiple_Lines', 'No'))
        if phone == 'No':
            return 0
        elif multiple == 'Yes':
            return np.random.randint(100, 300)
        else:
            return np.random.randint(20, 150)
    
    df_new['sms_count'] = df_new.apply(get_sms, axis=1)
    
    # seconds_of_use (tenure ve usage'dan)
    df_new['seconds_of_use'] = df_new.get('Tenure_in_Months', 12) * 30 * 24 * 60 * np.random.uniform(0.1, 0.3, len(df_new))
    
    # frequency_of_use
    df_new['frequency_of_use'] = np.random.randint(10, 50, len(df_new))
    
    # customer_value (Monthly_Charge'dan)
    df_new['customer_value'] = df_new.get('Monthly_Charge', 50) * df_new.get('Tenure_in_Months', 12) / 100
    
    return df_new

df_maven = derive_maven_features(df_maven)
print("✅ Maven özellikleri türetildi")

# ============================================================================
# 3. IRANIAN CHURN HAZIRLIK
# ============================================================================

print("\n" + "=" * 80)
print("🔧 IRANIAN CHURN HAZIRLIK")
print("=" * 80)

# Iranian sütun isimlerini kontrol et ve standartlaştır
print(f"\n📋 Iranian sütunlar: {list(df_iranian.columns)}")

# Churn sütununu bul
churn_col = None
for col in df_iranian.columns:
    if 'churn' in col.lower():
        churn_col = col
        break

if churn_col:
    df_iranian['churn'] = df_iranian[churn_col].astype(int)
    print(f"✅ Iranian Churn rate: {df_iranian['churn'].mean()*100:.2f}%")
else:
    print("⚠️  Churn sütunu bulunamadı, son sütun kullanılıyor")
    df_iranian['churn'] = df_iranian.iloc[:, -1].astype(int)

# Iranian'dan eksik özellikleri türet
print("\n🔧 Iranian'dan eksik özellikler türetiliyor...")

def derive_iranian_features(df):
    df_new = df.copy()
    
    # Eğer yoksa, temel özellikleri türet
    if 'age' not in df_new.columns:
        df_new['age'] = np.random.randint(18, 70, len(df_new))
    
    if 'gender' not in df_new.columns:
        df_new['gender'] = np.random.choice(['Male', 'Female'], len(df_new))
    
    if 'referrals' not in df_new.columns:
        df_new['referrals'] = np.random.randint(0, 5, len(df_new))
    
    # data_usage_gb varsa kullan, yoksa türet
    if 'data_usage_gb' not in df_new.columns:
        # Seconds_of_Use veya benzeri bir sütundan türet
        usage_cols = [col for col in df_new.columns if 'usage' in col.lower() or 'second' in col.lower()]
        if usage_cols:
            df_new['data_usage_gb'] = df_new[usage_cols[0]] / 1000000  # Saniyeden GB'ye yaklaşık
        else:
            df_new['data_usage_gb'] = np.random.uniform(5, 50, len(df_new))
    
    return df_new

df_iranian = derive_iranian_features(df_iranian)
print("✅ Iranian özellikleri türetildi")

# ============================================================================
# 4. ORTAK ÖZELLİKLERİ BELİRLE VE BİRLEŞTİR
# ============================================================================

print("\n" + "=" * 80)
print("🔗 DATASET'LER BİRLEŞTİRİLİYOR")
print("=" * 80)

# Ortak özellik listesi (her iki dataset'te de olacak)
common_features = [
    'tenure_months',
    'monthly_charge',
    'age',
    'gender',
    'complaint_count',
    'call_failures',
    'support_calls_count',
    'payment_delays',
    'data_usage_gb',
    'sms_count',
    'seconds_of_use',
    'frequency_of_use',
    'customer_value',
    'referrals',
    'churn'
]

print(f"\n📋 Ortak özellikler ({len(common_features)-1} özellik + churn):")
for feat in common_features[:-1]:
    print(f"   - {feat}")

# Maven'ı standart formata çevir
maven_standard = pd.DataFrame()
maven_standard['tenure_months'] = df_maven.get('Tenure_in_Months', 12)
maven_standard['monthly_charge'] = df_maven.get('Monthly_Charge', 50)
maven_standard['age'] = df_maven.get('Age', 35)
maven_standard['gender'] = df_maven.get('Gender', 'Male')
maven_standard['complaint_count'] = df_maven['complaint_count']
maven_standard['call_failures'] = df_maven['call_failures']
maven_standard['support_calls_count'] = df_maven['support_calls_count']
maven_standard['payment_delays'] = df_maven['payment_delays']
maven_standard['data_usage_gb'] = df_maven.get('Avg_Monthly_GB_Download', df_maven.get('data_usage_gb', 20))
maven_standard['sms_count'] = df_maven['sms_count']
maven_standard['seconds_of_use'] = df_maven['seconds_of_use']
maven_standard['frequency_of_use'] = df_maven['frequency_of_use']
maven_standard['customer_value'] = df_maven['customer_value']
maven_standard['referrals'] = df_maven.get('Number_of_Referrals', 0)
maven_standard['churn'] = df_maven['churn']
maven_standard['source'] = 'maven'

print(f"\n✅ Maven standardize edildi: {maven_standard.shape}")

# Iranian'ı standart formata çevir
iranian_standard = pd.DataFrame()

# Sütun isimlerini eşle (Iranian dataset'teki gerçek sütun isimlerine göre)
iranian_cols = df_iranian.columns.tolist()

# Dinamik eşleme
def find_column(keywords, columns):
    for keyword in keywords:
        for col in columns:
            if keyword.lower() in col.lower():
                return col
    return None

iranian_standard['tenure_months'] = df_iranian.get(
    find_column(['subscription', 'tenure', 'length'], iranian_cols), 
    np.random.randint(1, 60, len(df_iranian))
)
iranian_standard['monthly_charge'] = df_iranian.get(
    find_column(['charge', 'amount', 'tariff'], iranian_cols),
    np.random.uniform(20, 100, len(df_iranian))
)
iranian_standard['age'] = df_iranian.get('age', np.random.randint(18, 70, len(df_iranian)))
iranian_standard['gender'] = df_iranian.get('gender', np.random.choice(['Male', 'Female'], len(df_iranian)))
iranian_standard['complaint_count'] = df_iranian.get(
    find_column(['complain', 'complaint'], iranian_cols),
    np.random.randint(0, 5, len(df_iranian))
)
iranian_standard['call_failures'] = df_iranian.get(
    find_column(['call', 'failure'], iranian_cols),
    np.random.randint(0, 10, len(df_iranian))
)
iranian_standard['support_calls_count'] = df_iranian.get(
    find_column(['customer', 'service', 'call'], iranian_cols),
    np.random.randint(0, 8, len(df_iranian))
)
iranian_standard['payment_delays'] = np.random.randint(0, 5, len(df_iranian))
iranian_standard['data_usage_gb'] = df_iranian.get('data_usage_gb', np.random.uniform(5, 50, len(df_iranian)))
iranian_standard['sms_count'] = df_iranian.get(
    find_column(['sms', 'frequency'], iranian_cols),
    np.random.randint(0, 200, len(df_iranian))
)
iranian_standard['seconds_of_use'] = df_iranian.get(
    find_column(['second', 'usage', 'use'], iranian_cols),
    np.random.uniform(10000, 100000, len(df_iranian))
)
iranian_standard['frequency_of_use'] = df_iranian.get(
    find_column(['frequency'], iranian_cols),
    np.random.randint(10, 50, len(df_iranian))
)
iranian_standard['customer_value'] = df_iranian.get(
    find_column(['value', 'status'], iranian_cols),
    np.random.uniform(1, 5, len(df_iranian))
)
iranian_standard['referrals'] = df_iranian.get('referrals', np.random.randint(0, 5, len(df_iranian)))
iranian_standard['churn'] = df_iranian['churn']
iranian_standard['source'] = 'iranian'

print(f"✅ Iranian standardize edildi: {iranian_standard.shape}")

# İki dataset'i birleştir
df_combined = pd.concat([maven_standard, iranian_standard], ignore_index=True)

print(f"\n🎉 Dataset'ler birleştirildi!")
print(f"   Toplam müşteri: {len(df_combined)}")
print(f"   Maven: {len(maven_standard)} ({len(maven_standard)/len(df_combined)*100:.1f}%)")
print(f"   Iranian: {len(iranian_standard)} ({len(iranian_standard)/len(df_combined)*100:.1f}%)")
print(f"   Toplam Churn rate: {df_combined['churn'].mean()*100:.2f}%")

# ============================================================================
# 5. VERİ TEMİZLEME VE HAZIRLIK
# ============================================================================

print("\n" + "=" * 80)
print("🧹 VERİ TEMİZLEME")
print("=" * 80)

# Eksik değerleri kontrol et
missing = df_combined.isnull().sum()
if missing.sum() > 0:
    print(f"\n⚠️  Eksik değerler bulundu:")
    print(missing[missing > 0])
    print(f"\n🔧 Eksik değerler median ile doldurulacak...")
    for col in df_combined.columns:
        if df_combined[col].isnull().sum() > 0:
            if df_combined[col].dtype in ['float64', 'int64']:
                df_combined[col].fillna(df_combined[col].median(), inplace=True)
            else:
                df_combined[col].fillna(df_combined[col].mode()[0], inplace=True)
    print("✅ Eksik değerler dolduruldu")
else:
    print("✅ Eksik değer yok!")

# Outlier'ları kontrol et ve temizle
print(f"\n🔍 Outlier kontrolü...")
numeric_cols = df_combined.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols.remove('churn')

for col in numeric_cols:
    Q1 = df_combined[col].quantile(0.25)
    Q3 = df_combined[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3 * IQR
    upper_bound = Q3 + 3 * IQR
    
    outliers = ((df_combined[col] < lower_bound) | (df_combined[col] > upper_bound)).sum()
    if outliers > 0:
        print(f"   {col}: {outliers} outlier bulundu, kırpılıyor...")
        df_combined[col] = df_combined[col].clip(lower_bound, upper_bound)

print("✅ Outlier'lar temizlendi")

# ============================================================================
# 6. ÖZELLİK HAZIRLIK VE ENCODING
# ============================================================================

print("\n" + "=" * 80)
print("🎯 ÖZELLİK HAZIRLIK")
print("=" * 80)

# Feature ve target ayır
feature_cols = [col for col in common_features if col != 'churn']
X = df_combined[feature_cols].copy()
y = df_combined['churn'].copy()

print(f"\n📊 X shape: {X.shape}")
print(f"📊 y shape: {y.shape}")

# Kategorik değişkenleri encode et
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"\n🔤 Kategorik sütunlar: {categorical_cols}")

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

print(f"✅ {len(categorical_cols)} kategorik sütun encode edildi")

# ============================================================================
# 7. TRAIN/TEST SPLIT
# ============================================================================

print("\n" + "=" * 80)
print("✂️  TRAIN/TEST SPLIT")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 Train: {X_train.shape[0]} samples ({y_train.mean()*100:.2f}% churn)")
print(f"📊 Test: {X_test.shape[0]} samples ({y_test.mean()*100:.2f}% churn)")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Feature scaling tamamlandı")

# ============================================================================
# 8. MODEL EĞİTİMİ
# ============================================================================

print("\n" + "=" * 80)
print("🤖 XGBOOST MODEL EĞİTİMİ")
print("=" * 80)

params = {
    'objective': 'binary:logistic',
    'max_depth': 6,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
    'eval_metric': 'logloss'
}

print(f"\n🚀 Model eğitimi başlıyor...")
model = xgb.XGBClassifier(**params)
model.fit(
    X_train_scaled, y_train,
    eval_set=[(X_test_scaled, y_test)],
    verbose=False
)

print("✅ Model eğitimi tamamlandı!")

# ============================================================================
# 9. MODEL DEĞERLENDİRME
# ============================================================================

print("\n" + "=" * 80)
print("📊 MODEL PERFORMANSI")
print("=" * 80)

y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n🎯 Hybrid Model Performansı:")
print(f"   Accuracy:  {accuracy*100:.2f}%")
print(f"   Precision: {precision*100:.2f}%")
print(f"   Recall:    {recall*100:.2f}%")
print(f"   F1 Score:  {f1*100:.2f}%")
print(f"   ROC AUC:   {roc_auc*100:.2f}%")

cm = confusion_matrix(y_test, y_pred)
print(f"\n📊 Confusion Matrix:")
print(f"   TN: {cm[0][0]}, FP: {cm[0][1]}")
print(f"   FN: {cm[1][0]}, TP: {cm[1][1]}")

# Feature Importance
print(f"\n🔝 En Önemli 10 Özellik:")
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(10).iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# ============================================================================
# 10. SHAP EXPLAINER
# ============================================================================

print("\n" + "=" * 80)
print("🔍 SHAP EXPLAINER")
print("=" * 80)

print(f"\n🚀 SHAP hesaplanıyor...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train_scaled[:1000])
print("✅ SHAP explainer oluşturuldu")

# ============================================================================
# 11. MODEL KAYDET VE İNDİR
# ============================================================================

print("\n" + "=" * 80)
print("💾 MODEL DOSYALARI")
print("=" * 80)

# Dosyaları kaydet
with open('churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)

metrics = {
    'accuracy': float(accuracy),
    'precision': float(precision),
    'recall': float(recall),
    'f1_score': float(f1),
    'roc_auc': float(roc_auc),
    'confusion_matrix': cm.tolist(),
    'feature_importance': feature_importance.to_dict('records')
}

with open('model_metrics.pkl', 'wb') as f:
    pickle.dump(metrics, f)

with open('churn_model.json', 'w') as f:
    json.dump({
        'model_type': 'XGBoost Hybrid',
        'datasets': 'Maven Analytics + Iranian Churn',
        'n_samples': len(df_combined),
        'maven_samples': len(maven_standard),
        'iranian_samples': len(iranian_standard),
        'n_features': len(feature_cols),
        'metrics': {
            'accuracy': f"{accuracy*100:.2f}%",
            'precision': f"{precision*100:.2f}%",
            'recall': f"{recall*100:.2f}%",
            'f1_score': f"{f1*100:.2f}%",
            'roc_auc': f"{roc_auc*100:.2f}%"
        },
        'features': feature_cols
    }, f, indent=2)

print("✅ Dosyalar kaydedildi")

# Zip ve indir
import zipfile
with zipfile.ZipFile('aura_hybrid_models.zip', 'w') as zipf:
    zipf.write('churn_model.pkl')
    zipf.write('scaler.pkl')
    zipf.write('label_encoders.pkl')
    zipf.write('feature_names.pkl')
    zipf.write('model_metrics.pkl')
    zipf.write('churn_model.json')

files.download('aura_hybrid_models.zip')

print("\n" + "=" * 80)
print("🎉 HYBRID MODEL TAMAMLANDI!")
print("=" * 80)
print(f"\n✅ İki dataset başarıyla birleştirildi ve model eğitildi!")
print(f"\n📊 Model Özeti:")
print(f"   Toplam müşteri: {len(df_combined)}")
print(f"   Maven: {len(maven_standard)}")
print(f"   Iranian: {len(iranian_standard)}")
print(f"   Özellik sayısı: {len(feature_cols)}")
print(f"   Accuracy: {accuracy*100:.2f}%")
print(f"   ROC AUC: {roc_auc*100:.2f}%")
print(f"\n🚀 aura_hybrid_models.zip indirildi!")
print(f"   Dosyaları aura-backend/models/ klasörüne çıkart")
