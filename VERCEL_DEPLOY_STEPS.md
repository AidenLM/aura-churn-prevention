# 🚀 Vercel Deployment - Adım Adım Rehber

## 1️⃣ Vercel'e Giriş Yap (30 saniye)

1. Tarayıcıda aç: **https://vercel.com/signup**
2. **"Continue with GitHub"** butonuna tıkla
3. GitHub hesabınla giriş yap (AidenLM)
4. Vercel'in GitHub'a erişim izni iste → **"Authorize Vercel"**

---

## 2️⃣ Yeni Proje Oluştur (1 dakika)

1. Vercel Dashboard'da **"Add New..."** butonuna tıkla
2. **"Project"** seç
3. **"Import Git Repository"** bölümünde:
   - `AidenLM/aura-churn-prevention` repository'sini bul
   - **"Import"** butonuna tıkla

---

## 3️⃣ Proje Ayarları (2 dakika)

### Framework Preset
- Otomatik algılanacak: **Next.js** ✅

### Root Directory
- **ÖNEMLİ:** `aura-frontend` yaz
- **"Edit"** butonuna tıkla → `aura-frontend` yaz → **"Continue"**

### Build and Output Settings
Otomatik dolacak, kontrol et:
```
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### Environment Variables
**ŞİMDİLİK BOŞ BIRAK** - Backend deploy olduktan sonra ekleyeceğiz.

---

## 4️⃣ Deploy Et! (3-5 dakika)

1. **"Deploy"** butonuna tıkla
2. Vercel build işlemini başlatacak:
   - ✅ Installing dependencies...
   - ✅ Building...
   - ✅ Deploying...
3. **"Congratulations!"** mesajını gördüğünde tamamdır! 🎉

---

## 5️⃣ URL'i Kopyala

Deploy tamamlandığında:
1. **"Visit"** butonuna tıkla veya
2. URL'i kopyala (örn: `aura-churn-prevention.vercel.app`)

**NOT:** Şu anda backend olmadığı için API çağrıları hata verecek. Bu normal! ✅

---

## 6️⃣ Railway'e Backend Deploy (5 dakika)

### Adım 6.1: Railway'e Giriş
1. **https://railway.app** adresine git
2. **"Login with GitHub"** ile giriş yap

### Adım 6.2: Yeni Proje
1. **"New Project"** butonuna tıkla
2. **"Deploy from GitHub repo"** seç
3. `aura-churn-prevention` repository'sini seç
4. **"Deploy Now"** tıkla

### Adım 6.3: Environment Variables Ekle
1. Proje açıldıktan sonra **"Variables"** sekmesine git
2. **"New Variable"** butonuna tıkla
3. Şu değişkenleri ekle:

```bash
PYTHON_VERSION=3.11
DATABASE_URL=sqlite:///./aura_dev.db
CORS_ORIGINS=https://aura-churn-prevention.vercel.app
```

(Her birini ayrı ayrı ekle)

### Adım 6.4: Root Directory Ayarla
1. **"Settings"** sekmesine git
2. **"Service"** bölümünde **"Root Directory"** bul
3. `aura-backend` yaz
4. **"Update"** tıkla

### Adım 6.5: Start Command Ayarla
1. Hala **"Settings"** sekmesinde
2. **"Deploy"** bölümünde **"Start Command"** bul
3. Şunu yaz:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
4. **"Update"** tıkla

### Adım 6.6: Backend URL'ini Kopyala
1. **"Settings"** → **"Networking"** → **"Public Networking"**
2. **"Generate Domain"** butonuna tıkla (eğer yoksa)
3. URL'i kopyala (örn: `aura-backend-production-xxxx.up.railway.app`)

---

## 7️⃣ Frontend'i Backend'e Bağla (2 dakika)

### Adım 7.1: Vercel'e Dön
1. Vercel Dashboard → `aura-churn-prevention` projesi
2. **"Settings"** sekmesine git
3. Sol menüden **"Environment Variables"** seç

### Adım 7.2: API URL Ekle
1. **"Add New"** butonuna tıkla
2. **Name:** `NEXT_PUBLIC_API_URL`
3. **Value:** Railway'den kopyaladığın URL (örn: `https://aura-backend-production-xxxx.up.railway.app`)
4. **Environment:** All (Production, Preview, Development) seç
5. **"Save"** butonuna tıkla

