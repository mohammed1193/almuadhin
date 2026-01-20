import geocoder

class LocationService:
    def __init__(self):
        self.current_location = None
    
    def get_current_location(self):
        """
        يحصل على الموقع الحالي باستخدام IP
        يرجع: dict مع city, country, latitude, longitude
        """
        try:
            g = geocoder.ip('me')
            if g.ok:
                self.current_location = {
                    'city': g.city or 'Unknown',
                    'country': g.country or 'Unknown',
                    'latitude': g.lat,
                    'longitude': g.lng,
                    'method': 'ip'
                }
                return self.current_location
            return None
        except Exception as e:
            print(f"Error getting location by IP: {e}")
            return None
    
    def get_precise_location(self):
        """
        يحاول الحصول على موقع دقيق باستخدام Windows Location Services
        أو أي خدمة GPS متاحة
        """
        try:
            location = None
            
            try:
                import wmi
                c = wmi.WMI()
                for item in c.Win32_Location():
                    if hasattr(item, 'Latitude') and hasattr(item, 'Longitude'):
                        location = {
                            'latitude': float(item.Latitude),
                            'longitude': float(item.Longitude),
                            'method': 'gps'
                        }
                        break
            except:
                pass
            
            if location:
                location_info = self.reverse_geocode(
                    location['latitude'], 
                    location['longitude']
                )
                if location_info:
                    location.update(location_info)
                    self.current_location = location
                    return location
            
            return self.get_current_location()
            
        except Exception as e:
            print(f"Error getting precise location: {e}")
            return self.get_current_location()
    
    def reverse_geocode(self, latitude, longitude):
        """
        يحول الإحداثيات إلى اسم مدينة ودولة
        """
        try:
            g = geocoder.osm([latitude, longitude], method='reverse')
            if g.ok:
                return {
                    'city': g.city or g.town or g.village or 'Unknown',
                    'country': g.country or 'Unknown'
                }
            return None
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return None
    
    def search_city(self, city_name):
        """
        يبحث عن مدينة ويرجع إحداثياتها
        """
        try:
            g = geocoder.osm(city_name)
            if g.ok:
                return {
                    'city': g.city or city_name,
                    'country': g.country or 'Unknown',
                    'latitude': g.lat,
                    'longitude': g.lng,
                    'method': 'search'
                }
            return None
        except Exception as e:
            print(f"Error searching city: {e}")
            return None
    
    def validate_coordinates(self, latitude, longitude):
        """
        يتحقق من صحة الإحداثيات
        """
        try:
            lat = float(latitude)
            lng = float(longitude)
            
            if -90 <= lat <= 90 and -180 <= lng <= 180:
                return True
            return False
        except:
            return False
    
    def get_location_info(self, latitude, longitude):
        """
        يحصل على معلومات الموقع من الإحداثيات
        """
        if not self.validate_coordinates(latitude, longitude):
            return None
        
        location_info = self.reverse_geocode(latitude, longitude)
        if location_info:
            return {
                'city': location_info['city'],
                'country': location_info['country'],
                'latitude': float(latitude),
                'longitude': float(longitude),
                'method': 'manual'
            }
        
        return {
            'city': 'Unknown',
            'country': 'Unknown',
            'latitude': float(latitude),
            'longitude': float(longitude),
            'method': 'manual'
        }
