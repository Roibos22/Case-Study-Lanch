class RestaurantParser:
    def __init__(self, json_data):
        self.data = json_data
        self.slug_to_id = {
            restaurant['primarySlug']: id 
            for id, restaurant in self.data['restaurants'].items()
        }
        self.total_restaurants = len(self.data['restaurants'])
        self.total_delivering = len([r for r in self.data['restaurants'].values() 
                                   if r['supports']['delivery']])
        self.open_delivering_restaurants = self._get_open_delivering_restaurants()
        
    def _get_restaurant_id(self, slug):
        return self.slug_to_id.get(slug)
        
    def _get_rank(self, restaurant_id):
        try:
            return self.data['aggregates']['topRank'].index(restaurant_id) + 1
        except ValueError:
            return None
            
    def _is_restaurant_open(self, restaurant):
        delivery = restaurant['shippingInfo']['delivery']
        pickup = restaurant['shippingInfo']['pickup']
        return delivery['isOpenForOrder'] or pickup['isOpenForOrder']
    
    def _get_open_delivering_restaurants(self):
        open_delivering = []
        for id, restaurant in self.data['restaurants'].items():
            if (self._is_restaurant_open(restaurant) and 
                restaurant['supports']['delivery']):
                open_delivering.append(id)
        return open_delivering
    
    def _get_true_rank(self, restaurant_id):
        if restaurant_id not in self.open_delivering_restaurants:
            return None
        try:
            filtered_list = [r for r in self.data['aggregates']['topRank'] 
                           if r in self.open_delivering_restaurants]
            return filtered_list.index(restaurant_id) + 1
        except ValueError:
            return None
            
    def parse_restaurant(self, slug):
        restaurant_id = self._get_restaurant_id(slug)
        if not restaurant_id:
            return None
            
        restaurant = self.data['restaurants'][restaurant_id]
        
        return {
            'slug': slug,
            'rank': self._get_rank(restaurant_id),
            'true_rank': self._get_true_rank(restaurant_id),
            'sponsored': restaurant['indicators']['isSponsored'],
            'is_open': self._is_restaurant_open(restaurant),
            'total_restaurants': self.total_restaurants,
            'total_delivering': self.total_delivering,
            'total_open_delivering': len(self.open_delivering_restaurants)
        }
        
    def parse_multiple_restaurants(self, slugs):
        results = []
        for slug in slugs:
            result = self.parse_restaurant(slug)
            if result:
                results.append(result)
        return results