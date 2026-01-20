import requests
from datetime import datetime
import json

class AlAdhanAPI:
    BASE_URL = "http://api.aladhan.com/v1"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_timings_by_city(self, city, country, method=4):
        try:
            url = f"{self.BASE_URL}/timingsByCity"
            params = {
                'city': city,
                'country': country,
                'method': method
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] == 200:
                return data['data']['timings']
            return None
        except Exception as e:
            print(f"Error fetching prayer times: {e}")
            return None
    
    def get_timings_by_coordinates(self, latitude, longitude, method=4):
        try:
            url = f"{self.BASE_URL}/timings"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'method': method
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] == 200:
                return data['data']['timings']
            return None
        except Exception as e:
            print(f"Error fetching prayer times: {e}")
            return None
