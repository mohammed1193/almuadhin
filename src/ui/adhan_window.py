from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QWidget, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor

class AdhanWindow(QDialog):
    def __init__(self, prayer_name, prayer_time, audio_player, parent=None):
        super().__init__(parent)
        self.prayer_name = prayer_name
        self.prayer_time = prayer_time
        self.audio_player = audio_player
        
        self.init_ui()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint
        )
    
    def init_ui(self):
        self.setWindowTitle("الأذان")
        self.setFixedSize(650, 550)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container with gradient background
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0D47A1, stop:0.5 #1976D2, stop:1 #42A5F5);
                border-radius: 20px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(25)
        container_layout.setContentsMargins(50, 50, 50, 50)
        
        # Mosque icon/emoji
        icon_label = QLabel("🕌")
        icon_font = QFont("Arial", 72)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(icon_label)
        
        # Title with animation
        title_label = QLabel("حان وقت الصلاة")
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            color: white;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        """)
        container_layout.addWidget(title_label)
        self.title_label = title_label
        
        # Prayer name card
        prayer_card = QFrame()
        prayer_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        prayer_card_layout = QVBoxLayout(prayer_card)
        prayer_card_layout.setSpacing(10)
        
        prayer_label = QLabel(self.prayer_name)
        prayer_font = QFont("Arial", 56, QFont.Weight.Bold)
        prayer_label.setFont(prayer_font)
        prayer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prayer_label.setStyleSheet("color: #1976D2; padding: 15px;")
        prayer_card_layout.addWidget(prayer_label)
        self.prayer_label = prayer_label
        
        time_label = QLabel(self.prayer_time)
        time_font = QFont("Arial", 36, QFont.Weight.Bold)
        time_label.setFont(time_font)
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("color: #666; padding: 10px;")
        prayer_card_layout.addWidget(time_label)
        
        # Add shadow to prayer card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        prayer_card.setGraphicsEffect(shadow)
        
        container_layout.addWidget(prayer_card)
        container_layout.addStretch()
        
        # Modern buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        stop_btn = self.create_modern_button("⏸️ إيقاف الأذان", "#F44336")
        stop_btn.clicked.connect(self.stop_adhan)
        button_layout.addWidget(stop_btn)
        
        close_btn = self.create_modern_button("✖️ إغلاق", "#FF9800")
        close_btn.clicked.connect(self.close_window)
        button_layout.addWidget(close_btn)
        
        container_layout.addLayout(button_layout)
        
        main_layout.addWidget(container)
        
        # Add shadow to main window
        window_shadow = QGraphicsDropShadowEffect()
        window_shadow.setBlurRadius(40)
        window_shadow.setXOffset(0)
        window_shadow.setYOffset(10)
        window_shadow.setColor(QColor(0, 0, 0, 100))
        container.setGraphicsEffect(window_shadow)
        
        # Start animations
        self.start_animations()
        
        # Auto-close timer
        self.auto_close_timer = QTimer()
        self.auto_close_timer.timeout.connect(self.check_audio_finished)
        self.auto_close_timer.start(1000)
    
    def create_modern_button(self, text, color):
        """إنشاء زر عصري"""
        btn = QPushButton(text)
        btn.setMinimumHeight(55)
        btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 25px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.3)};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 50))
        btn.setGraphicsEffect(shadow)
        
        return btn
    
    def darken_color(self, hex_color, factor=0.2):
        """تغميق اللون"""
        color = QColor(hex_color)
        h, s, v, a = color.getHsv()
        v = int(v * (1 - factor))
        color.setHsv(h, s, v, a)
        return color.name()
    
    def start_animations(self):
        """بدء الرسوم المتحركة"""
        # Pulse animation for prayer label
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse_effect)
        self.pulse_timer.start(1000)
        self.pulse_state = 0
    
    def pulse_effect(self):
        """تأثير النبض"""
        if self.pulse_state == 0:
            self.prayer_label.setStyleSheet("color: #1976D2; padding: 15px; font-size: 56pt;")
            self.pulse_state = 1
        else:
            self.prayer_label.setStyleSheet("color: #2196F3; padding: 15px; font-size: 54pt;")
            self.pulse_state = 0
    
    def stop_adhan(self):
        if self.audio_player:
            self.audio_player.stop()
        self.close_window()
    
    def close_window(self):
        self.auto_close_timer.stop()
        self.accept()
    
    def check_audio_finished(self):
        if self.audio_player and not self.audio_player.is_busy():
            QTimer.singleShot(2000, self.close_window)
    
    def showEvent(self, event):
        super().showEvent(event)
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
