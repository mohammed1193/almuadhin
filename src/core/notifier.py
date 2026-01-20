from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QIcon
import platform
from pathlib import Path

class NotificationManager(QObject):
    def __init__(self, tray_icon=None):
        super().__init__()
        self.tray_icon = tray_icon
        self.system = platform.system()
    
    def show_notification(self, title, message, duration=5000):
        try:
            if self.tray_icon and isinstance(self.tray_icon, QSystemTrayIcon):
                # استخدام NoIcon لعرض أيقونة التطبيق من system tray
                self.tray_icon.showMessage(
                    title,
                    message,
                    QSystemTrayIcon.MessageIcon.NoIcon,
                    duration
                )
                return True
            else:
                print(f"Notification: {title} - {message}")
                return False
        except Exception as e:
            print(f"Error showing notification: {e}")
            return False
    
    def show_prayer_notification(self, prayer_name, minutes_before):
        title = "تنبيه الصلاة"
        message = f"باقي {minutes_before} دقيقة على صلاة {prayer_name}"
        self.show_notification(title, message)
    
    def show_adhan_notification(self, prayer_name):
        title = "حان وقت الصلاة"
        message = f"حان الآن وقت صلاة {prayer_name}"
        self.show_notification(title, message, duration=10000)
    
    def show_iqama_notification(self, prayer_name):
        title = "الإقامة"
        message = f"حان وقت إقامة صلاة {prayer_name}"
        self.show_notification(title, message, duration=8000)
    
    def show_error(self, message):
        title = "خطأ"
        self.show_notification(title, message, duration=5000)
    
    def show_success(self, message):
        title = "نجح"
        self.show_notification(title, message, duration=3000)
