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

COPY app/database/docker/db-entrypoint.sh /db-entrypoint.sh
RUN chmod +x /db-entrypoint.sh

ENTRYPOINT ["/db-entrypoint.sh"]