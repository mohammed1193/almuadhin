import winreg
import sys
import os

class StartupManager:
    def __init__(self, app_name="المؤذن"):
        self.app_name = app_name
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    def is_enabled(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            print(f"Error checking startup status: {e}")
            return False
    
    def enable(self):
        try:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
            else:
                python_exe = sys.executable
                script_path = os.path.abspath(sys.argv[0])
                exe_path = f'"{python_exe}" "{script_path}"'
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error enabling startup: {e}")
            return False
    
    def disable(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_WRITE
            )
            try:
                winreg.DeleteValue(key, self.app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return True
        except Exception as e:
            print(f"Error disabling startup: {e}")
            return False
