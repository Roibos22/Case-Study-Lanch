
---
## Analysis and Research
---

#### Lieferando Web Page

- Looked for Lieferando’s API’s, nothing of course
- Investigated Site: https://www.lieferando.de/lieferservice/essen/frechen-50226
    - Looked for API endpoint that returns List of restaurants
        - Found an [endpoint](https://cw-api.takeaway.com/api/v34/restaurants?deliveryAreaId=1213069&postalCode=50226&lat=50.913583442425406&lng=6.784137236111377&limit=0&isAccurate=true&filterShowTestRestaurants=false), but restaurants do not have same order as on page
            - Looked for sorting algorithm in network tab, but did not find anything
            - Also found [article](https://www.lieferando.de/kundenservice/artikel/wie-ist-die-restaurantliste-organisiert-1?topicSlug=restaurantliste) about Lieferando’s sorting mechanism, but it’s not conclusive
            - To use this endpoint would need to reverse engineer sorting algorithm (would be overkill)
    - No pagination → makes scraping easier
    - Restaurant classes are lazy in HTML → we need to scroll down first

#### What Scraping Framework to use?

#### What Database to use?

#### What Framewor to use for the API?

#### Key Data Points to track
- sponsored, ...
- list all possible data points

#### Possible Limitations and Constraints
- Rate Limit
- 
