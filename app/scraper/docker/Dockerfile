FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

COPY app/scraper/docker/scraper-entrypoint.sh /scraper-entrypoint.sh
RUN chmod +x /scraper-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/scraper-entrypoint.sh"]
