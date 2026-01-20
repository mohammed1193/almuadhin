from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QGridLayout, QFrame, QGraphicsDropShadowEffect,
                             QStackedWidget, QTabWidget, QLineEdit, QComboBox, QCheckBox, 
                             QGroupBox, QSpinBox, QSlider, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QIcon, QColor
from core.api_client import AlAdhanAPI
from core.prayer_times import PrayerTimesManager
from core.scheduler import PrayerScheduler
from core.audio_player import AudioPlayer
from core.notifier import NotificationManager
from utils.config import ConfigManager
from utils.theme_manager import ThemeManager
from ui.adhan_window import AdhanWindow
from ui.tray_icon import SystemTrayIcon
from ui.settings_window import SettingsWindow
from utils.location import LocationService
from utils.startup import StartupManager
from utils.saudi_cities import get_cities_list, get_city_info
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.api_client = AlAdhanAPI()
        self.prayer_manager = PrayerTimesManager()
        self.audio_player = AudioPlayer()
        self.theme_manager = ThemeManager()
        
        self.init_ui()
        self.apply_theme()
        self.setup_tray_icon()
        self.setup_notifications()
        self.setup_scheduler()
        
        self.load_prayer_times()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def init_ui(self):
        self.setWindowTitle("مواقيت الصلاة")
        self.setMinimumSize(600, 800)
        self.setMaximumSize(800, 950)
        
        # إزالة شريط العنوان الافتراضي
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # إنشاء layout رئيسي يحتوي على شريط العنوان المخصص
        main_container = QVBoxLayout(central_widget)
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setSpacing(0)
        
        # إنشاء شريط العنوان المخصص
        self.create_custom_title_bar(main_container)
        
        # إضافة StackedWidget إلى الـ container
        main_container.addWidget(self.stacked_widget)
    
    def create_custom_title_bar(self, parent_layout):
        """إنشاء شريط عنوان مخصص"""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #1976D2;
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 5, 0)
        title_layout.setSpacing(8)
        
        # أيقونة التطبيق
        from pathlib import Path
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "app_icon.ico"
        if icon_path.exists():
            icon_label = QLabel()
            icon_pixmap = QIcon(str(icon_path)).pixmap(24, 24)
            icon_label.setPixmap(icon_pixmap)
            title_layout.addWidget(icon_label)
        
        # نص العنوان
        title_label = QLabel("مواقيت الصلاة")
        title_label.setFont(QFont("Tajawal", 11, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # زر التصغير
        minimize_btn = QPushButton("━")
        minimize_btn.setFixedSize(40, 35)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid white;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_btn)
        
        # زر الإغلاق
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 35)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
                border: 1px solid #D32F2F;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        parent_layout.addWidget(title_bar)
        
        # حفظ مرجع لشريط العنوان لتمكين السحب
        self.title_bar = title_bar
        self.title_bar.mousePressEvent = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move
        
        # إنشاء StackedWidget للتبديل بين الصفحات
        self.stacked_widget = QStackedWidget()
        
        # إنشاء صفحة المواقيت الرئيسية
        main_page = QWidget()
        main_layout = QVBoxLayout(main_page)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(35, 35, 35, 35)
        
        # Header Card - بطاقة العنوان
        header_card = self.create_card()
        header_layout = QVBoxLayout(header_card)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(25, 25, 25, 25)
        
        title_label = QLabel("◉ المؤذن")
        title_font = QFont("Tajawal", 32, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1976D2; padding: 10px; letter-spacing: 2px;")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("مواقيت الصلاة")
        subtitle_font = QFont("Tajawal", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; padding-bottom: 5px;")
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_card)
        
        # Next Prayer Card - بطاقة الصلاة القادمة
        next_prayer_card = self.create_card(gradient=True)
        next_prayer_layout = QVBoxLayout(next_prayer_card)
        next_prayer_layout.setSpacing(15)
        next_prayer_layout.setContentsMargins(30, 30, 30, 30)
        
        self.next_prayer_label = QLabel("الصلاة القادمة: جاري التحميل...")
        next_prayer_font = QFont("Tajawal", 18, QFont.Weight.Bold)
        self.next_prayer_label.setFont(next_prayer_font)
        self.next_prayer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.next_prayer_label.setStyleSheet("color: white; padding: 5px;")
        next_prayer_layout.addWidget(self.next_prayer_label)
        
        self.countdown_label = QLabel("00:00:00")
        countdown_font = QFont("Tajawal", 32, QFont.Weight.Bold)
        self.countdown_label.setFont(countdown_font)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("color: white; padding: 8px; letter-spacing: 0px;")
        next_prayer_layout.addWidget(self.countdown_label)
        
        main_layout.addWidget(next_prayer_card)
        
        # Prayer Times - مواقيت الصلاة بدون بطاقة
        prayers_title = QLabel("مواقيت اليوم")
        prayers_title_font = QFont("Tajawal", 14, QFont.Weight.Bold)
        prayers_title.setFont(prayers_title_font)
        prayers_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prayers_title.setStyleSheet("color: #333; padding: 8px;")
        main_layout.addWidget(prayers_title)
        
        prayers_grid = QGridLayout()
        prayers_grid.setSpacing(10)
        prayers_grid.setContentsMargins(40, 5, 40, 5)
        prayers_grid.setVerticalSpacing(12)
        prayers_grid.setHorizontalSpacing(20)
        prayers_grid.setColumnStretch(0, 1)
        prayers_grid.setColumnStretch(1, 1)
        
        self.prayer_labels = {}
        prayers = [
            ('الفجر', 'Fajr'),
            ('الظهر', 'Dhuhr'),
            ('العصر', 'Asr'),
            ('المغرب', 'Maghrib'),
            ('العشاء', 'Isha')
        ]
        
        for i, (arabic_name, english_name) in enumerate(prayers):
            # Prayer name label
            name_label = QLabel(arabic_name)
            name_font = QFont("Tajawal", 14, QFont.Weight.Bold)
            name_label.setFont(name_font)
            name_label.setStyleSheet("color: #333;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            prayers_grid.addWidget(name_label, i, 0)
            
            # Prayer time label
            time_label = QLabel("--:--")
            time_font = QFont("Tajawal", 14, QFont.Weight.Bold)
            time_label.setFont(time_font)
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            time_label.setStyleSheet("color: #1976D2 !important;")
            prayers_grid.addWidget(time_label, i, 1)
            
            self.prayer_labels[english_name] = time_label
        
        main_layout.addLayout(prayers_grid)
        
        # Action Buttons - أزرار الإجراءات
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        refresh_btn = self.create_modern_button("⟳  تحديث", "#2196F3")
        refresh_btn.clicked.connect(self.load_prayer_times)
        button_layout.addWidget(refresh_btn)
        
        settings_btn = self.create_modern_button("⚙  الإعدادات", "#2196F3")
        settings_btn.clicked.connect(self.open_settings)
        button_layout.addWidget(settings_btn)
        
        test_adhan_btn = self.create_modern_button("▶  تجربة الأذان", "#2196F3")
        test_adhan_btn.clicked.connect(self.test_adhan)
        button_layout.addWidget(test_adhan_btn)
        
        main_layout.addLayout(button_layout)
        
        # إضافة الصفحة الرئيسية إلى StackedWidget
        self.stacked_widget.addWidget(main_page)
        
        # إنشاء صفحة الإعدادات
        self.create_settings_page()
        
    
    def create_card(self, gradient=False):
        """إنشاء بطاقة عصرية مع ظل"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        
        if gradient:
            card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1976D2, stop:1 #2196F3);
                    border-radius: 15px;
                    border: none;
                }
            """)
        else:
            card.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 15px;
                    border: 1px solid #E0E0E0;
                }
            """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)
        
        return card
    
    
    def create_modern_button(self, text, color):
        """إنشاء زر عصري مع تأثيرات"""
        btn = QPushButton(text)
        btn.setMinimumHeight(45)
        btn.setFont(QFont("Tajawal", 13, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.3)};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 40))
        btn.setGraphicsEffect(shadow)
        
        return btn
    
    def darken_color(self, hex_color, factor=0.2):
        """تغميق اللون للتأثيرات"""
        color = QColor(hex_color)
        h, s, v, a = color.getHsv()
        v = int(v * (1 - factor))
        color.setHsv(h, s, v, a)
        return color.name()
    
    def load_prayer_times(self):
        config = self.config_manager.load_config()
        
        use_coords = config['location'].get('use_coordinates', False)
        latitude = config['location'].get('latitude')
        longitude = config['location'].get('longitude')
        
        timings = None
        
        print(f"Loading prayer times... use_coords={use_coords}, lat={latitude}, lon={longitude}")
        
        if use_coords and latitude and longitude:
            print(f"Fetching by coordinates: {latitude}, {longitude}")
            timings = self.api_client.get_timings_by_coordinates(
                latitude, 
                longitude,
                config.get('calculation_method', 4)
            )
        
        if not timings:
            city = config['location']['city']
            country = config['location']['country']
            print(f"Fetching by city: {city}, {country}")
            timings = self.api_client.get_timings_by_city(
                city, 
                country,
                config.get('calculation_method', 4)
            )
        
        if timings:
            print(f"Timings received: {timings}")
            self.prayer_manager.set_timings(timings)
            
            for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
                offset = config['offsets'].get(prayer, 0)
                self.prayer_manager.apply_offset(prayer, offset)
            
            self.update_prayer_display()
            print("Prayer times updated successfully")
        else:
            print("ERROR: Failed to fetch prayer times!")
            # عرض رسالة خطأ للمستخدم
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "خطأ",
                "فشل تحميل مواقيت الصلاة.\nتأكد من الاتصال بالإنترنت والإعدادات."
            )
    
    def update_prayer_display(self):
        all_timings = self.prayer_manager.get_all_timings()
        
        print(f"Updating display with timings: {all_timings}")
        print(f"Available prayer labels: {list(self.prayer_labels.keys())}")
        
        for prayer, time_str in all_timings.items():
            if prayer in self.prayer_labels and time_str:
                print(f"Setting {prayer} to {time_str}")
                label = self.prayer_labels[prayer]
                label.setText(time_str)
                label.setVisible(True)
                label.update()
                label.repaint()
            else:
                print(f"Skipping {prayer}: in_labels={prayer in self.prayer_labels}, has_time={bool(time_str)}")
    
    def update_time(self):
        next_prayer, next_time = self.prayer_manager.get_next_prayer()
        
        if next_time:
            arabic_name = PrayerTimesManager.PRAYER_NAMES.get(next_prayer, next_prayer)
            self.next_prayer_label.setText(f"الصلاة القادمة: {arabic_name}")
            
            hours, minutes, seconds = self.prayer_manager.get_time_remaining(next_time)
            self.countdown_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def setup_tray_icon(self):
        icon = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        self.tray_icon = SystemTrayIcon(icon, self)
        
        self.tray_icon.show_window_signal.connect(self.show)
        self.tray_icon.hide_window_signal.connect(self.hide)
        self.tray_icon.quit_signal.connect(self.quit_application)
        
        self.tray_icon.show()
    
    def setup_notifications(self):
        self.notifier = NotificationManager(self.tray_icon)
    
    def setup_scheduler(self):
        self.scheduler = PrayerScheduler(self.prayer_manager, self.config_manager)
        
        self.scheduler.prayer_time_reached.connect(self.on_prayer_time)
        self.scheduler.iqama_time_reached.connect(self.on_iqama_time)
        self.scheduler.notification_time.connect(self.on_notification_time)
    
    def on_prayer_time(self, prayer, arabic_name):
        config = self.config_manager.load_config()
        
        self.notifier.show_adhan_notification(arabic_name)
        
        sound_file = config['adhan'].get('sound_file', 'default_adhan.mp3')
        resources_path = Path(__file__).parent.parent.parent / "resources" / "sounds"
        sound_path = resources_path / sound_file
        
        if not sound_path.exists():
            sound_path = resources_path / "default_adhan.mp3"
        
        if sound_path.exists():
            volume = config['adhan'].get('volume', 80)
            self.audio_player.play(str(sound_path), volume)
        
        prayer_time = self.prayer_manager.get_prayer_time(prayer)
        adhan_window = AdhanWindow(arabic_name, prayer_time, self.audio_player, self)
        adhan_window.exec()
    
    def on_iqama_time(self, prayer):
        config = self.config_manager.load_config()
        arabic_name = self.prayer_manager.PRAYER_NAMES.get(prayer, prayer)
        
        self.notifier.show_iqama_notification(arabic_name)
        
        sound_file = config['iqama'].get('sound_file', 'default_iqama.mp3')
        resources_path = Path(__file__).parent.parent.parent / "resources" / "sounds"
        sound_path = resources_path / sound_file
        
        if sound_path.exists():
            self.audio_player.play(str(sound_path))
    
    def on_notification_time(self, prayer, minutes):
        arabic_name = self.prayer_manager.PRAYER_NAMES.get(prayer, prayer)
        self.notifier.show_prayer_notification(arabic_name, minutes)
    
    def test_adhan(self):
        self.on_prayer_time('Fajr', 'الفجر')
    
    def test_iqama(self):
        self.on_iqama_time('Fajr')
    
    def create_settings_page(self):
        """إنشاء صفحة الإعدادات داخل النافذة"""
        self.location_service = LocationService()
        self.startup_manager = StartupManager()
        
        settings_page = QWidget()
        settings_layout = QVBoxLayout(settings_page)
        settings_layout.setSpacing(15)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        
        # عنوان صفحة الإعدادات
        title_label = QLabel("⚙ الإعدادات")
        title_font = QFont("Tajawal", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1976D2; padding: 10px;")
        settings_layout.addWidget(title_label)
        
        # إنشاء التبويبات
        tabs = QTabWidget()
        tabs.setFont(QFont("Tajawal", 11))
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab {
                background: #F5F5F5;
                color: #333;
                padding: 8px 15px;
                margin-right: 4px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 11px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #1976D2;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #E8E8E8;
            }
        """)
        
        # إضافة التبويبات من SettingsWindow
        settings_window = SettingsWindow(self)
        tabs.addTab(settings_window.create_general_tab(), "عام")
        tabs.addTab(settings_window.create_adhan_tab(), "الأذان")
        tabs.addTab(settings_window.create_iqama_tab(), "الإقامة")
        tabs.addTab(settings_window.create_times_tab(), "الأوقات")
        tabs.addTab(settings_window.create_notifications_tab(), "الإشعارات")
        tabs.addTab(settings_window.create_developer_tab(), "عن المطور")
        
        # حفظ مرجع لـ settings_window
        self.embedded_settings = settings_window
        
        settings_layout.addWidget(tabs)
        
        # أزرار الحفظ والرجوع
        button_layout = QHBoxLayout()
        
        save_btn = self.create_modern_button("✓ حفظ", "#4CAF50")
        save_btn.clicked.connect(self.save_embedded_settings)
        button_layout.addWidget(save_btn)
        
        back_btn = self.create_modern_button("← رجوع", "#607D8B")
        back_btn.clicked.connect(self.show_main_page)
        button_layout.addWidget(back_btn)
        
        settings_layout.addLayout(button_layout)
        
        self.stacked_widget.addWidget(settings_page)
    
    def save_embedded_settings(self):
        """حفظ الإعدادات من الصفحة المدمجة"""
        self.embedded_settings.save_settings()
        self.on_settings_saved()
        self.show_main_page()
    
    def open_settings(self):
        """عرض صفحة الإعدادات"""
        self.stacked_widget.setCurrentIndex(1)
    
    def show_main_page(self):
        """العودة إلى الصفحة الرئيسية"""
        self.stacked_widget.setCurrentIndex(0)
    
    def apply_theme(self):
        config = self.config_manager.load_config()
        theme = config['appearance'].get('theme', 'light')
        stylesheet = self.theme_manager.apply_theme(theme)
        self.setStyleSheet(stylesheet)
    
    def on_settings_saved(self):
        self.load_prayer_times()
        self.apply_theme()
        self.notifier.show_success("تم حفظ الإعدادات بنجاح")
    
    def closeEvent(self, event):
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtGui import QFont
        
        reply = QMessageBox()
        reply.setWindowTitle("إغلاق التطبيق")
        reply.setText("هل تريد إغلاق التطبيق؟")
        reply.setInformativeText("اختر أحد الخيارات التالية:")
        reply.setIcon(QMessageBox.Icon.Question)
        
        # تطبيق خط تجوال وتنسيق عربي
        font = QFont("Tajawal", 11)
        reply.setFont(font)
        
        # تطبيق stylesheet متناسق مع التطبيق
        reply.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #333;
                font-family: 'Tajawal';
                font-size: 12pt;
            }
            QPushButton {
                font-family: 'Tajawal';
                font-size: 11pt;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
                min-width: 100px;
            }
            QPushButton[text="تصغير للخلفية"] {
                background-color: #2196F3;
                color: white;
            }
            QPushButton[text="تصغير للخلفية"]:hover {
                background-color: #1976D2;
            }
            QPushButton[text="إغلاق نهائي"] {
                background-color: #F44336;
                color: white;
            }
            QPushButton[text="إغلاق نهائي"]:hover {
                background-color: #D32F2F;
            }
            QPushButton[text="إلغاء"] {
                background-color: #9E9E9E;
                color: white;
            }
            QPushButton[text="إلغاء"]:hover {
                background-color: #757575;
            }
        """)
        
        # إضافة الأزرار المخصصة
        minimize_btn = reply.addButton("تصغير للخلفية", QMessageBox.ButtonRole.AcceptRole)
        close_btn = reply.addButton("إغلاق نهائي", QMessageBox.ButtonRole.DestructiveRole)
        cancel_btn = reply.addButton("إلغاء", QMessageBox.ButtonRole.RejectRole)
        
        reply.setDefaultButton(minimize_btn)
        reply.exec()
        
        if reply.clickedButton() == minimize_btn:
            # تصغير للخلفية
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "المؤذن",
                "التطبيق يعمل في الخلفية",
                QSystemTrayIcon.MessageIcon.NoIcon,
                2000
            )
        elif reply.clickedButton() == close_btn:
            # إغلاق نهائي
            event.accept()
            self.quit_application()
        else:
            # إلغاء
            event.ignore()
    
    def quit_application(self):
        self.audio_player.stop()
        self.tray_icon.hide()
        self.close()
        import sys
        sys.exit(0)
    
    def title_bar_mouse_press(self, event):
        """حفظ موضع الماوس عند الضغط على شريط العنوان"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def title_bar_mouse_move(self, event):
        """تحريك النافذة عند سحب شريط العنوان"""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
