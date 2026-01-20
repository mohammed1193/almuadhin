from datetime import datetime, timedelta
import pytz

class PrayerTimesManager:
    PRAYER_NAMES = {
        'Fajr': 'الفجر',
        'Dhuhr': 'الظهر',
        'Asr': 'العصر',
        'Maghrib': 'المغرب',
        'Isha': 'العشاء'
    }
    
    def __init__(self):
        self.timings = {}
        self.offsets = {
            'Fajr': 0,
            'Dhuhr': 0,
            'Asr': 0,
            'Maghrib': 0,
            'Isha': 0
        }
    
    def set_timings(self, timings_dict):
        self.timings = {
            'Fajr': timings_dict.get('Fajr', ''),
            'Dhuhr': timings_dict.get('Dhuhr', ''),
            'Asr': timings_dict.get('Asr', ''),
            'Maghrib': timings_dict.get('Maghrib', ''),
            'Isha': timings_dict.get('Isha', '')
        }
    
    def apply_offset(self, prayer_name, minutes):
        self.offsets[prayer_name] = minutes
    
    def get_prayer_time(self, prayer_name):
        if prayer_name not in self.timings:
            return None
        
        time_str = self.timings[prayer_name]
        time_obj = datetime.strptime(time_str, "%H:%M")
        
        offset = self.offsets.get(prayer_name, 0)
        adjusted_time = time_obj + timedelta(minutes=offset)
        
        return adjusted_time.strftime("%H:%M")
    
    def get_next_prayer(self):
        now = datetime.now()
        current_time = now.time()
        
        for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
            prayer_time_str = self.get_prayer_time(prayer)
            if prayer_time_str:
                prayer_time = datetime.strptime(prayer_time_str, "%H:%M").time()
                if current_time < prayer_time:
                    return prayer, prayer_time_str
        
        return 'Fajr', self.get_prayer_time('Fajr')
    
    def get_time_remaining(self, prayer_time_str):
        now = datetime.now()
        prayer_datetime = datetime.combine(now.date(), 
                                          datetime.strptime(prayer_time_str, "%H:%M").time())
        
        if prayer_datetime < now:
            prayer_datetime += timedelta(days=1)
        
        remaining = prayer_datetime - now
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        seconds = remaining.seconds % 60
        
        return hours, minutes, seconds
    
    def get_all_timings(self):
        return {prayer: self.get_prayer_time(prayer) for prayer in self.PRAYER_NAMES.keys()}
