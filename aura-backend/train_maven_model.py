"""
AURA Churn Prediction - Maven Analytics Dataset Training Script
================================================================

Bu script Maven Analytics Telecom Churn dataset'ini kullanarak:
1. Dataset'i yükler ve temizler
2. Davranışsal özellikleri türetir (complaint_count, support_calls, payment_delays, sms_count)
3. XGBoost modeli eğitir
4. SHAP explainer oluşturur
5. Model dosyalarını kaydeder

Dataset: Maven Analytics Telecom Customer Churn (7,043 müşteri, 37+ özellik)
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

# ============================================================================
# 1. DATASET YÜKLEME VE İLK İNCELEME
# ============================================================================

print("=" * 80)
print("🎯 AURA CHURN PREDICTION - MAVEN ANALYTICS DATASET")
print("=" * 80)

# Dataset'i yükle (Google Colab'da upload edilecek)
print("\n📂 Dataset yükleniyor...")
print("⚠️  Lütfen Maven Analytics'ten indirdiğin CSV dosyasını yükle!")
print("    Link: https://mavenanalytics.io/data-playground/telecom-customer-churn")

# Google Colab için file upload
from google.colab import files
uploaded = files.upload()

# İlk yüklenen dosyayı al
filename = list(uploaded.keys())[0]
df = pd.read_csv(filename)

print(f"\n✅ Dataset yüklendi: {filename}")
print(f"📊 Boyut: {df.shape[0]} satır, {df.shape[1]} sütun")
print(f"\n📋 İlk 5 satır:")
print(df.head())

# ============================================================================
# 2. VERİ TEMİZLEME VE HAZIRLIK
# ============================================================================

print("\n" + "=" * 80)
print("🧹 VERİ TEMİZLEME")
print("=" * 80)

# Eksik değerleri kontrol et
print(f"\n📊 Eksik değerler:")
missing = df.isnull().sum()
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("✅ Eksik değer yok!")

# Churn sütununu binary'ye çevir
if 'Customer_Status' in df.columns:
    df['Churn'] = (df['Customer_Status'] == 'Churned').astype(int)
    print(f"\n✅ Churn sütunu oluşturuldu (Customer_Status'ten)")
elif 'Churn' in df.columns:
    if df['Churn'].dtype == 'object':
        df['Churn'] = (df['Churn'] == 'Yes').astype(int)
    print(f"\n✅ Churn sütunu binary'ye çevrildi")

# Churn dağılımı
churn_dist = df['Churn'].value_counts()
print(f"\n📊 Churn Dağılımı:")
print(f"   Kalan müşteriler: {churn_dist[0]} ({churn_dist[0]/len(df)*100:.1f}%)")
print(f"   Ayrılan müşteriler: {churn_dist[1]} ({churn_dist[1]/len(df)*100:.1f}%)")

# ============================================================================
# 3. DAVRANIŞSAL ÖZELLİKLERİ TÜRET (FEATURE ENGINEERING)
# ============================================================================

print("\n" + "=" * 80)
print("🔧 DAVRANIŞSAL ÖZELLİKLER TÜRETİLİYOR")
print("=" * 80)

def derive_behavioral_features(df):
    """
    Maven Analytics dataset'inden davranışsal özellikleri türet
    """
    df_new = df.copy()
    
    # 1. COMPLAINT_COUNT (Şikayet Sayısı)
    print("\n1️⃣  complaint_count türetiliyor...")
    def get_complaint_count(row):
        # Churn_Reason'dan şikayet sayısını tahmin et
        churn_reason = str(row.get('Churn_Reason', ''))
        premium_support = str(row.get('Premium_Tech_Support', 'No'))
        
        if 'Attitude' in churn_reason or 'support person' in churn_reason.lower():
            return np.random.randint(4, 8)  # Destek personeli tutumu kötü
        elif 'Dissatisfaction' in churn_reason or 'Poor' in churn_reason:
            return np.random.randint(2, 5)  # Memnuniyetsizlik
        elif premium_support == 'Yes':
            return np.random.randint(0, 2)  # Premium destek alanlar daha az şikayet eder
        elif premium_support == 'No':
            return np.random.randint(1, 4)  # Premium destek almayanlar daha fazla şikayet edebilir
        else:
            return np.random.randint(0, 3)  # Varsayılan
    
    df_new['complaint_count'] = df_new.apply(get_complaint_count, axis=1)
    print(f"   ✅ Ortalama: {df_new['complaint_count'].mean():.2f}, Min: {df_new['complaint_count'].min()}, Max: {df_new['complaint_count'].max()}")
    
    # 2. SUPPORT_CALLS_COUNT (Destek Çağrısı Sayısı)
    print("\n2️⃣  support_calls_count türetiliyor...")
    def get_support_calls(row):
        churn_reason = str(row.get('Churn_Reason', ''))
        premium_support = str(row.get('Premium_Tech_Support', 'No'))
        complaint_count = row['complaint_count']
        
        if 'Attitude' in churn_reason:
            return np.random.randint(6, 12)  # Çok fazla destek çağrısı
        elif premium_support == 'Yes':
            return np.random.randint(3, 8)  # Premium destek kullananlar daha fazla arar
        elif complaint_count >= 4:
            return np.random.randint(5, 10)  # Şikayeti çok olanlar daha fazla arar
        elif premium_support == 'No':
            return np.random.randint(0, 3)  # Premium destek almayanlar az arar
        else:
            return np.random.randint(1, 4)  # Varsayılan
    
    df_new['support_calls_count'] = df_new.apply(get_support_calls, axis=1)
    print(f"   ✅ Ortalama: {df_new['support_calls_count'].mean():.2f}, Min: {df_new['support_calls_count'].min()}, Max: {df_new['support_calls_count'].max()}")
    
    # 3. PAYMENT_DELAYS (Ödeme Gecikmeleri)
    print("\n3️⃣  payment_delays türetiliyor...")
    def get_payment_delays(row):
        payment_method = str(row.get('Payment_Method', ''))
        churn_reason = str(row.get('Churn_Reason', ''))
        
        if 'Price' in churn_reason or 'Expensive' in churn_reason:
            return np.random.randint(3, 6)  # Fiyat şikayeti olanlar ödeme yapmakta zorlanır
        elif 'Mailed check' in payment_method or 'Mail' in payment_method:
            return np.random.randint(2, 5)  # Posta ile ödeme gecikmeli
        elif 'Bank' in payment_method:
            return np.random.randint(1, 3)  # Banka transferi orta
        elif 'Credit' in payment_method or 'Electronic' in payment_method:
            return np.random.randint(0, 2)  # Kredi kartı/elektronik hızlı
        else:
            return np.random.randint(0, 3)  # Varsayılan
    
    df_new['payment_delays'] = df_new.apply(get_payment_delays, axis=1)
    print(f"   ✅ Ortalama: {df_new['payment_delays'].mean():.2f}, Min: {df_new['payment_delays'].min()}, Max: {df_new['payment_delays'].max()}")
    
    # 4. DATA_USAGE_GB (Veri Kullanımı)
    print("\n4️⃣  data_usage_gb türetiliyor...")
    if 'Avg_Monthly_GB_Download' in df_new.columns:
        df_new['data_usage_gb'] = df_new['Avg_Monthly_GB_Download']
        print(f"   ✅ Avg_Monthly_GB_Download'dan kopyalandı")
    else:
        # Yoksa türet
        def get_data_usage(row):
            internet_service = str(row.get('Internet_Service', 'No'))
            streaming_tv = str(row.get('Streaming_TV', 'No'))
            streaming_movies = str(row.get('Streaming_Movies', 'No'))
            
            if internet_service == 'No':
                return 0
            
            base_usage = np.random.uniform(5, 20)
            if streaming_tv == 'Yes':
                base_usage += np.random.uniform(10, 30)
            if streaming_movies == 'Yes':
                base_usage += np.random.uniform(15, 40)
            
            return round(base_usage, 2)
        
        df_new['data_usage_gb'] = df_new.apply(get_data_usage, axis=1)
        print(f"   ✅ Streaming servislerinden türetildi")
    
    print(f"   ✅ Ortalama: {df_new['data_usage_gb'].mean():.2f} GB")
    
    # 5. SMS_COUNT (SMS Sayısı)
    print("\n5️⃣  sms_count türetiliyor...")
    def get_sms_count(row):
        phone_service = str(row.get('Phone_Service', 'No'))
        multiple_lines = str(row.get('Multiple_Lines', 'No'))
        
        if phone_service == 'No':
            return 0
        elif multiple_lines == 'Yes':
            return np.random.randint(100, 300)  # Çoklu hat kullananlar daha fazla SMS atar
        else:
            return np.random.randint(20, 150)  # Tek hat kullananlar orta seviye
    
    df_new['sms_count'] = df_new.apply(get_sms_count, axis=1)
    print(f"   ✅ Ortalama: {df_new['sms_count'].mean():.2f}, Min: {df_new['sms_count'].min()}, Max: {df_new['sms_count'].max()}")
    
    return df_new

# Davranışsal özellikleri türet
df = derive_behavioral_features(df)

print("\n✅ Davranışsal özellikler başarıyla türetildi!")
print(f"📊 Yeni boyut: {df.shape[0]} satır, {df.shape[1]} sütun")

# ============================================================================
# 4. ÖZELLİK SEÇİMİ VE HAZIRLIK
# ============================================================================

print("\n" + "=" * 80)
print("🎯 ÖZELLİK SEÇİMİ")
print("=" * 80)

# Kullanılacak özellikler
feature_columns = [
    # Davranışsal özellikler (türetilmiş)
    'complaint_count',
    'support_calls_count',
    'payment_delays',
    'data_usage_gb',
    'sms_count',
    
    # Demografik
    'Age',
    'Gender',
    'Married',
    'Number_of_Dependents',
    
    # Müşteri bilgileri
    'Tenure_in_Months',
    'Number_of_Referrals',
    
    # Servisler
    'Phone_Service',
    'Multiple_Lines',
    'Internet_Service',
    'Internet_Type',
    'Online_Security',
    'Online_Backup',
    'Device_Protection_Plan',
    'Premium_Tech_Support',
    'Streaming_TV',
    'Streaming_Movies',
    'Streaming_Music',
    'Unlimited_Data',
    
    # Sözleşme
    'Contract',
    'Paperless_Billing',
    'Payment_Method',
    'Monthly_Charge',
    'Total_Revenue',
    'Offer'
]

# Mevcut sütunları kontrol et
available_features = [col for col in feature_columns if col in df.columns]
missing_features = [col for col in feature_columns if col not in df.columns]

print(f"\n✅ Kullanılabilir özellikler: {len(available_features)}")
if missing_features:
    print(f"⚠️  Eksik özellikler: {missing_features}")

# Feature ve target ayır
X = df[available_features].copy()
y = df['Churn'].copy()

print(f"\n📊 X shape: {X.shape}")
print(f"📊 y shape: {y.shape}")

# ============================================================================
# 5. KATEGORİK DEĞİŞKENLERİ ENCODE ET
# ============================================================================

print("\n" + "=" * 80)
print("🔤 KATEGORİK DEĞİŞKENLER ENCODE EDİLİYOR")
print("=" * 80)

# Kategorik sütunları bul
categorical_columns = X.select_dtypes(include=['object']).columns.tolist()
print(f"\n📋 Kategorik sütunlar ({len(categorical_columns)}):")
for col in categorical_columns:
    print(f"   - {col}: {X[col].nunique()} unique değer")

# Label Encoding
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

print(f"\n✅ {len(categorical_columns)} kategorik sütun encode edildi!")

# ============================================================================
# 6. VERİYİ TRAIN/TEST OLARAK AYIR
# ============================================================================

print("\n" + "=" * 80)
print("✂️  VERİ BÖLME (TRAIN/TEST SPLIT)")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 Train set: {X_train.shape[0]} samples")
print(f"📊 Test set: {X_test.shape[0]} samples")
print(f"\n📊 Train churn rate: {y_train.mean()*100:.2f}%")
print(f"📊 Test churn rate: {y_test.mean()*100:.2f}%")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n✅ Feature scaling tamamlandı!")

# ============================================================================
# 7. MODEL EĞİTİMİ (XGBOOST)
# ============================================================================

print("\n" + "=" * 80)
print("🤖 MODEL EĞİTİMİ (XGBOOST)")
print("=" * 80)

# XGBoost parametreleri
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

print(f"\n📋 Model parametreleri:")
for key, value in params.items():
    print(f"   {key}: {value}")

# Model oluştur ve eğit
print(f"\n🚀 Model eğitimi başlıyor...")
model = xgb.XGBClassifier(**params)
model.fit(
    X_train_scaled, y_train,
    eval_set=[(X_test_scaled, y_test)],
    verbose=False
)

print(f"✅ Model eğitimi tamamlandı!")

# ============================================================================
# 8. MODEL DEĞERLENDİRME
# ============================================================================

print("\n" + "=" * 80)
print("📊 MODEL DEĞERLENDİRME")
print("=" * 80)

# Tahminler
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Metrikler
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n🎯 Model Performansı:")
print(f"   Accuracy:  {accuracy*100:.2f}%")
print(f"   Precision: {precision*100:.2f}%")
print(f"   Recall:    {recall*100:.2f}%")
print(f"   F1 Score:  {f1*100:.2f}%")
print(f"   ROC AUC:   {roc_auc*100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\n📊 Confusion Matrix:")
print(f"   True Negatives:  {cm[0][0]}")
print(f"   False Positives: {cm[0][1]}")
print(f"   False Negatives: {cm[1][0]}")
print(f"   True Positives:  {cm[1][1]}")

# Feature Importance
print(f"\n🔝 En Önemli 10 Özellik:")
feature_importance = pd.DataFrame({
    'feature': available_features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(10).iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# ============================================================================
# 9. SHAP EXPLAINER OLUŞTUR
# ============================================================================

print("\n" + "=" * 80)
print("🔍 SHAP EXPLAINER OLUŞTURULUYOR")
print("=" * 80)

print(f"\n🚀 SHAP explainer hesaplanıyor (bu biraz zaman alabilir)...")

# SHAP explainer oluştur
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train_scaled[:1000])  # İlk 1000 sample

print(f"✅ SHAP explainer oluşturuldu!")

# ============================================================================
# 10. MODEL DOSYALARINI KAYDET
# ============================================================================

print("\n" + "=" * 80)
print("💾 MODEL DOSYALARI KAYDEDILIYOR")
print("=" * 80)

# Model dosyalarını kaydet
print(f"\n📁 Dosyalar kaydediliyor...")

# 1. XGBoost model
with open('churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print(f"   ✅ churn_model.pkl")

# 2. Scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print(f"   ✅ scaler.pkl")

# 3. Label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print(f"   ✅ label_encoders.pkl")

# 4. Feature names
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(available_features, f)
print(f"   ✅ feature_names.pkl")

# 5. Model metrics
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
print(f"   ✅ model_metrics.pkl")

# JSON formatında da kaydet
with open('churn_model.json', 'w') as f:
    json.dump({
        'model_type': 'XGBoost',
        'dataset': 'Maven Analytics Telecom Churn',
        'n_samples': len(df),
        'n_features': len(available_features),
        'metrics': {
            'accuracy': f"{accuracy*100:.2f}%",
            'precision': f"{precision*100:.2f}%",
            'recall': f"{recall*100:.2f}%",
            'f1_score': f"{f1*100:.2f}%",
            'roc_auc': f"{roc_auc*100:.2f}%"
        },
        'features': available_features,
        'behavioral_features': [
            'complaint_count',
            'support_calls_count',
            'payment_delays',
            'data_usage_gb',
            'sms_count'
        ]
    }, f, indent=2)
print(f"   ✅ churn_model.json")

print(f"\n✅ Tüm dosyalar kaydedildi!")

# ============================================================================
# 11. DOSYALARI İNDİR (GOOGLE COLAB)
# ============================================================================

print("\n" + "=" * 80)
print("📥 DOSYALAR İNDİRİLİYOR")
print("=" * 80)

# Dosyaları zip'le
import zipfile

print(f"\n📦 Dosyalar zip'leniyor...")
with zipfile.ZipFile('aura_maven_models.zip', 'w') as zipf:
    zipf.write('churn_model.pkl')
    zipf.write('scaler.pkl')
    zipf.write('label_encoders.pkl')
    zipf.write('feature_names.pkl')
    zipf.write('model_metrics.pkl')
    zipf.write('churn_model.json')

print(f"✅ aura_maven_models.zip oluşturuldu!")

# İndir
print(f"\n📥 Dosya indiriliyor...")
files.download('aura_maven_models.zip')

print("\n" + "=" * 80)
print("🎉 TAMAMLANDI!")
print("=" * 80)
print(f"\n✅ Model başarıyla eğitildi ve kaydedildi!")
print(f"✅ aura_maven_models.zip dosyasını indir ve aura-backend/models/ klasörüne çıkart")
print(f"\n📊 Model Özeti:")
print(f"   Dataset: Maven Analytics Telecom Churn")
print(f"   Müşteri sayısı: {len(df)}")
print(f"   Özellik sayısı: {len(available_features)}")
print(f"   Accuracy: {accuracy*100:.2f}%")
print(f"   ROC AUC: {roc_auc*100:.2f}%")
print(f"\n🚀 Sonraki adım: Backend'i güncelle ve yeni modeli kullan!")
