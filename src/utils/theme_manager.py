from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
    
    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        
        if theme_name == "dark":
            return self.get_dark_theme()
        else:
            return self.get_light_theme()
    
    def get_light_theme(self):
        return """
            QMainWindow, QDialog, QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
                color: #212121;
            }
            
            QLabel {
                color: #212121;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 8px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45A049;
            }
            
            QPushButton:pressed {
                background-color: #388E3C;
            }
            
            QPushButton:disabled {
                background-color: #BDBDBD;
                color: #757575;
            }
            
            QLineEdit, QSpinBox, QComboBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                padding: 8px;
                color: #212121;
            }
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 2px solid #2E7D32;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #212121;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QCheckBox {
                color: #212121;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #BDBDBD;
                border-radius: 3px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #2E7D32;
                border-color: #2E7D32;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #BDBDBD;
                height: 8px;
                background: #E0E0E0;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #2E7D32;
                border: 1px solid #1B5E20;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #212121;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                color: #2E7D32;
                font-weight: bold;
            }
            
            QTabBar::tab:hover {
                background-color: #EEEEEE;
            }
        """
    
    def get_dark_theme(self):
        return """
            QMainWindow, QDialog, QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }
            
            QLabel {
                color: #E0E0E0;
            }
            
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #388E3C;
            }
            
            QPushButton:pressed {
                background-color: #1B5E20;
            }
            
            QPushButton:disabled {
                background-color: #424242;
                color: #757575;
            }
            
            QLineEdit, QSpinBox, QComboBox {
                background-color: #2C2C2C;
                border: 2px solid #424242;
                border-radius: 5px;
                padding: 8px;
                color: #E0E0E0;
            }
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 2px solid #2E7D32;
            }
            
            QComboBox::drop-down {
                border: none;
                background-color: #424242;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #E0E0E0;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2C2C2C;
                color: #E0E0E0;
                selection-background-color: #2E7D32;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #424242;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #E0E0E0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QCheckBox {
                color: #E0E0E0;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #616161;
                border-radius: 3px;
                background-color: #2C2C2C;
            }
            
            QCheckBox::indicator:checked {
                background-color: #2E7D32;
                border-color: #2E7D32;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #424242;
                height: 8px;
                background: #2C2C2C;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #2E7D32;
                border: 1px solid #1B5E20;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            QTabWidget::pane {
                border: 1px solid #424242;
                background-color: #2C2C2C;
            }
            
            QTabBar::tab {
                background-color: #2C2C2C;
                color: #E0E0E0;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: #1E1E1E;
                color: #2E7D32;
                font-weight: bold;
            }
            
            QTabBar::tab:hover {
                background-color: #424242;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #424242;
                border: none;
            }
            
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 7px;
                height: 7px;
            }
        """
    
    def get_palette_for_theme(self, theme_name):
        palette = QPalette()
        
        if theme_name == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.Base, QColor(44, 44, 44))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.Text, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.Button, QColor(44, 44, 44))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.Link, QColor(46, 125, 50))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(46, 125, 50))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Text, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Button, QColor(224, 224, 224))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Link, QColor(46, 125, 50))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(46, 125, 50))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        return palette
