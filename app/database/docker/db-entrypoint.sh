#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
    sleep 1
done

echo "Database is ready!"

echo "Initializing database..."
python - << EOF
from app.database.init_db import init_db
init_db()
EOF

echo "Starting API server..."
exec "$@"