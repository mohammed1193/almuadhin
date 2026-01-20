import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".almuadhin"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
        self.default_config = {
            "location": {
                "city": "Riyadh",
                "country": "Saudi Arabia",
                "latitude": None,
                "longitude": None,
                "use_coordinates": False,
                "method": "city"
            },
            "calculation_method": 4,
            "offsets": {
                "Fajr": 0,
                "Dhuhr": 0,
                "Asr": 0,
                "Maghrib": 0,
                "Isha": 0
            },
            "adhan": {
                "enabled": {
                    "Fajr": True,
                    "Dhuhr": True,
                    "Asr": True,
                    "Maghrib": True,
                    "Isha": True
                },
                "sound_file": "default_adhan.mp3",
                "volume": 80
            },
            "iqama": {
                "enabled": False,
                "delay_minutes": 15,
                "sound_file": "default_iqama.mp3"
            },
            "notifications": {
                "enabled": True,
                "before_minutes": 10
            },
            "appearance": {
                "theme": "light",
                "language": "ar",
                "font_size": 12
            },
            "startup": {
                "run_on_startup": False,
                "minimize_to_tray": True
            }
        }
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**self.default_config, **config}
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self, config):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path, default=None):
        config = self.load_config()
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        config = self.load_config()
        keys = key_path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return self.save_config(config)
