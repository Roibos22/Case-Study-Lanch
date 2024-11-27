from datetime import datetime

class RestaurantParser:
    def __init__(self, json_data):
        self.data = json_data
        self.slug_to_id = {
            restaurant['primarySlug']: id 
            for id, restaurant in self.data['restaurants'].items()
        }
        self.total_restaurants = len(self.data['restaurants'])
        self.restaurants_delivery = [id for id, r in self.data['restaurants'].items()
                                    if r['supports']['delivery']]
        self.restaurants_delivery_open = [id for id, r in self.data['restaurants'].items()
                                    if r['shippingInfo']['delivery']['isOpenForOrder']
                                    and r['supports']['delivery']]

    def parse_restaurant(self, slug):
        restaurant_id = self.slug_to_id.get(slug)
        if not restaurant_id:
            return None

        restaurant = self.data['restaurants'][restaurant_id]
        if not restaurant:
            return None

        return {
            'restaurant_slug': slug,
            'rank': self._get_rank(restaurant_id),
            'rank_overall': self._get_rank_total(restaurant_id),
            'restaurants_delivery': len(self.restaurants_delivery),
            'restaurants_total': self.total_restaurants,
            'is_sponsored': restaurant['indicators']['isSponsored'],
            'is_active': restaurant['shippingInfo']['delivery']['isOpenForOrder'],
            'rating_votes': restaurant['rating']['votes'],
            'rating_score': restaurant['rating']['score'],
            'timestamp': datetime.now().isoformat()
        }

    def _get_rank_total(self, restaurant_id):
        try:
            return self.data['aggregates']['topRank'].index(restaurant_id) + 1
        except ValueError:
            return 0

    def _get_rank(self, restaurant_id):
        if restaurant_id not in self.restaurants_delivery_open:
           return 0
        try:
            filtered_list = [r for r in self.data['aggregates']['topRank'] 
                          if r in self.restaurants_delivery_open]
            return filtered_list.index(restaurant_id) + 1
        except ValueError:
           return 0

