import sys
import ctypes
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QSharedMemory
from PyQt6.QtGui import QIcon

# إضافة مسار src إلى PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("المؤذن")
    app.setOrganizationName("محمد الدخيل")
    app.setApplicationDisplayName("المؤذن")
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # منع تشغيل نسختين من التطبيق
    shared_memory = QSharedMemory("AlmuadhinAppSingleInstance")
    if not shared_memory.create(1):
        # التطبيق يعمل بالفعل
        QMessageBox.warning(
            None,
            "تنبيه",
            "التطبيق يعمل بالفعل!\nلا يمكن تشغيل أكثر من نسخة واحدة في نفس الوقت.",
            QMessageBox.StandardButton.Ok
        )
        sys.exit(0)
    
    app.shared_memory = shared_memory  # حفظ المرجع لمنع حذفه
    
    # تعيين اسم التطبيق في Windows taskbar
    if sys.platform == 'win32':
        myappid = 'المؤذن'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # تعيين أيقونة التطبيق
    icon_path = Path(__file__).parent.parent / "resources" / "icons" / "app_icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
