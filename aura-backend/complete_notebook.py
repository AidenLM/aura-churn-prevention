#!/usr/bin/env python3
"""Complete the AURA Churn Model notebook with all cells"""
import json

# Read existing
with open('AURA_Churn_Model.ipynb', 'r') as f:
    nb = json.load(f)

# Add remaining cells
new_cells = [
    # Feature selection (leakage control)
    {"cell_type": "markdown", "metadata": {}, "source": ["## 🔍 3. Feature Selection - Leakage Kontrolü"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('🔍 FEATURE SELECTION - LEAKAGE KONTROLÜ')\n",
            "print('=' * 80)\n",
            "\n",
            "# Churn sütununu bul\n",
            "churn_col = [col for col in df.columns if 'churn' in col.lower()]\n",
            "if churn_col:\n",
            "    churn_column = churn_col[0]\n",
            "    print(f'\\n✅ Churn sütunu: {churn_column}')\n",
            "else:\n",
            "    churn_column = df.columns[-1]\n",
            "    print(f'\\n⚠️  Churn sütunu bulunamadı, son sütun: {churn_column}')\n",
            "\n",
            "# ⚠️ LEAKAGE RİSKİ OLAN FEATURE'LARI ÇIKAR\n",
            "leakage_features = ['Status', 'Customer Value', 'Age Group']\n",
            "print(f'\\n⚠️  Leakage riski olan feature\\'lar (ÇIKARILACAK):')\n",
            "for feat in leakage_features:\n",
            "    if feat in df.columns:\n",
            "        print(f'   ❌ {feat}')\n",
            "        df = df.drop(feat, axis=1)\n",
            "\n",
            "# Güvenli feature'lar\n",
            "print(f'\\n✅ Güvenli feature\\'lar (KULLANILACAK):')\n",
            "safe_features = [col for col in df.columns if col != churn_column]\n",
            "for feat in safe_features:\n",
            "    print(f'   ✅ {feat}')\n",
            "\n",
            "print(f'\\n📊 Final feature count: {len(safe_features)}')"
        ]
    },
    
    # Data preparation
    {"cell_type": "markdown", "metadata": {}, "source": ["## 🔧 4. Veri Hazırlık"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('🔧 VERİ HAZIRLIK')\n",
            "print('=' * 80)\n",
            "\n",
            "# Target ve features\n",
            "y = df[churn_column].astype(int)\n",
            "X = df.drop(churn_column, axis=1)\n",
            "\n",
            "print(f'\\n📊 Churn Dağılımı:')\n",
            "print(f'   Non-churn: {len(y[y==0])} ({len(y[y==0])/len(y)*100:.1f}%)')\n",
            "print(f'   Churn: {len(y[y==1])} ({len(y[y==1])/len(y)*100:.1f}%)')\n",
            "\n",
            "# Eksik değerleri doldur\n",
            "for col in X.columns:\n",
            "    if X[col].isnull().sum() > 0:\n",
            "        if X[col].dtype in ['float64', 'int64']:\n",
            "            X[col].fillna(X[col].median(), inplace=True)\n",
            "        else:\n",
            "            X[col].fillna(X[col].mode()[0], inplace=True)\n",
            "\n",
            "# Kategorik encode\n",
            "categorical_cols = X.select_dtypes(include=['object']).columns.tolist()\n",
            "label_encoders = {}\n",
            "for col in categorical_cols:\n",
            "    le = LabelEncoder()\n",
            "    X[col] = le.fit_transform(X[col].astype(str))\n",
            "    label_encoders[col] = le\n",
            "\n",
            "print(f'\\n✅ X: {X.shape}, y: {y.shape}')\n",
            "print(f'✅ {len(categorical_cols)} kategorik sütun encode edildi')\n",
            "print(f'\\n📋 Final Features:')\n",
            "print(X.columns.tolist())"
        ]
    },
    
    # Train/test split
    {"cell_type": "markdown", "metadata": {}, "source": ["## ✂️ 5. Train/Test Split"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('✂️  TRAIN/TEST SPLIT')\n",
            "print('=' * 80)\n",
            "\n",
            "# Stratified split\n",
            "X_train, X_test, y_train, y_test = train_test_split(\n",
            "    X, y, test_size=0.25, random_state=42, stratify=y\n",
            ")\n",
            "\n",
            "# Scaling\n",
            "scaler = StandardScaler()\n",
            "X_train_scaled = scaler.fit_transform(X_train)\n",
            "X_test_scaled = scaler.transform(X_test)\n",
            "\n",
            "print(f'\\n📊 Train: {len(X_train)} samples ({y_train.mean()*100:.2f}% churn)')\n",
            "print(f'📊 Test: {len(X_test)} samples ({y_test.mean()*100:.2f}% churn)')\n",
            "print('✅ Feature scaling tamamlandı')"
        ]
    },
    
    # Model training
    {"cell_type": "markdown", "metadata": {}, "source": ["## 🤖 6. Model Eğitimi - Conservative Parameters"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('🤖 XGBOOST MODEL - CONSERVATIVE PARAMETERS')\n",
            "print('=' * 80)\n",
            "\n",
            "# Class imbalance\n",
            "n_non_churn = len(y_train[y_train == 0])\n",
            "n_churn = len(y_train[y_train == 1])\n",
            "scale_pos_weight = n_non_churn / n_churn\n",
            "\n",
            "print(f'\\n📊 Class Distribution:')\n",
            "print(f'   Non-churn: {n_non_churn} ({n_non_churn/len(y_train)*100:.1f}%)')\n",
            "print(f'   Churn: {n_churn} ({n_churn/len(y_train)*100:.1f}%)')\n",
            "print(f'   scale_pos_weight: {scale_pos_weight:.2f}')\n",
            "\n",
            "# Conservative model (prevent overfitting)\n",
            "model = xgb.XGBClassifier(\n",
            "    objective='binary:logistic',\n",
            "    max_depth=3,                    # Shallow trees\n",
            "    learning_rate=0.05,             # Slow learning\n",
            "    n_estimators=300,               # Moderate number\n",
            "    min_child_weight=5,             # Strong regularization\n",
            "    gamma=0.2,                      # Pruning\n",
            "    subsample=0.7,                  # Less data per tree\n",
            "    colsample_bytree=0.7,           # Less features per tree\n",
            "    scale_pos_weight=scale_pos_weight,\n",
            "    random_state=42,\n",
            "    eval_metric='auc'\n",
            ")\n",
            "\n",
            "print('\\n🚀 Model eğitimi başlıyor...')\n",
            "model.fit(\n",
            "    X_train_scaled, y_train,\n",
            "    eval_set=[(X_test_scaled, y_test)],\n",
            "    verbose=False\n",
            ")\n",
            "print('✅ Model eğitimi tamamlandı!')"
        ]
    },
    
    # Cross-validation
    {"cell_type": "markdown", "metadata": {}, "source": ["## 🔄 7. Cross-Validation - Overfitting Kontrolü"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('🔄 5-FOLD CROSS-VALIDATION')\n",
            "print('=' * 80)\n",
            "\n",
            "# 5-fold CV\n",
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n",
            "cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='roc_auc')\n",
            "\n",
            "print(f'\\n📊 Cross-Validation ROC-AUC Scores:')\n",
            "for i, score in enumerate(cv_scores, 1):\n",
            "    print(f'   Fold {i}: {score*100:.2f}%')\n",
            "\n",
            "print(f'\\n📊 CV Summary:')\n",
            "print(f'   Mean: {cv_scores.mean()*100:.2f}%')\n",
            "print(f'   Std: {cv_scores.std()*100:.2f}%')\n",
            "\n",
            "# Overfitting check\n",
            "if cv_scores.std() > 0.05:\n",
            "    print(f'\\n⚠️  WARNING: High variance ({cv_scores.std()*100:.2f}%) - possible overfitting')\n",
            "else:\n",
            "    print(f'\\n✅ Low variance ({cv_scores.std()*100:.2f}%) - good generalization')"
        ]
    }
]

nb["cells"].extend(new_cells)

# Save
with open('AURA_Churn_Model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"✅ Added {len(new_cells)} cells. Total: {len(nb['cells'])} cells")
