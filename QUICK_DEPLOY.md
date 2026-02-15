# 🚀 AURA - Hızlı Deployment Rehberi

## ✅ Tamamlanan Adımlar

1. ✅ Gereksiz dosyalar temizlendi (1.5GB → 31MB)
2. ✅ Git repository oluşturuldu
3. ✅ İlk commit yapıldı

---

## 📝 Şimdi Yapılacaklar (5 Dakika)

### 1️⃣ GitHub Repository Oluştur (1 dk)

1. Tarayıcıda aç: **https://github.com/new**
2. Repository adı: `aura-churn-prevention`
3. Public seç
4. **Create repository** butonuna tıkla

### 2️⃣ GitHub'a Push Et (1 dk)

Terminal'de şu komutları çalıştır (KULLANICI_ADIN yerine GitHub kullanıcı adını yaz):

```bash
git remote add origin https://github.com/KULLANICI_ADIN/aura-churn-prevention.git
git branch -M main
git push -u origin main
```

### 3️⃣ Vercel'e Deploy Et - Frontend (2 dk)

1. **https://vercel.com/signup** - GitHub ile giriş yap
2. **New Project** → GitHub repo'nu seç: `aura-churn-prevention`
3. **Root Directory:** `aura-frontend` yaz
4. **Deploy** butonuna tıkla
5. Deploy tamamlanınca URL'i kopyala (örn: `aura-churn-prevention.vercel.app`)

### 4️⃣ Railway'e Deploy Et - Backend (2 dk)

1. **https://railway.app** - GitHub ile giriş yap
2. **New Project** → **Deploy from GitHub repo**
3. `aura-churn-prevention` seç
4. **Add variables:**
   ```
   PYTHON_VERSION=3.11
   CORS_ORIGINS=https://aura-churn-prevention.vercel.app
   ```
5. **Settings** → **Root Directory:** `aura-backend`
6. Deploy tamamlanınca URL'i kopyala

### 5️⃣ Frontend'i Backend'e Bağla (1 dk)

1. Vercel Dashboard → Project → **Settings** → **Environment Variables**
2. Ekle:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```
3. **Redeploy** butonuna tıkla

---

## 🌐 Domain Bağlama (nativestruct.com)

### Eski Siteyi Kapat

**Eğer Vercel'de ise:**
1. Vercel Dashboard → Eski proje
2. Settings → Domains → `nativestruct.com` → Remove

**Eğer başka yerde ise:**
- GitHub Pages: Settings → Pages → Source: None
- Netlify: Site Settings → Domain Management → Remove

### Yeni Domain Ekle

1. Vercel Dashboard → AURA projesi → **Settings** → **Domains**
2. **Add:** `nativestruct.com`
3. Vercel size DNS ayarlarını gösterecek

### DNS Ayarları (Domain Sağlayıcınızda)

**Seçenek 1: A Record (Hızlı)**
```
Type: A
Host: @
Value: 76.76.21.21
TTL: 3600
```

**Seçenek 2: CNAME (Önerilen)**
```
Type: CNAME
Host: www
Value: cname.vercel-dns.com
TTL: 3600
```

---

## 🎯 Test Et

```bash
# Frontend
curl https://nativestruct.com

# Backend
curl https://your-backend-url.railway.app/api/dashboard/summary
```

---

## 📊 Sonuç

✅ Frontend: `nativestruct.com`
✅ Backend: `your-backend-url.railway.app`
✅ SSL: Otomatik (Let's Encrypt)
✅ Deployment: Otomatik (Git push ile)

---

## 🆘 Sorun mu var?

1. **Vercel Logs:** Dashboard → Deployments → Logs
2. **Railway Logs:** Dashboard → Deployments → View Logs
3. **Detaylı rehber:** `cat DEPLOYMENT_GUIDE.md`

---

## 🎉 Başarılar!

AURA sisteminiz artık canlıda! 🚀
