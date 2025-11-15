#!/bin/bash
# Bu script'i deploy kullanıcısı olarak çalıştırın
# Kullanım: ./deploy_app.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

cd /opt/epica

echo -e "${BLUE}1. Projeyi GitHub'dan çekiyorum...${NC}"
if [ ! -d ".git" ]; then
    git clone https://github.com/ozmenkaya/epica.git .
else
    git pull origin main
fi

echo -e "${BLUE}2. Virtual environment oluşturuluyor...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo -e "${BLUE}3. Python paketleri yükleniyor...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${BLUE}4. .env dosyası oluşturuluyor...${NC}"
if [ ! -f ".env" ]; then
    cp deploy/env.example .env
    
    # SECRET_KEY üret
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    # .env dosyasını düzenle
    sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
    sed -i "s/epica.com.tr,www.epica.com.tr/78.46.162.116/" .env
    sed -i "s|https://epica.com.tr,https://www.epica.com.tr|http://78.46.162.116|" .env
    
    # PostgreSQL ayarları
    cat >> .env << 'EOF'

# PostgreSQL Settings
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=epica_db
DATABASE_USER=epica_user
DATABASE_PASSWORD=epica_password_change_me
DATABASE_HOST=localhost
DATABASE_PORT=5432
EOF
    
    echo -e "${GREEN}.env dosyası oluşturuldu. Lütfen gözden geçirin ve düzenleyin!${NC}"
else
    echo ".env dosyası zaten mevcut"
fi

echo -e "${BLUE}5. Veritabanı migration'ları çalıştırılıyor...${NC}"
python manage.py migrate

echo -e "${BLUE}6. Static dosyalar toplanıyor...${NC}"
python manage.py collectstatic --noinput

echo -e "${BLUE}7. Superuser oluşturun (opsiyonel):${NC}"
echo "python manage.py createsuperuser"

echo -e "${GREEN}=== Uygulama hazır! ===${NC}"
echo ""
echo "Şimdi systemd ve nginx kurulumu için root olarak:"
echo "  sudo bash /opt/epica/deploy/setup_services.sh"
