#!/bin/bash
#
# Create tenant database using SQLite (for development/small deployments)
#
# Usage:
#   ./deploy/create_sqlite_tenant.sh helmex
#   ./deploy/create_sqlite_tenant.sh acme

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <tenant_slug>"
    echo "Example: $0 helmex"
    exit 1
fi

TENANT_SLUG="$1"
DB_PATH="/opt/epica/tenant_dbs/db_${TENANT_SLUG}.sqlite3"
ENV_FILE="/opt/epica/.env"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🗄️  Creating SQLite Tenant Database"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tenant: $TENANT_SLUG"
echo "Database: $DB_PATH"
echo ""

# Create tenant_dbs directory if doesn't exist
mkdir -p /opt/epica/tenant_dbs

# Check if database already exists
if [ -f "$DB_PATH" ]; then
    echo "⚠️  Database already exists: $DB_PATH"
    read -p "Do you want to recreate it? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
    rm "$DB_PATH"
fi

# Create database file
touch "$DB_PATH"
chmod 664 "$DB_PATH"
chown deploy:deploy "$DB_PATH"

echo "✅ Database file created: $DB_PATH"

# Add to .env file
ENV_VAR="TENANT_DB_${TENANT_SLUG^^}"
DB_URL="sqlite:///$DB_PATH"

# Check if already in .env
if grep -q "^${ENV_VAR}=" "$ENV_FILE" 2>/dev/null; then
    echo "⚠️  Environment variable already exists in .env"
    read -p "Do you want to update it? (yes/no): " confirm
    if [ "$confirm" == "yes" ]; then
        # Update existing line
        sed -i "s|^${ENV_VAR}=.*|${ENV_VAR}=${DB_URL}|" "$ENV_FILE"
        echo "✅ Updated $ENV_VAR in .env"
    fi
else
    # Add new line
    echo "" >> "$ENV_FILE"
    echo "# Tenant database: $TENANT_SLUG" >> "$ENV_FILE"
    echo "${ENV_VAR}=${DB_URL}" >> "$ENV_FILE"
    echo "✅ Added $ENV_VAR to .env"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Added to .env:"
echo "$ENV_VAR=$DB_URL"
echo ""

# Run migrations
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 Running Migrations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd /opt/epica
source venv/bin/activate

# Restart Django to load new database config
systemctl restart epica
sleep 2

# Run migrations on new tenant database
python manage.py migrate --database="tenant_${TENANT_SLUG}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Tenant Database Created Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access via:"
echo "   - https://${TENANT_SLUG}.epica.com.tr/"
echo "   - https://epica.com.tr/?org=${TENANT_SLUG}"
echo ""
echo "🔧 Next steps:"
echo "   1. Create an Organization with slug '${TENANT_SLUG}' in Django admin"
echo "   2. Access the tenant subdomain"
echo "   3. Data will be isolated in: $DB_PATH"
echo ""
