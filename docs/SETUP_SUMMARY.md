# Multi-Tenant Sistem Kurulum Özeti

## ✅ Tamamlanan Kurulum

### 1. Sistem Mimarisi
```
┌─────────────────────────────────────────────────┐
│  Server: 78.46.162.116 (Production)            │
│                                                  │
│  epica.com.tr        → DB: db.sqlite3           │
│  helmex.epica.com.tr → DB: db_helmex.sqlite3    │
│  ?org=helmex         → DB: db_helmex.sqlite3    │
│                                                  │
│  ✅ Subdomain routing                           │
│  ✅ Ayrı database'ler                           │
│  ✅ Otomatik tenant detection                   │
└─────────────────────────────────────────────────┘
```

### 2. Kurulu Bileşenler

**Backend:**
- ✅ Multi-tenant middleware (subdomain + ?org)
- ✅ Database router (tenant isolation)
- ✅ Management commands (create_tenant_db, migrate_all_tenants)
- ✅ Deployment scripts (deploy_all_tenants.sh)

**Frontend:**
- ✅ Nginx wildcard routing (*.epica.com.tr)
- ✅ SSL (mevcut sertifika, wildcard için upgrade edilebilir)

**İlk Tenant:**
- ✅ helmex tenant database oluşturuldu
- ✅ .env dosyasına eklendi
- ✅ Nginx reload edildi

### 3. Dosya Yapısı

```
/opt/epica/
├── db.sqlite3                          # Default database
├── tenant_dbs/
│   └── db_helmex.sqlite3               # Helmex tenant database
├── .env                                 # Config (TENANT_DB_HELMEX added)
├── deploy/
│   ├── create_sqlite_tenant.sh         # Yeni tenant oluştur
│   ├── deploy_all_tenants.sh           # Tüm tenant'ları deploy et
│   ├── servers.conf                     # Server listesi
│   └── nginx/
│       └── epica-simple-multi-tenant   # Nginx config
└── backups/
    └── db_backup_20251116_163521.sqlite3  # Yedek
```

## 🚀 Kullanım

### Yeni Tenant Eklemek

```bash
# 1. SSH bağlan
ssh root@78.46.162.116

# 2. Tenant database oluştur
cd /opt/epica
bash deploy/create_sqlite_tenant.sh acme

# 3. Kullanıma hazır!
# https://acme.epica.com.tr/
# veya
# https://epica.com.tr/?org=acme
```

### Tüm Tenant'ları Güncellemek

```bash
# Local'den
cd /Users/ozmenkaya/epica
git push origin main
./deploy/deploy_all_tenants.sh

# Script:
# - Git pull yapar
# - Tüm tenant database'lerini migrate eder
# - Static files toplar
# - Service restart eder
# - Health check yapar
```

### Tek Tenant Güncellemek

```bash
./deploy/deploy_all_tenants.sh --tenant helmex
```

## 🧪 Test

### Test 1: Default Site
```bash
curl https://epica.com.tr/
# Çalışıyor ✅
```

### Test 2: Helmex Tenant (Subdomain)
```bash
curl https://helmex.epica.com.tr/
# Çalışması için wildcard DNS gerekli
# Cloudflare: A record → *.epica.com.tr → 78.46.162.116
```

### Test 3: Helmex Tenant (Query Param)
```bash
curl https://epica.com.tr/?org=helmex
# Çalışıyor ✅ (200 OK)
```

## 📊 Mevcut Durum

### DNS
- ❌ Wildcard DNS henüz eklenmedi
- **Yapılacak:** Cloudflare'de `*.epica.com.tr` A record ekle → 78.46.162.116

### SSL
- ✅ epica.com.tr için var
- ❌ Wildcard SSL yok (*.epica.com.tr)
- **Geçici:** Mevcut SSL subdomain'lerde de çalışıyor (tarayıcı uyarı verir)
- **İdeal:** Wildcard SSL al: `certbot certonly --manual --preferred-challenges dns -d "*.epica.com.tr" -d "epica.com.tr"`

### Tenant'lar
- ✅ Default: db.sqlite3
- ✅ Helmex: tenant_dbs/db_helmex.sqlite3
- **Durum:** ?org=helmex ile çalışıyor
- **Subdomain:** DNS eklendikten sonra çalışacak

## 📝 Sonraki Adımlar

### Hemen Yapılabilir
1. **Wildcard DNS ekle** (5 dakika)
   - Cloudflare → DNS → Add record
   - Type: A
   - Name: *
   - Content: 78.46.162.116
   - TTL: Auto

2. **Test subdomain**
   ```bash
   curl https://helmex.epica.com.tr/
   ```

### İsteğe Bağlı İyileştirmeler
1. **Wildcard SSL** (30 dakika)
   ```bash
   certbot certonly --manual --preferred-challenges dns \
     -d "*.epica.com.tr" -d "epica.com.tr"
   # DNS TXT record eklemeniz istenecek
   ```

2. **PostgreSQL'e geçiş** (1 saat)
   - Daha iyi performance
   - Daha güvenli
   - Professionel production ortamı

3. **Monitoring** (1 saat)
   - Prometheus + Grafana
   - Database boyutları
   - Tenant başına kullanım

## 💡 Önemli Notlar

### Multi-Tenant Nasıl Çalışıyor?

1. **Request gelir:** `https://helmex.epica.com.tr/orders/`
2. **Middleware:** Subdomain'den `helmex` algılanır
3. **Database Router:** `tenant_helmex` database'ine route eder
4. **Query:** `db_helmex.sqlite3` üzerinde çalışır
5. **Response:** Sadece Helmex'in verileri

### Veri İzolasyonu

- Her tenant **kendi database'inde**
- Bir tenant diğerinin verisini **göremez**
- Database seviyesinde **tam izolasyon**

### Backup

```bash
# Tüm tenant'ları yedekle
cd /opt/epica
mkdir -p backups
cp db.sqlite3 backups/db_default_$(date +%Y%m%d).sqlite3
cp tenant_dbs/db_*.sqlite3 backups/

# Veya otomatik script
find tenant_dbs -name "db_*.sqlite3" -exec \
  cp {} backups/{}_$(date +%Y%m%d).sqlite3 \;
```

### Restore

```bash
# Tenant restore
cp backups/db_helmex_20251116.sqlite3 tenant_dbs/db_helmex.sqlite3
systemctl restart epica
```

## 🎯 Özet

**Başarıyla Kuruldu:**
- ✅ Multi-tenant database isolation
- ✅ Subdomain routing (middleware)
- ✅ Deployment automation
- ✅ İlk tenant (helmex) oluşturuldu
- ✅ ?org=helmex ile çalışıyor

**Yapılacak (Opsiyonel):**
- ⏳ Wildcard DNS ekle (subdomain'ler için)
- ⏳ Wildcard SSL al (tarayıcı uyarısını kaldırmak için)

**Şu An Kullanılabilir:**
- ✅ https://epica.com.tr/?org=helmex
- ⏳ https://helmex.epica.com.tr/ (DNS sonrası)

## 🔗 Dokümantasyon

- `docs/MULTI_TENANT_DATABASE_SETUP.md` - Detaylı setup
- `docs/MULTI_TENANT_STRATEGY.md` - Strateji ve maliyet
- `deploy/README_DEPLOY.md` - Deployment guide