### Adım 7.3: Redeploy
1. **"Deployments"** sekmesine git
2. En üstteki deployment'ın sağındaki **"..."** menüsüne tıkla
3. **"Redeploy"** seç
4. **"Redeploy"** butonuna tıkla

---

## 8️⃣ Domain Bağla (nativestruct.com) - 5 dakika

### Adım 8.1: Eski Siteyi Kapat

**GitHub Pages'i kapat:**
1. GitHub'da eski repository'ye git (AidenLM.github.io veya başka)
2. **Settings** → **Pages**
3. **Source:** **None** seç
4. **Save**

### Adım 8.2: Vercel'de Domain Ekle
1. Vercel Dashboard → AURA projesi
2. **"Settings"** → **"Domains"**
3. **"Add"** butonuna tıkla
4. `nativestruct.com` yaz
5. **"Add"** butonuna tıkla

### Adım 8.3: DNS Ayarları

Vercel size DNS ayarlarını gösterecek. Domain sağlayıcında (GoDaddy, Namecheap, vs.):

#### A Record Ekle:
```
Type: A
Name: @ (veya boş)
Value: 76.76.21.21
TTL: 3600
```

#### CNAME Record Ekle:
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

#### Eski Kayıtları Sil:
- Resimde gördüğüm `185.199.x.x` IP'lerini sil
- Eski `AidenLM.github.io` CNAME'i sil

### Adım 8.4: Bekle
- DNS değişiklikleri 5-30 dakika sürebilir
- Vercel otomatik SSL sertifikası oluşturacak (Let's Encrypt)

---

## 9️⃣ Test Et! (1 dakika)

### Frontend Test:
```bash
# Tarayıcıda aç:
https://aura-churn-prevention.vercel.app
```

### Backend Test:
```bash
# Terminal'de:
curl https://your-backend-url.railway.app/api/dashboard/summary
```

### Domain Test (DNS yayıldıktan sonra):
```bash
# Tarayıcıda aç:
https://nativestruct.com
```

---

## ✅ Checklist

- [ ] Vercel'e giriş yaptım
- [ ] Frontend deploy oldu
- [ ] Railway'e backend deploy oldu
- [ ] Environment variables ekledim
- [ ] Frontend'i backend'e bağladım
- [ ] Domain ekledim
- [ ] DNS ayarlarını güncelledim
- [ ] Site çalışıyor! 🎉

---

## 🆘 Sorun Giderme

### "Module not found" hatası
**Çözüm:** Root Directory'nin `aura-frontend` olduğundan emin ol

### "API call failed" hatası
**Çözüm:** 
1. Railway backend'in çalıştığını kontrol et
2. Vercel Environment Variables'da `NEXT_PUBLIC_API_URL` doğru mu kontrol et
3. CORS_ORIGINS Railway'de doğru mu kontrol et

### Domain çalışmıyor
**Çözüm:**
1. DNS değişiklikleri 30 dakika sürebilir
2. https://dnschecker.org adresinde kontrol et
3. Eski DNS kayıtlarını sildiğinden emin ol

### Backend 500 hatası
**Çözüm:**
1. Railway Logs'a bak: Dashboard → Deployments → View Logs
2. Database ve model dosyalarının yüklendiğinden emin ol

---

## 🎉 Tebrikler!

AURA sisteminiz artık canlıda! 

- Frontend: `https://nativestruct.com`
- Backend: `https://your-backend-url.railway.app`
- GitHub: `https://github.com/AidenLM/aura-churn-prevention`

Her git push yaptığında otomatik deploy olacak! 🚀
