# Hibrit Model Kurulum Rehberi (Türkçe)

## 📦 Hazırlık

### 1. Model Dosyalarını Kontrol Et
Google Colab'dan indirdiğin `aura_hybrid_models.zip` dosyasını açtın ve dosyaları `aura-backend/models/` klasörüne kopyaladın.

Kontrol et:
```bash
cd aura-backend
ls -la models/
```

Görmeli olduğun dosyalar:
- ✅ churn_model.pkl
- ✅ scaler.pkl
- ✅ label_encoders.pkl
- ✅ feature_names.pkl
- ✅ model_metrics.pkl
- ✅ churn_model.json

### 2. Model Özelliklerini Doğrula
```bash
python3 -c "import joblib; print(joblib.load('models/feature_names.pkl'))"
```

Çıktı şöyle olmalı:
```
['tenure_months', 'monthly_charge', 'age', 'gender', 'complaint_count', 
 'call_failures', 'support_calls_count', 'payment_delays', 'data_usage_gb', 'sms_count']
```

## 🚀 Otomatik Kurulum (Önerilen)

En kolay yol:
```bash
cd aura-backend
./deploy_hybrid_model.sh
```

Script sana 3 seçenek sunacak:
1. **Mevcut veritabanını güncelle** - Müşteri verilerini korur, yeni kolonlar ekler
2. **Yeni veritabanı oluştur** - Eski verileri siler, yeni verilerle doldurur
3. **Veritabanı güncellemesini atla** - Sadece model dosyalarını kontrol eder

## 🔧 Manuel Kurulum

### Adım 1: Veritabanını Güncelle

**Seçenek A - Mevcut veritabanını güncelle:**
```bash
python3 migrate_to_hybrid.py
```

Bu komut:
- `age` kolonu ekler (yaş)
- `gender` kolonu ekler (cinsiyet: 0=Kadın, 1=Erkek)
- `call_failures` kolonu ekler (başarısız aramalar)
- `tenure` → `tenure_months` olarak kopyalar
- Rastgele gerçekçi değerler atar

**Seçenek B - Yeni veritabanı oluştur:**
```bash
rm aura_dev.db  # Eski veritabanını sil
python3 seed_database.py  # Yeni veritabanı oluştur
```

Bu komut:
- 250 yeni müşteri oluşturur
- Hibrit model özellikleriyle (10 özellik)
- Gerçekçi yaş, cinsiyet, başarısız arama verileriyle

### Adım 2: Sunucuyu Yeniden Başlat
```bash
./start_server.sh
```

### Adım 3: Logları Kontrol Et
Sunucu başladığında şu mesajları görmeli olmalısın:
```
✅ Hybrid XGBoost model loaded successfully
   Features: ['tenure_months', 'monthly_charge', 'age', 'gender', ...]
✅ Hybrid model SHAP explainer initialized
   Features: ['tenure_months', 'monthly_charge', 'age', 'gender', ...]
```

### Adım 4: API'yi Test Et
```bash
# Müşterileri listele
curl http://localhost:8000/api/customers | jq '.[0]'

# Tahmin yap
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 12,
    "monthly_charge": 199.99,
    "age": 35,
    "gender": 1,
    "complaint_count": 2,
    "call_failures": 5,
    "support_calls_count": 3,
    "payment_delays": 1,
    "data_usage_gb": 15.5,
    "sms_count": 120,
    "plan_type": "Premium",
    "voice_minutes": 450,
    "contract_type": "Monthly"
  }'
```

### Adım 5: Frontend'i Kontrol Et
Tarayıcıda aç: http://localhost:3000

Kontrol et:
- ✅ Dashboard açılıyor
- ✅ Müşteri listesi görünüyor
- ✅ Risk skorları gösteriliyor
- ✅ Müşteri detayları açılıyor
- ✅ SHAP açıklamaları Türkçe

## 📊 Hibrit Model Özellikleri

### 10 Özellik
1. **tenure_months** - Üyelik süresi (ay)
2. **monthly_charge** - Aylık fatura (₺)
3. **age** - Yaş (18-100)
4. **gender** - Cinsiyet (0=Kadın, 1=Erkek)
5. **complaint_count** - Şikayet sayısı
6. **call_failures** - Başarısız aramalar
7. **support_calls_count** - Destek çağrısı sayısı
8. **payment_delays** - Ödeme gecikmeleri
9. **data_usage_gb** - Veri kullanımı (GB)
10. **sms_count** - SMS sayısı

### Veri Kaynakları
- **Maven Analytics:** 7,043 müşteri
- **Iranian Churn:** 3,150 müşteri
- **Toplam:** 10,193 müşteri

### Beklenen Performans
- Doğruluk: ~%85-90
- Kesinlik: ~%80-85
- Duyarlılık: ~%75-80
- F1 Skoru: ~%77-82
- ROC AUC: ~%88-92

## 🐛 Sorun Giderme

### Model Yüklenmiyor
**Hata:** `FileNotFoundError: models/churn_model.pkl`
**Çözüm:** Model dosyalarını Google Colab'dan `aura-backend/models/` klasörüne kopyala

### Yanlış Özellik Sayısı
**Hata:** `Feature shape mismatch: expected 10, got 19`
**Çözüm:** Eski Telco model dosyalarını kullanıyorsun. Hibrit model dosyalarını kullan.

### Veritabanı Hatası
**Hata:** `no such column: age`
**Çözüm:** `python3 migrate_to_hybrid.py` komutunu çalıştır

### Tahmin Hatası
**Hata:** `KeyError: 'age'` veya `KeyError: 'call_failures'`
**Çözüm:** API çağrılarına yeni zorunlu alanları ekle (age, gender, call_failures)

## ✅ Kontrol Listesi

Kurulum sonrası kontrol et:

- [ ] Sunucu hatasız başladı
- [ ] Loglar "Hybrid XGBoost model loaded successfully" gösteriyor
- [ ] API müşterileri yeni alanlarla döndürüyor (age, gender, call_failures)
- [ ] Tahminler çalışıyor
- [ ] SHAP açıklamaları Türkçe
- [ ] Frontend doğru veri gösteriyor
- [ ] Dashboard risk dağılımını gösteriyor

## 🎯 Sonraki Adımlar

1. ✅ Modeli kur
2. 📊 Gerçek müşteri verilerinde test et
3. 📈 Üretimde doğruluğu izle
4. 💼 İş kullanıcılarından geri bildirim al
5. 🔄 Gerçek churn verisiyle modeli yeniden eğit
6. 🎁 Tahminlere dayalı kampanyaları A/B test et

## 📚 Diğer Dökümanlar

- **Eğitim Rehberi:** `HYBRID_MODEL_GUIDE.md`
- **Hızlı Başlangıç:** `HYBRID_QUICK_START.md`
- **Deployment Rehberi:** `HYBRID_MODEL_DEPLOYMENT.md`
- **Özet:** `DEPLOYMENT_SUMMARY.md`
- **Eğitim Notebook:** `AURA_Hybrid_Model.ipynb`

## 💡 İpuçları

1. **İlk kurulumda** yeni veritabanı oluştur (Seçenek B)
2. **Model dosyalarını** her zaman yedekle
3. **Sunucu loglarını** kontrol et
4. **API testlerini** Postman veya curl ile yap
5. **Frontend'i** Chrome DevTools ile kontrol et

## 🎉 Başarılı Kurulum

Eğer her şey çalışıyorsa:
- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

Tebrikler! Hibrit model başarıyla kuruldu! 🚀
