# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
# from gui.realtime_widget import RealtimeWidget
# from gui.upload_widget import UploadWidget
# from gui.settings_widget import SettingsWidget
# from config.config_manager import ConfigManager
# from early_warning.warning_manager import WarningManager

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Violence & Weapon Detection System")
#         self.resize(900, 700)

#         # Muat konfigurasi
#         config = ConfigManager.load_config()

#         # Buat 1 instance WarningManager untuk semua tab
#         self.warning_manager = WarningManager(
#             model_path=config["model_path"],
#             telegram_token=config["telegram_token"],
#             chat_id=config["chat_id"],
#             conf_threshold=config["confidence_threshold"],
#             device=config["device"]
#         )

#         # Tab utama
#         tabs = QTabWidget()
#         tabs.addTab(RealtimeWidget(self.warning_manager), "Real-Time")
#         tabs.addTab(UploadWidget(self.warning_manager), "Upload File")
#         tabs.addTab(SettingsWidget(), "Settings")

#         layout = QVBoxLayout()
#         layout.addWidget(tabs)
#         self.setLayout(layout)

# from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
# from gui.realtime_widget import RealtimeWidget
# from gui.upload_widget import UploadWidget
# from gui.settings_widget import SettingsWidget
# from config.config_manager import ConfigManager
# from early_warning.warning_manager import WarningManager

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("🔍 Weapon & Violence Detection System")
#         self.resize(900, 650)

#         config = ConfigManager.load_config()
#         wm = WarningManager(
#             model_path=config["model_path"],
#             telegram_token=config["telegram_token"],
#             chat_id=config["chat_id"],
#             conf_threshold=config["confidence_threshold"],
#             device=config["device"]
#         )

#         tabs = QTabWidget()
#         tabs.addTab(RealtimeWidget(wm), "Real‑Time")
#         tabs.addTab(UploadWidget(wm), "Upload File")
#         tabs.addTab(SettingsWidget(), "Settings")

#         layout = QVBoxLayout()
#         layout.addWidget(tabs)
#         self.setLayout(layout)


# File: gui/main_window. py
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from gui.realtime_widget import RealtimeWidget
from gui.upload_widget import UploadWidget
from gui.settings_widget import SettingsWidget
from config.config_manager import ConfigManager
from early_warning. warning_manager import WarningManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Weapon & Violence Detection System")
        self.resize(900, 650)

        config = ConfigManager.load_config()
        self.warning_manager = WarningManager(  # ✅ Simpan sebagai self.warning_manager
            model_path=config["model_path"],
            telegram_token=config["telegram_token"],
            chat_id=config["chat_id"],
            conf_threshold=config["confidence_threshold"],
            device=config["device"]
        )

        tabs = QTabWidget()
        tabs.addTab(RealtimeWidget(self.warning_manager), "Real‑Time")
        tabs.addTab(UploadWidget(self.warning_manager), "Upload File")
        tabs.addTab(SettingsWidget(self.warning_manager), "Settings")  # ✅ Pass warning_manager

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)