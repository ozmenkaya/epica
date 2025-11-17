# Sayfa Yetkileri Sistemi

## Genel Bakış

Epica sistemi, kullanıcılara organizasyon bazında detaylı sayfa yetkileri atama imkanı sunar. Her kullanıcı için hangi sayfalara erişebileceği ve hangi işlemleri yapabileceği özelleştirilebilir.

## Rol Yapısı

### 1. Owner (Sahip)
- **Tüm yetkilere sahiptir**
- Organizasyonu oluşturan kişi
- Diğer kullanıcıların yetkilerini yönetebilir
- Silinemeyen özel rol

### 2. Admin (Yönetici)
- **Varsayılan Yetkiler:**
  - Dashboard
  - Müşteriler (Listeleme, Ekleme, Düzenleme, Silme)
  - Tedarikçiler (Listeleme, Ekleme, Düzenleme, Silme)
  - Talepler (Listeleme, Oluşturma)
  - Teklifler (Listeleme)
  - Siparişler (Listeleme)
  - Ürünler (Listeleme, Yönetim)

- **Kısıtlamalar:**
  - Kategoriler yönetimine erişemez
  - Raporlara erişemez
  - Organizasyon ayarlarını değiştiremez

### 3. Member (Üye)
- **Varsayılan Yetkiler:**
  - Dashboard (Sadece Görüntüleme)
  - Müşteriler (Sadece Listeleme)
  - Tedarikçiler (Sadece Listeleme)
  - Talepler (Sadece Listeleme)

- **Kısıtlamalar:**
  - Hiçbir şey ekleyemez, düzenleyemez veya silemez
  - Sadece görüntüleme yetkileri var

## Sayfa Yetkileri

### Müşteriler
- `customers_list` - Müşteri listesini görüntüleme
- `customers_create` - Yeni müşteri ekleme
- `customers_edit` - Müşteri bilgilerini düzenleme
- `customers_delete` - Müşteri silme

### Tedarikçiler
- `suppliers_list` - Tedarikçi listesini görüntüleme
- `suppliers_create` - Yeni tedarikçi ekleme
- `suppliers_edit` - Tedarikçi bilgilerini düzenleme
- `suppliers_delete` - Tedarikçi silme

### Kategoriler
- `categories_list` - Kategori listesini görüntüleme
- `categories_manage` - Kategori ekleme, düzenleme, silme

### Talepler
- `tickets_list` - Talep listesini görüntüleme
- `tickets_create` - Yeni talep oluşturma

### Teklifler & Siparişler
- `offers_list` - Teklif listesini görüntüleme
- `orders_list` - Sipariş listesini görüntüleme
- `orders_manage` - Sipariş onaylama, düzenleme

### Ürünler
- `products_list` - Ürün listesini görüntüleme
- `products_manage` - Ürün ekleme, düzenleme, silme

### Diğer
- `dashboard` - Dashboard sayfasını görüntüleme
- `reports` - Raporları görüntüleme
- `settings` - Organizasyon ayarlarını değiştirme

## Kullanıcı Ekleme

### Adım 1: Organizasyonlar Sayfasına Git
`https://epica.com.tr/tr/accounts/orgs/`

### Adım 2: Kullanıcılar Butonuna Tıkla
Her organizasyon satırındaki "Kullanıcılar" simgesine tıklayın.

### Adım 3: Yeni Kullanıcı Ekle
1. **Kullanıcı Adı veya E-posta**: Mevcut kullanıcı veya yeni oluşturulacak kullanıcı
2. **E-posta Adresi**: (Opsiyonel) Kullanıcının e-posta adresi
3. **Şifre**: (Opsiyonel) Özel şifre, boş bırakılırsa otomatik oluşturulur
4. **Kullanıcı yoksa yeni oluştur**: Checkbox işaretlenirse otomatik kullanıcı oluşturulur
5. **Rol**: Owner, Admin veya Member
6. **Sayfa Yetkileri**: Hangi sayfalara erişebileceğini seçin

