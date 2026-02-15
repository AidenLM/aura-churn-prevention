#!/usr/bin/env python3
"""Create final production-ready notebook without leakage"""
import json

def create_notebook():
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    cells = []
    
    # Title
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 🚀 AURA Churn Prediction - Production Ready\n",
            "## Iranian Dataset - Leakage-Free Model\n",
            "\n",
            "### 🎯 Hedef Metrikler (Gerçekçi):\n",
            "- **Accuracy:** 80-85%\n",
            "- **Precision:** 65-72%\n",
            "- **Recall:** 70-78%\n",
            "- **ROC-AUC:** 82-88%\n",
            "\n",
            "### ⚠️ Leakage Önleme:\n",
            "- Status ve Customer Value KULLANILMAYACAK\n",
            "- Sadece 10 güvenli feature\n",
            "- 5-fold cross-validation\n",
            "\n",
            "### 📊 Dataset:\n",
            "- Iranian Churn: ~3,150 müşteri\n",
            "- 10 güvenli feature\n",
            "- Süre: ~7-10 dakika"
        ]
    })
    
    # Install
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## 📦 1. Kütüphaneleri Yükle"]})
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "!pip install -q xgboost scikit-learn pandas numpy shap matplotlib seaborn\n",
            "\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import pickle\n",
            "import json\n",
            "import zipfile\n",
            "from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold\n",
            "from sklearn.preprocessing import LabelEncoder, StandardScaler\n",
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve\n",
            "import xgboost as xgb\n",
            "import shap\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "print('=' * 80)\n",
            "print('🎯 AURA CHURN PREDICTION - PRODUCTION READY')\n",
            "print('=' * 80)\n",
            "print('\\n✅ Kütüphaneler yüklendi!')"
        ]
    })
    
    # Load dataset
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## 📤 2. Dataset Yükle"]})
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('\\n' + '=' * 80)\n",
            "print('📤 IRANIAN CHURN DATASET')\n",
            "print('==' * 80)\n",
            "print('\\n📥 İndir: https://archive.ics.uci.edu/ml/datasets/Iranian+Churn+Dataset')\n",
            "print('\\n👇 Dosyayı seç ve yükle:')\n",
            "\n",
            "from google.colab import files\n",
            "uploaded = files.upload()\n",
            "\n",
            "iranian_file = list(uploaded.keys())[0]\n",
            "df = pd.read_csv(iranian_file)\n",
            "\n",
            "print(f'\\n✅ Dataset: {df.shape[0]} müşteri, {df.shape[1]} özellik')\n",
            "print(f'\\n📋 Sütunlar:')\n",
            "print(df.columns.tolist())\n",
            "df.head()"
        ]
    })
    
    notebook["cells"] = cells
    return notebook

# Create
nb = create_notebook()
with open("AURA_Churn_Model.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("✅ Notebook part 1 created")
