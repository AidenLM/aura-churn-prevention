# 🚀 AURA Deployment Rehberi - nativestruct.com

## 📋 İçindekiler
1. [GitHub'a Push Etme](#1-githuba-push-etme)
2. [Eski Siteyi Kapatma](#2-eski-siteyi-kapatma)
3. [Vercel'e Deploy](#3-vercele-deploy)
4. [Domain Bağlama](#4-domain-bağlama)
5. [Backend Deploy (Railway/Render)](#5-backend-deploy)

---

## 1. GitHub'a Push Etme

### Adım 1.1: .gitignore Dosyasını Kontrol Et

Büyük dosyaları GitHub'a atmamak için `.gitignore` dosyasını kontrol edin:

```bash
# Frontend .gitignore kontrol
cat aura-frontend/.gitignore

# Backend .gitignore kontrol
cat aura-backend/.gitignore
```

### Adım 1.2: Gereksiz Dosyaları Temizle

```bash
# Frontend build dosyalarını sil
cd aura-frontend
rm -rf .next
rm -rf node_modules

# Backend venv'i sil
cd ../aura-backend
rm -rf venv
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +

cd ..
```

### Adım 1.3: Git Repository Oluştur

```bash
# Git başlat (eğer yoksa)
git init

# Tüm dosyaları ekle
git add .

# Commit yap
git commit -m "Initial commit: AURA Customer Churn Prevention System"
```

### Adım 1.4: GitHub Repository Oluştur

1. GitHub'da yeni repository oluştur: https://github.com/new
2. Repository adı: `aura-churn-prevention`
3. Public veya Private seç
4. README ekleme (zaten var)

### Adım 1.5: GitHub'a Push Et

```bash
# Remote ekle (KULLANICI_ADIN yerine GitHub kullanıcı adını yaz)
git remote add origin https://github.com/KULLANICI_ADIN/aura-churn-prevention.git

# Main branch'e push et
git branch -M main
git push -u origin main
```

**Not:** Eğer dosya boyutu 100MB'dan büyükse Git LFS kullanmanız gerekebilir:

```bash
# Git LFS kur (macOS)
brew install git-lfs
git lfs install

# Büyük dosyaları track et
git lfs track "*.pkl"
git lfs track "*.db"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

---

## 2. Eski Siteyi Kapatma

### Seçenek A: GitHub Pages'den Kaldırma

Eğer eski site GitHub Pages kullanıyorsa:

1. Eski repository'ye git: https://github.com/KULLANICI_ADIN/eski-repo
2. Settings → Pages
3. "Source" kısmını "None" yap
4. Save

### Seçenek B: Vercel'den Kaldırma

Eğer eski site Vercel'de ise:

1. Vercel Dashboard'a git: https://vercel.com/dashboard
2. Eski projeyi bul
3. Settings → Domains
4. `nativestruct.com` domain'ini Remove et
5. Veya projeyi tamamen sil: Settings → Advanced → Delete Project

### Seçenek C: Netlify'dan Kaldırma

1. Netlify Dashboard: https://app.netlify.com
2. Site Settings → Domain Management
3. Custom domains'den `nativestruct.com`'u remove et

---

## 3. Vercel'e Deploy (Frontend)

### Adım 3.1: Vercel Hesabı Oluştur

1. https://vercel.com/signup adresine git
2. GitHub ile giriş yap

### Adım 3.2: Yeni Proje Oluştur

1. "Add New" → "Project"
2. GitHub repository'nizi seçin: `aura-churn-prevention`
3. Import

### Adım 3.3: Build Ayarları

```
Framework Preset: Next.js
Root Directory: aura-frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### Adım 3.4: Environment Variables

```
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

**Not:** Backend URL'ini adım 5'ten sonra ekleyeceksiniz.

### Adım 3.5: Deploy

"Deploy" butonuna tıklayın. 2-3 dakika içinde deploy olacak.

---

## 4. Domain Bağlama (nativestruct.com)

### Adım 4.1: Vercel'de Domain Ekle

1. Vercel Dashboard → Your Project → Settings → Domains
2. "Add" butonuna tıkla
3. `nativestruct.com` yaz
4. Add

### Adım 4.2: DNS Ayarları (Domain Sağlayıcınızda)

Vercel size 2 seçenek sunacak:

#### Seçenek A: Nameservers (Önerilen)

Vercel'in nameserver'larını kullan:
```
ns1.vercel-dns.com
ns2.vercel-dns.com
```

Domain sağlayıcınızda (GoDaddy, Namecheap, vs.):
1. DNS Management → Nameservers
2. Custom Nameservers seç
3. Vercel'in nameserver'larını ekle

#### Seçenek B: A Record (Manuel)

Domain sağlayıcınızda:
1. DNS Management → Add Record
2. Type: A Record
3. Host: @ (veya boş)
4. Value: `76.76.21.21` (Vercel IP)
5. TTL: 3600

CNAME Record ekle:
1. Type: CNAME
2. Host: www
3. Value: `cname.vercel-dns.com`
4. TTL: 3600

### Adım 4.3: SSL Sertifikası

Vercel otomatik olarak SSL sertifikası oluşturacak (Let's Encrypt).
24 saat içinde aktif olur.

---

## 5. Backend Deploy (Railway veya Render)

### Seçenek A: Railway (Önerilen)

#### Adım 5A.1: Railway Hesabı

1. https://railway.app adresine git
2. GitHub ile giriş yap

#### Adım 5A.2: Yeni Proje

1. "New Project" → "Deploy from GitHub repo"
2. `aura-churn-prevention` seç
3. "Add variables" → Environment Variables ekle:

```bash
# Python version
PYTHON_VERSION=3.11

# Database
DATABASE_URL=sqlite:///./aura_dev.db

# CORS
CORS_ORIGINS=https://nativestruct.com,https://www.nativestruct.com
```

#### Adım 5A.3: Build Ayarları

Railway otomatik algılar ama manuel ayarlamak için:

1. Settings → Build
2. Root Directory: `aura-backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Adım 5A.4: Deploy

"Deploy" butonuna tıklayın. Railway size bir URL verecek:
```
https://aura-backend-production-xxxx.up.railway.app
```

### Seçenek B: Render

#### Adım 5B.1: Render Hesabı

1. https://render.com adresine git
2. GitHub ile giriş yap

#### Adım 5B.2: Yeni Web Service

1. "New" → "Web Service"
2. GitHub repo'nuzu bağlayın
3. Ayarlar:

```
Name: aura-backend
Region: Frankfurt (EU)
Branch: main
Root Directory: aura-backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Adım 5B.3: Environment Variables

```bash
PYTHON_VERSION=3.11
DATABASE_URL=sqlite:///./aura_dev.db
CORS_ORIGINS=https://nativestruct.com,https://www.nativestruct.com
```

#### Adım 5B.4: Deploy

"Create Web Service" butonuna tıklayın.

---

## 6. Frontend'i Backend'e Bağla

### Adım 6.1: Backend URL'ini Al

Railway veya Render'dan backend URL'inizi kopyalayın:
```
https://aura-backend-production-xxxx.up.railway.app
```

### Adım 6.2: Vercel Environment Variable Güncelle

1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. `NEXT_PUBLIC_API_URL` değerini backend URL ile güncelle
3. "Save"
4. "Redeploy" butonuna tıkla

### Adım 6.3: Test Et

```bash
# Frontend test
curl https://nativestruct.com

# Backend test
curl https://your-backend-url.railway.app/api/dashboard/summary
```

---

## 7. Veritabanı ve Model Dosyalarını Upload Et

### Adım 7.1: Railway/Render'a Dosya Upload

Railway kullanıyorsanız:

```bash
# Railway CLI kur
npm i -g @railway/cli

# Login
railway login

# Proje seç
railway link

# Dosyaları upload et
railway run python seed_database.py
```

Render kullanıyorsanız:
- Render Dashboard → Shell
- Dosyaları manuel upload edin veya GitHub'dan çekin

---

## 8. Son Kontroller

### ✅ Checklist

- [ ] Frontend `nativestruct.com` adresinde açılıyor
- [ ] Backend API çalışıyor
- [ ] Dashboard verileri yükleniyor
- [ ] Müşteri detay sayfası çalışıyor
- [ ] Risk hesaplama çalışıyor
- [ ] SSL sertifikası aktif (https://)
- [ ] Mobil responsive çalışıyor

### Test Komutları

```bash
# Frontend test
curl -I https://nativestruct.com

# Backend health check
curl https://your-backend-url.railway.app/health

# API test
curl https://your-backend-url.railway.app/api/dashboard/summary
```

---

## 9. Sorun Giderme

### Problem: "Module not found" hatası

**Çözüm:**
```bash
# Frontend
cd aura-frontend
npm install
npm run build

# Backend
cd aura-backend
pip install -r requirements.txt
```

### Problem: CORS hatası

**Çözüm:**
Backend `.env` dosyasında:
```bash
CORS_ORIGINS=https://nativestruct.com,https://www.nativestruct.com
```

### Problem: Database bulunamıyor

**Çözüm:**
```bash
# Railway/Render shell'de
python seed_database.py
```

### Problem: Model dosyaları yüklenmiyor

**Çözüm:**
Model dosyalarını Git LFS ile push edin:
```bash
git lfs track "*.pkl"
git add .gitattributes
git add aura-backend/models/*.pkl
git commit -m "Add model files with LFS"
git push
```

---

## 10. Performans Optimizasyonu

### Frontend Optimizasyonu

```bash
# Next.js production build
cd aura-frontend
npm run build
npm run start
```

### Backend Optimizasyonu

```python
# app/main.py - Caching ekle
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
```

---

## 📞 Destek

Sorun yaşarsanız:
1. Vercel Logs: Dashboard → Deployments → Logs
2. Railway Logs: Dashboard → Deployments → View Logs
3. GitHub Issues: Repository → Issues

---

## 🎉 Tebrikler!

AURA sisteminiz artık `nativestruct.com` adresinde canlı! 🚀
