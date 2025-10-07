# Epica SaaS Starter (Django)

Basit bir Django tabanlı SaaS başlangıç projesi.

## Kurulum

```bash
# Sanal ortam (opsiyonel)
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıklar
python -m pip install -r requirements.txt

# Ortam değişkenleri
cp .env.example .env

# Veritabanı
python manage.py migrate
python manage.py runserver
```

## Docker (PostgreSQL ile)

```bash
docker compose up --build
```

## Test

```bash
pytest -q
```

## Format/Lint

```bash
pre-commit install
pre-commit run --all-files
```
