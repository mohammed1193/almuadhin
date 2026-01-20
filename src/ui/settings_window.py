from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QWidget, QLineEdit,
                             QComboBox, QSpinBox, QCheckBox, QGroupBox,
                             QFileDialog, QSlider, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from utils.config import ConfigManager
from utils.location import LocationService
from utils.startup import StartupManager
from utils.saudi_cities import get_cities_list, get_city_info

class NumberControl(QWidget):
    """مكون Slider مخصص للتحكم بالأرقام"""
    valueChanged = pyqtSignal(int)
    
    def __init__(self, min_val=-30, max_val=30, initial_val=0):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = initial_val
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # عرض القيمة الحالية
        self.value_label = QLabel(f"{self.current_val} دقيقة")
        self.value_label.setFixedWidth(70)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.value_label.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(self.value_label)
        
        # الشريط المنزلق
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(initial_val)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #E0E0E0;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #45A049;
            }
        """)
        self.slider.valueChanged.connect(self.on_slider_change)
        layout.addWidget(self.slider)
    
    def on_slider_change(self, value):
        self.current_val = value
        self.value_label.setText(f"{value} دقيقة")
        self.valueChanged.emit(value)
    
    def value(self):
        return self.current_val
    
    def setValue(self, val):
        self.current_val = val
        self.slider.setValue(val)
        self.value_label.setText(f"{val} دقيقة")

class SettingsWindow(QDialog):
    settings_saved = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.location_service = LocationService()
        self.startup_manager = StartupManager()
        self.config = self.config_manager.load_config()
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        self.setWindowTitle("الإعدادات")
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        
        tabs.addTab(self.create_general_tab(), "عام")
        tabs.addTab(self.create_adhan_tab(), "الأذان")
        tabs.addTab(self.create_iqama_tab(), "الإقامة")
        tabs.addTab(self.create_times_tab(), "الأوقات")
        tabs.addTab(self.create_notifications_tab(), "الإشعارات")
        tabs.addTab(self.create_appearance_tab(), "المظهر")
        
        layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("حفظ")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        location_group = QGroupBox("الموقع")
        location_layout = QGridLayout()
        
        self.use_coords_check = QCheckBox("استخدام الإحداثيات الجغرافية (أكثر دقة)")
        self.use_coords_check.setFont(QFont("Tajawal", 11))
        from pathlib import Path
        assets_dir = Path(__file__).parent.parent.parent / "assets"
        checkmark_path = str(assets_dir / "checkmark.svg").replace("\\", "/")
        self.use_coords_check.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: #4CAF50;
                border: 2px solid #4CAF50;
                image: url({checkmark_path});
            }}
        """)
        self.use_coords_check.stateChanged.connect(self.toggle_location_mode)
        location_layout.addWidget(self.use_coords_check, 0, 0, 1, 2)
        
        location_layout.addWidget(QLabel("اختر مدينة سعودية:"), 1, 0)
        self.saudi_city_combo = QComboBox()
        self.saudi_city_combo.addItem("-- اختر مدينة --", None)
        for city in get_cities_list():
            self.saudi_city_combo.addItem(city, city)
        self.saudi_city_combo.currentIndexChanged.connect(self.on_saudi_city_selected)
        location_layout.addWidget(self.saudi_city_combo, 1, 1)
        
        location_layout.addWidget(QLabel("أو أدخل مدينة أخرى:"), 2, 0)
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("اسم المدينة")
        location_layout.addWidget(self.city_input, 2, 1)
        
        location_layout.addWidget(QLabel("الدولة:"), 3, 0)
        self.country_input = QLineEdit()
        self.country_input.setText("Saudi Arabia")
        location_layout.addWidget(self.country_input, 3, 1)
        
        location_layout.addWidget(QLabel("خط العرض (Latitude):"), 4, 0)
        self.latitude_input = QLineEdit()
        self.latitude_input.setPlaceholderText("مثال: 24.7136")
        location_layout.addWidget(self.latitude_input, 4, 1)
        
        location_layout.addWidget(QLabel("خط الطول (Longitude):"), 5, 0)
        self.longitude_input = QLineEdit()
        self.longitude_input.setPlaceholderText("مثال: 46.6753")
        location_layout.addWidget(self.longitude_input, 5, 1)
        
        detect_btn = QPushButton("تحديد تلقائي (GPS)")
        detect_btn.clicked.connect(self.detect_precise_location)
        location_layout.addWidget(detect_btn, 6, 0, 1, 2)
        
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        calc_group = QGroupBox("طريقة الحساب")
        calc_layout = QVBoxLayout()
        
        self.method_combo = QComboBox()
        self.method_combo.addItem("جامعة أم القرى، مكة", 4)
        self.method_combo.addItem("الهيئة العامة المصرية للمساحة", 5)
        self.method_combo.addItem("رابطة العالم الإسلامي", 3)
        self.method_combo.addItem("الجمعية الإسلامية لأمريكا الشمالية", 2)
        calc_layout.addWidget(self.method_combo)
        
        calc_group.setLayout(calc_layout)
        layout.addWidget(calc_group)
        
        startup_group = QGroupBox("بدء التشغيل")
        startup_layout = QVBoxLayout()
        
        from pathlib import Path
        assets_dir = Path(__file__).parent.parent.parent / "assets"
        checkmark_path = str(assets_dir / "checkmark.svg").replace("\\", "/")
        checkbox_style = f"""
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: #4CAF50;
                border: 2px solid #4CAF50;
                image: url({checkmark_path});
            }}
        """
        
        self.startup_check = QCheckBox("تشغيل تلقائي عند بدء Windows")
        self.startup_check.setFont(QFont("Tajawal", 11))
        self.startup_check.setStyleSheet(checkbox_style)
        startup_layout.addWidget(self.startup_check)
        
        self.minimize_check = QCheckBox("تصغير إلى شريط المهام عند الإغلاق")
        self.minimize_check.setFont(QFont("Tajawal", 11))
        self.minimize_check.setStyleSheet(checkbox_style)
        startup_layout.addWidget(self.minimize_check)
        
        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)
        
        layout.addStretch()
        return widget
    
    def create_adhan_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        enable_group = QGroupBox("تفعيل الأذان")
        enable_layout = QVBoxLayout()
        
        self.adhan_checks = {}
        for prayer, arabic in [('Fajr', 'الفجر'), ('Dhuhr', 'الظهر'), 
                               ('Asr', 'العصر'), ('Maghrib', 'المغرب'), 
                               ('Isha', 'العشاء')]:
            check = QCheckBox(arabic)
            check.setFont(QFont("Tajawal", 11))
            
            # مسار ملف الأيقونة
            from pathlib import Path
            assets_dir = Path(__file__).parent.parent.parent / "assets"
            checkmark_path = str(assets_dir / "checkmark.svg").replace("\\", "/")
            
            check.setStyleSheet(f"""
                QCheckBox {{
                    spacing: 8px;
                }}
                QCheckBox::indicator {{
                    width: 22px;
                    height: 22px;
                    border: 2px solid #CCCCCC;
                    border-radius: 4px;
                    background: white;
                }}
                QCheckBox::indicator:checked {{
                    background: #4CAF50;
                    border: 2px solid #4CAF50;
                    image: url({checkmark_path});
                }}
            """)
            self.adhan_checks[prayer] = check
            enable_layout.addWidget(check)
        
        enable_group.setLayout(enable_layout)
        layout.addWidget(enable_group)
        
        sound_group = QGroupBox("الصوت")
        sound_layout = QVBoxLayout()
        
        sound_file_layout = QHBoxLayout()
        sound_file_layout.addWidget(QLabel("ملف الأذان:"))
        self.adhan_file_input = QLineEdit()
        sound_file_layout.addWidget(self.adhan_file_input)
        browse_btn = QPushButton("استعراض")
        browse_btn.clicked.connect(self.browse_adhan_file)
        sound_file_layout.addWidget(browse_btn)
        sound_layout.addLayout(sound_file_layout)
        
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("مستوى الصوت:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        volume_layout.addWidget(self.volume_slider)
        self.volume_label = QLabel("80%")
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_label.setText(f"{v}%"))
        volume_layout.addWidget(self.volume_label)
        sound_layout.addLayout(volume_layout)
        
        sound_group.setLayout(sound_layout)
        layout.addWidget(sound_group)
        
        layout.addStretch()
        return widget
    
    def create_iqama_tab(self):
        """إنشاء تبويب الإقامة المستقل"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        iqama_group = QGroupBox("الإقامة")
        iqama_layout = QVBoxLayout()
        iqama_layout.setSpacing(15)
        
        # تفعيل الإقامة
        from pathlib import Path
        assets_dir = Path(__file__).parent.parent.parent / "assets"
        checkmark_path = str(assets_dir / "checkmark.svg").replace("\\", "/")
        
        self.iqama_check = QCheckBox("تفعيل الإقامة")
        self.iqama_check.setFont(QFont("Tajawal", 12))
        self.iqama_check.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: #4CAF50;
                border: 2px solid #4CAF50;
                image: url({checkmark_path});
            }}
        """)
        iqama_layout.addWidget(self.iqama_check)
        
        # التأخير بالدقائق
        delay_layout = QHBoxLayout()
        delay_layout.setSpacing(10)
        
        delay_label = QLabel("التأخير (بالدقائق):")
        delay_label.setFont(QFont("Tajawal", 12))
        delay_layout.addWidget(delay_label)
        
        # Slider للتأخير
        self.iqama_delay_value = QLabel("15 دقيقة")
        self.iqama_delay_value.setFixedWidth(70)
        self.iqama_delay_value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.iqama_delay_value.setStyleSheet("font-size: 13px; color: #333;")
        delay_layout.addWidget(self.iqama_delay_value)
        
        self.iqama_delay_spin = QSlider(Qt.Orientation.Horizontal)
        self.iqama_delay_spin.setMinimum(1)
        self.iqama_delay_spin.setMaximum(60)
        self.iqama_delay_spin.setValue(15)
        self.iqama_delay_spin.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #E0E0E0;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #45A049;
            }
        """)
        self.iqama_delay_spin.valueChanged.connect(self.on_iqama_delay_change)
        delay_layout.addWidget(self.iqama_delay_spin)
        
        iqama_layout.addLayout(delay_layout)
        
        # ملف الإقامة
        iqama_file_layout = QHBoxLayout()
        iqama_file_layout.setSpacing(10)
        
        file_label = QLabel("ملف الإقامة:")
        file_label.setFont(QFont("Tajawal", 12))
        iqama_file_layout.addWidget(file_label)
        
        self.iqama_file_input = QLineEdit()
        self.iqama_file_input.setFont(QFont("Tajawal", 11))
        self.iqama_file_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 8px;
                background: white;
            }
        """)
        iqama_file_layout.addWidget(self.iqama_file_input)
        
        browse_iqama_btn = QPushButton("استعراض")
        browse_iqama_btn.setFont(QFont("Tajawal", 11))
        browse_iqama_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        browse_iqama_btn.clicked.connect(self.browse_iqama_file)
        iqama_file_layout.addWidget(browse_iqama_btn)
        
        iqama_layout.addLayout(iqama_file_layout)
        
        iqama_group.setLayout(iqama_layout)
        layout.addWidget(iqama_group)
        
        layout.addStretch()
        return widget
    
    def on_iqama_delay_change(self, value):
        """تحديث عرض قيمة تأخير الإقامة"""
        self.iqama_delay_value.setText(f"{value} دقيقة")
    
    def create_times_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        offset_group = QGroupBox("تعديل الأوقات (بالدقائق)")
        offset_layout = QGridLayout()
        offset_layout.setHorizontalSpacing(20)
        offset_layout.setVerticalSpacing(10)
        
        self.offset_spins = {}
        prayers = [('Fajr', 'الفجر'), ('Dhuhr', 'الظهر'), 
                   ('Asr', 'العصر'), ('Maghrib', 'المغرب'), 
                   ('Isha', 'العشاء')]
        
        for i, (prayer, arabic) in enumerate(prayers):
            label = QLabel(arabic + ":")
            label.setFont(QFont("Tajawal", 13))
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            offset_layout.addWidget(label, i, 1)
            
            control = NumberControl(min_val=-30, max_val=30, initial_val=0)
            self.offset_spins[prayer] = control
            offset_layout.addWidget(control, i, 0)
        
        offset_group.setLayout(offset_layout)
        layout.addWidget(offset_group)
        
        info_label = QLabel("ملاحظة: القيم الموجبة تؤخر الوقت، والسالبة تقدمه")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        return widget
    
    def create_notifications_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        notif_group = QGroupBox("الإشعارات")
        notif_layout = QVBoxLayout()
        notif_layout.setSpacing(15)
        
        # تفعيل الإشعارات
        from pathlib import Path
        assets_dir = Path(__file__).parent.parent.parent / "assets"
        checkmark_path = str(assets_dir / "checkmark.svg").replace("\\", "/")
        
        self.notif_check = QCheckBox("تفعيل الإشعارات")
        self.notif_check.setFont(QFont("Tajawal", 12))
        self.notif_check.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: #4CAF50;
                border: 2px solid #4CAF50;
                image: url({checkmark_path});
            }}
        """)
        notif_layout.addWidget(self.notif_check)
        
        # التنبيه قبل الصلاة
        before_layout = QHBoxLayout()
        before_layout.setSpacing(10)
        
        label = QLabel("التنبيه قبل الصلاة بـ:")
        label.setFont(QFont("Tajawal", 12))
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        before_layout.addWidget(label)
        
        # عرض القيمة
        self.notif_value_label = QLabel("10 دقيقة")
        self.notif_value_label.setFixedWidth(70)
        self.notif_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.notif_value_label.setStyleSheet("font-size: 13px; color: #333;")
        before_layout.addWidget(self.notif_value_label)
        
        # الشريط المنزلق
        self.notif_before_spin = QSlider(Qt.Orientation.Horizontal)
        self.notif_before_spin.setMinimum(1)
        self.notif_before_spin.setMaximum(60)
        self.notif_before_spin.setValue(10)
        self.notif_before_spin.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #E0E0E0;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #45A049;
            }
        """)
        self.notif_before_spin.valueChanged.connect(self.on_notif_slider_change)
        before_layout.addWidget(self.notif_before_spin)
        
        notif_layout.addLayout(before_layout)
        
        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)
        
        layout.addStretch()
        return widget
    
    def on_notif_slider_change(self, value):
        """تحديث عرض قيمة الإشعارات"""
        self.notif_value_label.setText(f"{value} دقيقة")
    
    def create_developer_tab(self):
        """إنشاء تبويب عن المطور"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # عنوان
        title_label = QLabel("عن المطوّر")
        title_font = QFont("Tajawal", 22, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1976D2; padding: 15px;")
        layout.addWidget(title_label)
        
        # النص الكامل
        full_text = """هذا التطبيق من تطوير
