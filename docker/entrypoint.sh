#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "Database is ready!"

echo "Initializing database..."
python - << EOF
from app.main import init_db
init_db()
EOF

echo "Waiting 10 seconds before starting the script..."
sleep 10

echo "Starting script..."
python scripts/run_scraper.py