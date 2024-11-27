#!/bin/bash
set -e

while ! nc -z db 5432; do
    sleep 1
done

python scripts/run_scraper.py