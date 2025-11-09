#!/bin/bash
# Hetzner Epica Deployment Script
# Server: 78.46.162.116

set -e  # Exit on error

echo "=== Hetzner Epica Deployment Script ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Sistem güncellemeleri yapılıyor...${NC}"
apt update && apt upgrade -y

echo -e "${BLUE}2. Gerekli paketler kuruluyor...${NC}"
apt install -y python3 python3-venv python3-pip nginx git postgresql postgresql-contrib certbot python3-certbot-nginx ufw

echo -e "${BLUE}3. Firewall yapılandırması...${NC}"
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo -e "${BLUE}4. Deploy kullanıcısı oluşturuluyor...${NC}"
if id "deploy" &>/dev/null; then
    echo "deploy kullanıcısı zaten mevcut"
else
    adduser --disabled-password --gecos "" deploy
    usermod -aG sudo deploy
    echo "deploy ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/deploy
fi

echo -e "${BLUE}5. PostgreSQL veritabanı oluşturuluyor...${NC}"
sudo -u postgres psql -c "CREATE DATABASE epica_db;" 2>/dev/null || echo "Database zaten mevcut"
sudo -u postgres psql -c "CREATE USER epica_user WITH PASSWORD 'epica_password_change_me';" 2>/dev/null || echo "User zaten mevcut"
sudo -u postgres psql -c "ALTER ROLE epica_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE epica_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE epica_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE epica_db TO epica_user;"

echo -e "${BLUE}6. Proje dizini hazırlanıyor...${NC}"
mkdir -p /opt/epica
chown deploy:deploy /opt/epica

echo -e "${BLUE}7. SSH key'i deploy kullanıcısına kopyalanıyor...${NC}"
mkdir -p /home/deploy/.ssh
cp /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys 2>/dev/null || echo "SSH key henüz yüklenmemiş"
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys 2>/dev/null || true

echo -e "${GREEN}=== Sistem hazır! ===${NC}"
echo ""
echo "Şimdi deploy kullanıcısı ile devam edin:"
echo "  su - deploy"
echo ""
echo "Sonraki adımlar:"
echo "  1. cd /opt/epica"
echo "  2. git clone https://github.com/ozmenkaya/epica.git ."
echo "  3. python3 -m venv venv"
echo "  4. source venv/bin/activate"
echo "  5. pip install -r requirements.txt"
