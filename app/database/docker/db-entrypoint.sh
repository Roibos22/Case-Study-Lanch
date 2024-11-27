#!/bin/bash
set -e

while ! nc -z db 5432; do
    sleep 1
done

python - << EOF
from app.database.init_db import init_db
init_db()
EOF

exec "$@"