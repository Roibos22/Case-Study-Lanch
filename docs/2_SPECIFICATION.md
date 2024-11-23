
---
## Technical Specification
---
#### Rank Retrieval
- Retrieve the rank as displayed to the end user on the Lieferando web app (https://www.lieferando.de/lieferservice/essen/frechen-50226)
- Lieferando requires user to enter address → use address of restaurant to retrieve rank for
- If required, we encourage you to use web scraping technologies
- Retrieve Rank without any filters applied
- Top Result → Rank 1, followed by 2, etc.
- Add any context relevant fields from the result page to the Database

#### Application Requirements
- Use Docker (docker compose up) to start application
- The API should have exactly one endpoint
- No authentication needed
- No routing needed → use http://localhost:8080 as base url

#### API Response Format
```json
{
   "restaurant_slug": "<restaurant_slug>",
   "rank": 4,
   ...
}
```

#### Logging of Ranks
- use python and / or bash script (cron is optional) to log data in db
    - you can hardcode slugs in script
- max 60 minutes interval
- slugs to retrieve:
    ```
    [
        "loco-chicken-i-frechen",
        "loco-chicken-bielefeld",
        "happy-slice-suedstadt",
        "happy-slice-pizza-i-wandsbek-markt",
    ]
    ````

#### Tech Stack
- Language Please use Python for the main application logic
- API Use any Python framework of your choice
- DB Use a relational database with any dialect of your choice
- Containerization Use Docker with docker compose