يوسف بن محمد الدخيل العنزي

تم إنشاء هذا التطبيق بنية خالصة لوجه الله تعالى،
سائلين الله أن ينفع به المسلمين،
وأن يجعله صدقة جارية عن المطوّر ووالديه،
وكل من ساهم في تطويره أو نشره.

نسأل الله القبول والتوفيق،
وأن يكون هذا العمل في ميزان الحسنات."""
        
        dev_info = QLabel(full_text)
        dev_info_font = QFont("Tajawal", 13)
        dev_info.setFont(dev_info_font)
        dev_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_info.setWordWrap(True)
        dev_info.setStyleSheet("""
            color: #333; 
            padding: 20px;
            line-height: 1.8;
            background: #F9F9F9;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
        """)
        layout.addWidget(dev_info)
        
        layout.addStretch()
        return widget
    
    def create_appearance_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        theme_group = QGroupBox("المظهر")
        theme_layout = QVBoxLayout()
        
        theme_layout.addWidget(QLabel("الثيم:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("فاتح", "light")
        self.theme_combo.addItem("داكن", "dark")
        theme_layout.addWidget(self.theme_combo)
        
        theme_layout.addWidget(QLabel("اللغة:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("العربية", "ar")
        self.lang_combo.addItem("English", "en")
        theme_layout.addWidget(self.lang_combo)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        layout.addStretch()
        return widget
    
    def load_settings(self):
        self.city_input.setText(self.config['location']['city'])
        self.country_input.setText(self.config['location']['country'])
        
        use_coords = self.config['location'].get('use_coordinates', False)
        self.use_coords_check.setChecked(use_coords)
        
        if self.config['location'].get('latitude'):
            self.latitude_input.setText(str(self.config['location']['latitude']))
        if self.config['location'].get('longitude'):
            self.longitude_input.setText(str(self.config['location']['longitude']))
        
        self.toggle_location_mode()
        
        method = self.config['calculation_method']
        index = self.method_combo.findData(method)
        if index >= 0:
            self.method_combo.setCurrentIndex(index)
        
        for prayer, check in self.adhan_checks.items():
            check.setChecked(self.config['adhan']['enabled'].get(prayer, True))
        
        self.adhan_file_input.setText(self.config['adhan']['sound_file'])
        self.volume_slider.setValue(self.config['adhan']['volume'])
        
        self.iqama_check.setChecked(self.config['iqama']['enabled'])
        self.iqama_delay_spin.setValue(self.config['iqama']['delay_minutes'])
        self.iqama_file_input.setText(self.config['iqama'].get('sound_file', 'default_iqama.mp3'))
        
        for prayer, spin in self.offset_spins.items():
            spin.setValue(self.config['offsets'].get(prayer, 0))
        
        self.notif_check.setChecked(self.config['notifications']['enabled'])
        self.notif_before_spin.setValue(self.config['notifications']['before_minutes'])
        
        theme = self.config['appearance']['theme']
        theme_index = self.theme_combo.findData(theme)
        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(theme_index)
        
        lang = self.config['appearance']['language']
        lang_index = self.lang_combo.findData(lang)
        if lang_index >= 0:
            self.lang_combo.setCurrentIndex(lang_index)
        
        startup_enabled = self.startup_manager.is_enabled()
        self.startup_check.setChecked(startup_enabled)
        self.minimize_check.setChecked(self.config['startup']['minimize_to_tray'])
    
    def save_settings(self):
        self.config['location']['city'] = self.city_input.text()
        self.config['location']['country'] = self.country_input.text()
        self.config['location']['use_coordinates'] = self.use_coords_check.isChecked()
        
        if self.latitude_input.text() and self.longitude_input.text():
            try:
                lat = float(self.latitude_input.text())
                lng = float(self.longitude_input.text())
                if self.location_service.validate_coordinates(lat, lng):
                    self.config['location']['latitude'] = lat
                    self.config['location']['longitude'] = lng
                    self.config['location']['method'] = 'coordinates'
                else:
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "خطأ", "الإحداثيات غير صحيحة!\nخط العرض: -90 إلى 90\nخط الطول: -180 إلى 180")
                    return
            except ValueError:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "خطأ", "الرجاء إدخال أرقام صحيحة للإحداثيات!")
                return
        else:
            self.config['location']['latitude'] = None
            self.config['location']['longitude'] = None
            self.config['location']['method'] = 'city'
        
        self.config['calculation_method'] = self.method_combo.currentData()
        
        for prayer, check in self.adhan_checks.items():
            self.config['adhan']['enabled'][prayer] = check.isChecked()
        
        self.config['adhan']['sound_file'] = self.adhan_file_input.text()
        self.config['adhan']['volume'] = self.volume_slider.value()
        
        self.config['iqama']['enabled'] = self.iqama_check.isChecked()
        self.config['iqama']['delay_minutes'] = self.iqama_delay_spin.value()
        self.config['iqama']['sound_file'] = self.iqama_file_input.text()
        
        for prayer, spin in self.offset_spins.items():
            self.config['offsets'][prayer] = spin.value()
        
        self.config['notifications']['enabled'] = self.notif_check.isChecked()
        self.config['notifications']['before_minutes'] = self.notif_before_spin.value()
        
        self.config['appearance']['theme'] = self.theme_combo.currentData()
        self.config['appearance']['language'] = self.lang_combo.currentData()
        
        startup_enabled = self.startup_check.isChecked()
        if startup_enabled:
            self.startup_manager.enable()
        else:
            self.startup_manager.disable()
        
        self.config['startup']['run_on_startup'] = startup_enabled
        self.config['startup']['minimize_to_tray'] = self.minimize_check.isChecked()
        
        if self.config_manager.save_config(self.config):
            self.settings_saved.emit()
            self.accept()
    
    def detect_location(self):
        location = self.location_service.get_current_location()
        if location:
            self.city_input.setText(location['city'])
            self.country_input.setText(location['country'])
            if location.get('latitude') and location.get('longitude'):
                self.latitude_input.setText(str(location['latitude']))
                self.longitude_input.setText(str(location['longitude']))
    
    def detect_precise_location(self):
        from PyQt6.QtWidgets import QMessageBox
        location = self.location_service.get_precise_location()
        if location:
            if location.get('city'):
                self.city_input.setText(location['city'])
            if location.get('country'):
                self.country_input.setText(location['country'])
            if location.get('latitude') and location.get('longitude'):
                self.latitude_input.setText(str(location['latitude']))
                self.longitude_input.setText(str(location['longitude']))
                self.use_coords_check.setChecked(True)
                QMessageBox.information(self, "نجح", f"تم تحديد الموقع بدقة!\n{location['city']}, {location['country']}\nالإحداثيات: {location['latitude']:.4f}, {location['longitude']:.4f}")
        else:
            QMessageBox.warning(self, "تنبيه", "لم نتمكن من تحديد موقعك الدقيق.\nتم استخدام تحديد الموقع من IP بدلاً من ذلك.")
    
    def on_saudi_city_selected(self, index):
        city_name = self.saudi_city_combo.currentData()
        if city_name:
            city_info = get_city_info(city_name)
            if city_info:
                self.city_input.setText(city_info['name_en'])
                self.country_input.setText("Saudi Arabia")
                self.latitude_input.setText(str(city_info['latitude']))
                self.longitude_input.setText(str(city_info['longitude']))
                self.use_coords_check.setChecked(True)
    
    def toggle_location_mode(self):
        use_coords = self.use_coords_check.isChecked()
        
        self.latitude_input.setEnabled(use_coords)
        self.longitude_input.setEnabled(use_coords)
        
        if use_coords:
            self.saudi_city_combo.setEnabled(True)
            self.city_input.setEnabled(False)
            self.country_input.setEnabled(False)
        else:
            self.saudi_city_combo.setEnabled(True)
            self.city_input.setEnabled(True)
            self.country_input.setEnabled(True)
    
    def browse_adhan_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر ملف الأذان",
            "",
            "Audio Files (*.mp3 *.wav)"
        )
        if file_path:
            self.adhan_file_input.setText(file_path)
    
    def browse_iqama_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر ملف الإقامة",
            "",
            "Audio Files (*.mp3 *.wav)"
        )
        if file_path:
            self.iqama_file_input.setText(file_path)
