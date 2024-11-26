#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
    sleep 1
done

echo "Database is ready!"

echo "Running scraper..."
python scripts/run_scraper.py