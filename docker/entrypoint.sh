#!/bin/bash

set -e

echo "⏳ Waiting for database..."
./wait-for-it.sh db 3306 echo "DB is up"

echo "📦 Applying database migrations..."
export FLASK_APP=run.py
flask db migrate -m "initial migration"

echo "🛠️ Running flask db upgrade..."
flask db upgrade
echo "✅ Migrations applied successfully."


echo "👤 Creating admin (if not exist)..."
python /init_admin.py || {
    echo "❌ Error while creating admin.";
    exit 1;
}

echo "🏃‍♂️ Starting app..."
exec gunicorn -w 4 -b 0.0.0.0:8000 run:app