### Adım 4: Yetkileri Özelleştir
- Rol seçildiğinde varsayılan yetkiler otomatik işaretlenir
- İstediğiniz yetkileri checkbox'larla ekleyin veya çıkarın
- Her yetki için açıklama mevcuttur

## Kullanıcı Düzenleme

### Yetkileri Güncelleme
1. Organizasyon → Kullanıcılar → Düzenle
2. Yeni rol seçin (varsayılan yetkiler otomatik yüklenir)
3. Checkbox'larla yetkileri özelleştirin
4. Kaydet

### E-posta ve Şifre Güncelleme
- Düzenleme sayfasından e-posta değiştirilebilir
- Yeni şifre atanabilir

## Erişim Kontrolü

### Yetkisiz Erişim Durumunda
Kullanıcı yetkisi olmayan bir sayfaya gitmeye çalışırsa:

1. **Friendly Error Page** gösterilir
2. Neden erişemediği açıklanır
3. Dashboard'a veya başka sayfalara dönüş linkleri sunulur
4. Organizasyon yöneticisi ile iletişim önerisi yapılır

### Sistem Korumaları
- Portal kullanıcıları (müşteri/tedarikçi) backoffice'e erişemez
- Her view otomatik yetki kontrolü yapar
- Tenant (organizasyon) izolasyonu korunur

## Teknik Detaylar

### Decorator Kullanımı
```python
@page_permission_required('customers_list')
def customers_list(request):
    # Sadece 'customers_list' yetkisi olan kullanıcılar erişebilir
    ...
```

### Yetki Kontrolü
```python
membership = Membership.objects.get(user=user, organization=org)
if membership.has_permission('customers_create'):
    # Kullanıcının yetkisi var
    ...
```

### Özel Yetkiler
```python
# Rol bazlı varsayılan yetkiler + özel yetkiler
membership.custom_permissions = {
    "allowed": ["dashboard", "customers_list", "suppliers_create"]
}
```

## Best Practices

1. **Owner Rolü**: Her organizasyonda en az bir owner bulunmalı
2. **Minimum Yetki Prensibi**: Kullanıcılara sadece ihtiyaç duydukları yetkileri verin
3. **Düzenli Kontrol**: Periyodik olarak kullanıcı yetkilerini gözden geçirin
4. **Test**: Yeni kullanıcı ekledikten sonra yetkilerini test edin

## Örnek Senaryolar

### Senaryo 1: Sadece Görüntüleme Yetkisi
```
Rol: Member
Yetkiler: dashboard, customers_list, suppliers_list, tickets_list
Sonuç: Kullanıcı tüm listeleri görebilir ama hiçbir şey ekleyemez/düzenleyemez
```

### Senaryo 2: Müşteri Yöneticisi
```
Rol: Member
Yetkiler: dashboard, customers_list, customers_create, customers_edit
Sonuç: Kullanıcı sadece müşterilerle ilgili işlem yapabilir
```

### Senaryo 3: Sipariş Sorumlusu
```
Rol: Admin
Yetkiler: dashboard, orders_list, orders_manage, tickets_list
Sonuç: Kullanıcı siparişleri yönetir, diğer alanlara erişemez
```

## Sorun Giderme

### Problem: Kullanıcı erişemiyor
**Çözüm:**
1. Kullanıcının organizasyon üyesi olduğunu kontrol edin
2. Membership kaydının olduğunu doğrulayın
3. Yetkilerin doğru atandığından emin olun

### Problem: Varsayılan yetkiler yüklenmiyor
**Çözüm:**
1. Sayfayı yenileyin
2. Rol dropdown'ını değiştirip tekrar eski role getirin
3. Browser console'da JavaScript hata kontrolü yapın

### Problem: Owner yetkilerini değiştiremiyorum
**Çözüm:**
- Owner rolü sistem tarafından korunur
- Owner'ın tüm yetkileri sabit olarak tanımlıdır
- Bu rol değiştirilemez ve yetkileri düzenlenemez
