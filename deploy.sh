#!/bin/bash

# AURA Deployment Script
# Bu script projeyi GitHub'a push etmeye hazırlar

echo "🚀 AURA Deployment Hazırlığı Başlıyor..."
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Gereksiz dosyaları temizle
echo "${YELLOW}📦 Gereksiz dosyalar temizleniyor...${NC}"

# Frontend temizlik
if [ -d "aura-frontend/.next" ]; then
    echo "  - Frontend .next klasörü siliniyor..."
    rm -rf aura-frontend/.next
fi

if [ -d "aura-frontend/node_modules" ]; then
    echo "  - Frontend node_modules siliniyor..."
    rm -rf aura-frontend/node_modules
fi

# Backend temizlik
if [ -d "aura-backend/venv" ]; then
    echo "  - Backend venv siliniyor..."
    rm -rf aura-backend/venv
fi

if [ -d "aura-backend/__pycache__" ]; then
    echo "  - Backend __pycache__ siliniyor..."
    rm -rf aura-backend/__pycache__
fi

# Tüm __pycache__ klasörlerini sil
find aura-backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "${GREEN}✅ Temizlik tamamlandı!${NC}"
echo ""

# 2. Dosya boyutunu kontrol et
echo "${YELLOW}📊 Proje boyutu kontrol ediliyor...${NC}"
TOTAL_SIZE=$(du -sh . | awk '{print $1}')
echo "  Toplam boyut: $TOTAL_SIZE"
echo ""

# 3. .gitignore kontrolü
echo "${YELLOW}📝 .gitignore dosyaları kontrol ediliyor...${NC}"

# Frontend .gitignore
if [ ! -f "aura-frontend/.gitignore" ]; then
    echo "${RED}⚠️  Frontend .gitignore bulunamadı!${NC}"
    echo "  Oluşturuluyor..."
    cat > aura-frontend/.gitignore << 'EOF'
# Dependencies
node_modules
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts
EOF
    echo "${GREEN}✅ Frontend .gitignore oluşturuldu${NC}"
fi

# Backend .gitignore
if [ ! -f "aura-backend/.gitignore" ]; then
    echo "${RED}⚠️  Backend .gitignore bulunamadı!${NC}"
    echo "  Oluşturuluyor..."
    cat > aura-backend/.gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Large files (optional - uncomment if needed)
# *.pkl
# *.csv
# *.json
EOF
    echo "${GREEN}✅ Backend .gitignore oluşturuldu${NC}"
fi

echo ""

# 4. Git durumunu kontrol et
echo "${YELLOW}🔍 Git durumu kontrol ediliyor...${NC}"

if [ ! -d ".git" ]; then
    echo "${RED}⚠️  Git repository bulunamadı!${NC}"
    echo "  Git başlatılıyor..."
    git init
    echo "${GREEN}✅ Git repository oluşturuldu${NC}"
else
    echo "${GREEN}✅ Git repository mevcut${NC}"
fi

echo ""

# 5. Dosyaları stage'e ekle
echo "${YELLOW}📤 Dosyalar Git'e ekleniyor...${NC}"
git add .

# 6. Değişiklikleri göster
echo ""
echo "${YELLOW}📋 Değişiklikler:${NC}"
git status --short

echo ""
echo "${GREEN}✅ Deployment hazırlığı tamamlandı!${NC}"
echo ""
echo "${YELLOW}📝 Sonraki adımlar:${NC}"
echo "  1. Commit yapın:"
echo "     ${GREEN}git commit -m \"Initial commit: AURA System\"${NC}"
echo ""
echo "  2. GitHub repository oluşturun:"
echo "     ${GREEN}https://github.com/new${NC}"
echo ""
echo "  3. Remote ekleyin (KULLANICI_ADIN yerine GitHub kullanıcı adınızı yazın):"
echo "     ${GREEN}git remote add origin https://github.com/KULLANICI_ADIN/aura-churn-prevention.git${NC}"
echo ""
echo "  4. Push edin:"
echo "     ${GREEN}git branch -M main${NC}"
echo "     ${GREEN}git push -u origin main${NC}"
echo ""
echo "  5. Detaylı deployment rehberi için:"
echo "     ${GREEN}cat DEPLOYMENT_GUIDE.md${NC}"
echo ""
