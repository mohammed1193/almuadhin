from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from datetime import datetime, timedelta

class PrayerScheduler(QObject):
    prayer_time_reached = pyqtSignal(str, str)
    iqama_time_reached = pyqtSignal(str)
    notification_time = pyqtSignal(str, int)
    
    def __init__(self, prayer_manager, config_manager):
        super().__init__()
        self.prayer_manager = prayer_manager
        self.config_manager = config_manager
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_prayer_times)
        self.timer.start(1000)
        
        self.notified_prayers = set()
        self.played_adhans = set()
        self.played_iqamas = set()
        
        self.last_check_date = datetime.now().date()
    
    def check_prayer_times(self):
        now = datetime.now()
        current_date = now.date()
        
        if current_date != self.last_check_date:
            self.reset_daily_flags()
            self.last_check_date = current_date
        
        current_time = now.time()
        config = self.config_manager.load_config()
        
        for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
            prayer_time_str = self.prayer_manager.get_prayer_time(prayer)
            if not prayer_time_str:
                continue
            
            prayer_time = datetime.strptime(prayer_time_str, "%H:%M").time()
            
            if config['notifications']['enabled']:
                notification_minutes = config['notifications']['before_minutes']
                notification_time = (datetime.combine(current_date, prayer_time) - 
                                   timedelta(minutes=notification_minutes)).time()
                
                if (self._is_time_match(current_time, notification_time) and 
                    f"{prayer}_notif" not in self.notified_prayers):
                    self.notification_time.emit(prayer, notification_minutes)
                    self.notified_prayers.add(f"{prayer}_notif")
            
            if (self._is_time_match(current_time, prayer_time) and 
                prayer not in self.played_adhans):
                
                if config['adhan']['enabled'].get(prayer, True):
                    arabic_name = self.prayer_manager.PRAYER_NAMES.get(prayer, prayer)
                    self.prayer_time_reached.emit(prayer, arabic_name)
                    self.played_adhans.add(prayer)
                    
                    if config['iqama']['enabled']:
                        delay = config['iqama']['delay_minutes']
                        QTimer.singleShot(delay * 60 * 1000, 
                                        lambda p=prayer: self._play_iqama(p))
    
    def _play_iqama(self, prayer):
        if prayer not in self.played_iqamas:
            self.iqama_time_reached.emit(prayer)
            self.played_iqamas.add(prayer)
    
    def _is_time_match(self, current_time, target_time):
        return (current_time.hour == target_time.hour and 
                current_time.minute == target_time.minute and 
                current_time.second < 2)
    
    def reset_daily_flags(self):
        self.notified_prayers.clear()
        self.played_adhans.clear()
        self.played_iqamas.clear()
    
    def force_reset(self):
        self.reset_daily_flags()
