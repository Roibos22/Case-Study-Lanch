class RestaurantParser:
    def __init__(self, json_data):
        self.data = json_data
        self.slug_to_id = {
            restaurant['primarySlug']: id 
            for id, restaurant in self.data['restaurants'].items()
        }
        self.total_restaurants = len(self.data['restaurants'])
        self.total_restaurants_delivering = len([r for r in self.data['restaurants'].values() 
                                   if r['supports']['delivery']])
        self.restaurants_delivering_open = [id for id, r in self.data['restaurants'].items()
                             if r['shippingInfo']['delivery']['isOpenForOrder']]


    def parse_restaurant(self, slug):
        restaurant_id = self.slug_to_id.get(slug)
        if not restaurant_id:
            return None

        restaurant = self.data['restaurants'][restaurant_id]
        if not restaurant:
            return None

        return {
            'slug': slug,
            'rank': self._get_rank(restaurant_id),
            'rank_total': self._get_rank_total(restaurant_id),
            'total_restaurants': self.total_restaurants,
            'total_restaurants_delivering': self.total_restaurants_delivering,
            'total_restaurants_delivering_open': len(self.restaurants_delivering_open),
            'isSponsored': restaurant['indicators']['isSponsored'],
            'isOpenForOrder': restaurant['shippingInfo']['delivery']['isOpenForOrder']
        }



    def _get_rank_total(self, restaurant_id):
        try:
            return self.data['aggregates']['topRank'].index(restaurant_id) + 1
        except ValueError:
            return 0



    def _get_rank(self, restaurant_id):
        if restaurant_id not in self.restaurants_delivering_open:
           return 0
        try:
            filtered_list = [r for r in self.data['aggregates']['topRank'] 
                          if r in self.restaurants_delivering_open]
            return filtered_list.index(restaurant_id) + 1
        except ValueError:
           return 0

