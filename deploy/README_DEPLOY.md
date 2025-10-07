# Epica Production Deployment (Ubuntu/Nginx/Gunicorn)

This guide sets up Epica under /opt/epica with systemd (gunicorn) and nginx.

Prerequisites
- Ubuntu 22.04+ with sudo
- DNS A records for lethe.com.tr and www.lethe.com.tr pointing to the server
- A non-root user with sudo privileges

Paths
- Project root: /opt/epica
- Virtualenv: /opt/epica/.venv
- Static files: /opt/epica/staticfiles
- Media uploads: /opt/epica/media

1) System packages
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx
```

2) Project sync
Ensure /opt/epica contains the project (use git clone or rsync). Set owner if using www-data:
```bash
sudo mkdir -p /opt/epica
sudo chown -R $USER:$USER /opt/epica
# copy or clone your code into /opt/epica
```

3) Python venv and requirements
```bash
cd /opt/epica
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
```

4) Environment (.env)
Copy and edit:
```bash
cp deploy/env.example /opt/epica/.env
```
Edit .env values (SECRET_KEY, ALLOWED_HOSTS, etc.).

5) Migrate and collect static
```bash
source /opt/epica/.venv/bin/activate
cd /opt/epica
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

6) Systemd (gunicorn)
Create service file and enable:
```bash
sudo cp deploy/systemd/epica.service /etc/systemd/system/epica.service
sudo systemctl daemon-reload
sudo systemctl enable epica
sudo systemctl start epica
sudo systemctl status epica --no-pager
```

7) Nginx
Create site config and enable:
```bash
sudo cp deploy/nginx/epica /etc/nginx/sites-available/epica
sudo ln -s /etc/nginx/sites-available/epica /etc/nginx/sites-enabled/epica
sudo nginx -t
sudo systemctl reload nginx
```

8) TLS (Let’s Encrypt)
```bash
sudo certbot --nginx -d lethe.com.tr -d www.lethe.com.tr --redirect -m YOUR_EMAIL@example.com --agree-tos -n
```

9) Smoke tests
```bash
curl -I http://127.0.0.1
curl -I https://lethe.com.tr
curl -I https://www.lethe.com.tr
```

Troubleshooting
- View app logs: `sudo journalctl -u epica -f`
- Check nginx logs: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- Update service after code change: `sudo systemctl restart epica`
