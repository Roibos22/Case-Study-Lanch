# Case-Study-Lanch

### Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Installation Guide](#installation-guide)
5. [Notes](#notes)

---

## Project Overview
This Application tracks restaurant rankings on Lieferando. Built as a technical case study at Lanch. It provides:

- Real-time ranking via API endpoint
- Automated tracking every 60 minutes
- Historical data storage
- Docker-based deployment
- Type-safe data pipeline using Pydantic
- PostgreSQL for time-series data

---

## Key Features

#### Real-time Rank Retrieval

- GET http://localhost:8080/rank/{restaurant-slug}
- Response:
```json
{
    "restaurant_slug": "example-restaurant",
    "rank": 4,
    "rank_overall": 6,
    "restaurants_total": 130,
    "restaurants_delivery": 100,
    "is_sponsored": true,
    "is_active": true,
    "rating_votes": 129,
    "rating_score": 4.5,
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Automated Monitoring

- 60-minute interval tracking with cron job
- Configurable restaurant list
- Data Storage

---

## Tech Stack

- Python 3.11
- FastAPI, SQLAlchemy, Pydantic
- PostgreSQL
- Docker & Docker Compose

---

## Installation Guide

#### Prerequisites

- Docker & Docker Compose

#### Installation and Usage

```bash
git clone https://github.com/Roibos22/Case-Study-Lanch
cd Case-Study-Lanch
docker-compose up
```

---

## Notes

Development process and analysis in /docs:
```
/docs/
├── 1_REQUIREMENTS.md
├── 2_SPECIFICATION.md
├── 3_ANALYSIS.md
├── 4_DESIGN.md
└── 5_OUTLOOK.md
```