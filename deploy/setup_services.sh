#!/bin/bash
# Gunicorn ve Nginx servislerini kurar
# Root olarak çalıştırın: sudo bash setup_services.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1. Gunicorn systemd servisi kuruluyor...${NC}"
cp /opt/epica/deploy/systemd/epica.service /etc/systemd/system/epica.service

# Systemd dosyasını IP için güncelle
sed -i 's/127.0.0.1:8001/127.0.0.1:8000/' /etc/systemd/system/epica.service

systemctl daemon-reload
systemctl enable epica
systemctl start epica
systemctl status epica --no-pager

echo -e "${BLUE}2. Nginx yapılandırması kuruluyor...${NC}"
cp /opt/epica/deploy/nginx/epica /etc/nginx/sites-available/epica

# Nginx dosyasını IP için güncelle
sed -i 's/lethe.com.tr www.lethe.com.tr/78.46.162.116/' /etc/nginx/sites-available/epica
sed -i 's/127.0.0.1:8001/127.0.0.1:8000/' /etc/nginx/sites-available/epica

# Site'ı aktif et
ln -sf /etc/nginx/sites-available/epica /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Nginx test
nginx -t

# Nginx'i başlat
systemctl restart nginx
systemctl status nginx --no-pager

echo -e "${GREEN}=== Servisler kuruldu! ===${NC}"
echo ""
echo "Uygulamanız şu adreste çalışıyor:"
echo "  http://78.46.162.116"
echo ""
echo "Logları kontrol etmek için:"
echo "  sudo journalctl -u epica -f"
echo "  sudo tail -f /var/log/nginx/error.log"
