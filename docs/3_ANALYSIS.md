
---
## Analysis and Research
---

#### Lieferando Web Page

- Looked for Lieferando’s API’s
- Investigated Site: https://www.lieferando.de/lieferservice/essen/frechen-50226
    - No pagination → makes scraping easier
    - Restaurant classes are lazy in HTML → we need to scroll down first
    - Looked for API endpoint that returns List of restaurants
        - Found an [endpoint](https://cw-api.takeaway.com/api/v34/restaurants?deliveryAreaId=1213069&postalCode=50226&lat=50.913583442425406&lng=6.784137236111377&limit=0&isAccurate=true&filterShowTestRestaurants=false), but restaurants do not have same order as on page
            - Looked for sorting algorithm in network tab, but did not find anything
            - Also found [article](https://www.lieferando.de/kundenservice/artikel/wie-ist-die-restaurantliste-organisiert-1?topicSlug=restaurantliste) about Lieferando’s sorting mechanism, but it’s not conclusive
    - Finally found topRank at end of the response -> we just need to connect to this endpoint and should get all data we need

#### What Database to use?
- PostgereSQL
    - handles database operations
- pydantic
    - define schemas
    - validates and serializes data
- sqlalchemy
    - define databse schemas

- easy setup and integration together with fastAPI

#### What Framework to use for the API?
**FastAPI**
- built in json handling
- super easy to setup
- auto generating docs
- async
- good integration with db frameworks

#### Key Data Points to track
1. Tracked:
- slug - string -  Restaurant's unique identifier/name
- rank - int - Current position on delivery page (only restarants that are ['shippingInfo']['delivery']['isOpenForOrder'])
- rank_overall - int - Position among all restaurants
- open_restaurants_delivery - int - Number of open restaurants on delivery page
- restaurants_total - int - Total number of restaurants
- is_sponsored - bool - Whether restaurant has paid promotion
- is_active - bool - Whether currently in business hours
- rating_votes - int - Total number of customer reviews
- rating_score - float - Average customer rating score
- timestamp - datetime - When data was recorded

2. Possible Further Data Points:
- pickup_rank, pickup_restaurants, ...
- promotion, delivery_fee, price_range, ...

#### Possible Limitations and Constraints
**Rate Limiting**:
- API request limits unknown
    - Implement backoff strategy
- IP blocking possible
    - rotate IPs
    - rotating user agents
    - get real cookies and session

