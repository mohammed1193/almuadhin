from PyQt6.QtGui import QFontDatabase, QFont
from pathlib import Path

class FontLoader:
    def __init__(self):
        self.fonts_loaded = False
        self.tajawal_font = None
    
    def load_tajawal_font(self):
        """
        يحمل خط تجوال من مجلد resources/fonts
        """
        try:
            fonts_path = Path(__file__).parent.parent.parent / "resources" / "fonts"
            
            font_files = [
                "Tajawal-Regular.ttf",
                "Tajawal-Bold.ttf",
                "Tajawal-Medium.ttf",
                "Tajawal-Light.ttf"
            ]
            
            loaded_count = 0
            for font_file in font_files:
                font_path = fonts_path / font_file
                if font_path.exists():
                    font_id = QFontDatabase.addApplicationFont(str(font_path))
                    if font_id != -1:
                        loaded_count += 1
            
            if loaded_count > 0:
                self.fonts_loaded = True
                self.tajawal_font = "Tajawal"
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error loading Tajawal font: {e}")
            return False
    
    def get_font(self, size=12, weight=QFont.Weight.Normal):
        """
        يرجع خط تجوال إذا كان محملاً، وإلا يرجع Arial
        """
        if self.fonts_loaded and self.tajawal_font:
            return QFont(self.tajawal_font, size, weight)
        else:
            return QFont("Arial", size, weight)
    
    def is_loaded(self):
        return self.fonts_loaded
