from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal

class SystemTrayIcon(QSystemTrayIcon):
    show_window_signal = pyqtSignal()
    hide_window_signal = pyqtSignal()
    settings_signal = pyqtSignal()
    quit_signal = pyqtSignal()
    
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.create_menu()
        self.activated.connect(self.on_tray_icon_activated)
    
    def create_menu(self):
        menu = QMenu()
        
        show_action = QAction("إظهار", self)
        show_action.triggered.connect(self.show_window_signal.emit)
        menu.addAction(show_action)
        
        hide_action = QAction("إخفاء", self)
        hide_action.triggered.connect(self.hide_window_signal.emit)
        menu.addAction(hide_action)
        
        menu.addSeparator()
        
        settings_action = QAction("الإعدادات", self)
        settings_action.triggered.connect(self.settings_signal.emit)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        quit_action = QAction("خروج", self)
        quit_action.triggered.connect(self.quit_signal.emit)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window_signal.emit()
    
    def show_prayer_notification(self, prayer_name):
        self.showMessage(
            "حان وقت الصلاة",
            f"حان الآن وقت صلاة {prayer_name}",
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )
