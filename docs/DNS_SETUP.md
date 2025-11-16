# Wildcard DNS Kurulumu (BIND)

## ✅ Tamamlandı

### DNS Server
- BIND9 çalışıyor: `78.46.162.116`
- Zone file: `/etc/bind/db.epica.com.tr`
- Nameservers: ns1.epica.com.tr, ns2.epica.com.tr

### Wildcard DNS Eklendi
```
*       IN      A       78.46.162.116
```

### Test
```bash
dig @78.46.162.116 helmex.epica.com.tr +short
# 78.46.162.116

dig @78.46.162.116 acme.epica.com.tr +short
# 78.46.162.116
```

### Web Test
- ✅ http://helmex.epica.com.tr/ (200 OK)
- ✅ http://acme.epica.com.tr/ (200 OK)  
- ✅ http://test123.epica.com.tr/ (200 OK)

## Konfigürasyon

### ALLOWED_HOSTS (.env)
```
ALLOWED_HOSTS=epica.com.tr,www.epica.com.tr,.epica.com.tr,78.46.162.116,localhost,127.0.0.1
```

### Nginx (Geçici HTTP-Only)
```
/etc/nginx/sites-available/epica-test
```

## NOT: SSL İçin

Wildcard SSL sertifikası almak için:
```bash
certbot certonly --manual --preferred-challenges dns \
  -d "*.epica.com.tr" -d "epica.com.tr"
```

Sonra nginx'i SSL versiyonuna geri çevir:
```bash
ln -sf /etc/nginx/sites-available/epica /etc/nginx/sites-enabled/
systemctl reload nginx
```
