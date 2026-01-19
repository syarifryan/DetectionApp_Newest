# from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox

# class SettingsWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.model_path_input = QLineEdit("model/fix-model/try-new 2/best.pt")
#         self.token_input = QLineEdit("8214376499:AAG7tJAD5A-Ur9jks0XgKajxMXOotVK3ZWE")
#         self.chat_id_input = QLineEdit("1635415181")
#         self.camera_index_input = QLineEdit("0")
#         self.threshold_input = QLineEdit("0.5")

#         save_btn = QPushButton("Save Settings")
#         save_btn.clicked.connect(self.save_settings)

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("Model Path:"))
#         layout.addWidget(self.model_path_input)
#         layout.addWidget(QLabel("Telegram Bot Token:"))
#         layout.addWidget(self.token_input)
#         layout.addWidget(QLabel("Telegram Chat ID:"))
#         layout.addWidget(self.chat_id_input)
#         layout.addWidget(QLabel("Camera Index:"))
#         layout.addWidget(self.camera_index_input)
#         layout.addWidget(QLabel("Confidence Threshold (0-1):"))
#         layout.addWidget(self.threshold_input)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#     def save_settings(self):
#         # Sementara: hanya tampilkan info
#         QMessageBox.information(self, "Saved", "Settings saved successfully!")
#         # Untuk implementasi lanjut: update konfigurasi global atau simpan ke file

# NEW
# # File: gui/settings_widget.py
# from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
# from config.config_manager import ConfigManager

# class SettingsWidget(QWidget):
#     def __init__(self, warning_manager=None):
#         super().__init__()
#         self.warning_manager = warning_manager
#         self.init_ui()
#         self.load_current_settings()

#     def init_ui(self):
#         self.model_path_input = QLineEdit()
#         self.token_input = QLineEdit()
#         self.chat_id_input = QLineEdit()
#         self.camera_index_input = QLineEdit()
#         self.threshold_input = QLineEdit()

#         save_btn = QPushButton("Save Settings")
#         save_btn.clicked. connect(self.save_settings)

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("Model Path:"))
#         layout.addWidget(self.model_path_input)
#         layout.addWidget(QLabel("Telegram Bot Token:"))
#         layout.addWidget(self.token_input)
#         layout.addWidget(QLabel("Telegram Chat ID:"))
#         layout.addWidget(self.chat_id_input)
#         layout.addWidget(QLabel("Camera Index:"))
#         layout.addWidget(self.camera_index_input)
#         layout.addWidget(QLabel("Confidence Threshold (0-1):"))
#         layout.addWidget(self.threshold_input)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#     def load_current_settings(self):
#         """Muat settings dari config. json saat tab dibuka"""
#         try:
#             config = ConfigManager.load_config()
#             self.model_path_input.setText(config.get("model_path", ""))
#             self.token_input.setText(config.get("telegram_token", ""))
#             self.chat_id_input.setText(config.get("chat_id", ""))
#             self.camera_index_input.setText(str(config.get("camera_index", 0)))
#             self.threshold_input.setText(str(config.get("confidence_threshold", 0.5)))
#         except Exception as e:
#             QMessageBox.warning(self, "Error", f"Failed to load settings:  {e}")

#     def save_settings(self):
#         """Simpan settings ke config.json dan update WarningManager"""
#         try: 
#             # Validasi confidence threshold
#             threshold = float(self.threshold_input.text())
#             if not (0 <= threshold <= 1):
#                 QMessageBox.warning(self, "Invalid Input", "Confidence threshold must be between 0 and 1")
#                 return

#             # Simpan ke config. json
#             config = {
#                 "model_path": self.model_path_input.text(),
#                 "telegram_token":  self.token_input.text(),
#                 "chat_id": self.chat_id_input.text(),
#                 "camera_index":  int(self.camera_index_input.text()),
#                 "confidence_threshold": threshold,
#                 "device": "auto"  # Atau bisa ditambahkan input untuk device
#             }
            
#             ConfigManager.save_config(config)

#             # Update WarningManager secara langsung jika tersedia
#             if self.warning_manager:
#                 self.warning_manager.conf_threshold = threshold
#                 self. warning_manager.detector.conf_threshold = threshold
#                 self.warning_manager.telegram_token = config["telegram_token"]
#                 self.warning_manager.chat_id = config["chat_id"]

#             QMessageBox.information(self, "Success", "Settings saved and applied successfully!")
            
#         except ValueError: 
#             QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for threshold and camera index")
#         except Exception as e:
#             QMessageBox.warning(self, "Error", f"Failed to save settings: {e}")
            
            
#update 1/10/26
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QFileDialog
from config.config_manager import ConfigManager

class SettingsWidget(QWidget):
    def __init__(self, warning_manager=None):
        super().__init__()
        self.warning_manager = warning_manager
        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        self.model_path_input = QLineEdit()
        self.model_path_input.setReadOnly(True)  # Read-only, hanya bisa diubah via browse
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_model_file)
        
        self.token_input = QLineEdit()
        self.chat_id_input = QLineEdit()
        self.camera_index_input = QLineEdit()
        self.threshold_input = QLineEdit()

        save_btn = QPushButton("Save Settings")
        save_btn.clicked. connect(self.save_settings)

        layout = QVBoxLayout()
        
        # Model Path dengan tombol Browse
        layout. addWidget(QLabel("Model Path:"))
        model_layout = QHBoxLayout()
        model_layout.addWidget(self. model_path_input)
        model_layout.addWidget(browse_btn)
        layout.addLayout(model_layout)
        
        layout.addWidget(QLabel("Telegram Bot Token:"))
        layout.addWidget(self.token_input)
        layout.addWidget(QLabel("Telegram Chat ID:"))
        layout.addWidget(self.chat_id_input)
        layout.addWidget(QLabel("Camera Index:"))
        layout.addWidget(self.camera_index_input)
        layout.addWidget(QLabel("Confidence Threshold (0-1):"))
        layout.addWidget(self.threshold_input)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def browse_model_file(self):
        """Membuka dialog untuk memilih file model"""
        # Dapatkan direktori dari model path yang ada (jika ada)
        current_path = self.model_path_input.text()
        start_dir = ""
        if current_path: 
            import os
            start_dir = os.path.dirname(current_path) if os.path.dirname(current_path) else ""
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Model File",
            start_dir,
            "PyTorch Model Files (*.pt *. pth);;All Files (*.*)"
        )
        
        if file_path:
            self.model_path_input.setText(file_path)

    def load_current_settings(self):
        """Muat settings dari config. json saat tab dibuka"""
        try:
            config = ConfigManager.load_config()
            self.model_path_input. setText(config.get("model_path", ""))
            self.token_input.setText(config. get("telegram_token", ""))
            self.chat_id_input.setText(config.get("chat_id", ""))
            self.camera_index_input. setText(str(config.get("camera_index", 0)))
            self.threshold_input.setText(str(config.get("confidence_threshold", 0.5)))
        except Exception as e: 
            QMessageBox.warning(self, "Error", f"Failed to load settings:  {e}")

    def save_settings(self):
        """Simpan settings ke config.json dan update WarningManager"""
        try: 
            # Validasi model path
            model_path = self.model_path_input.text()
            if not model_path:
                QMessageBox.warning(self, "Invalid Input", "Please select a model file")
                return
            
            # Validasi confidence threshold
            threshold = float(self. threshold_input.text())
            if not (0 <= threshold <= 1):
                QMessageBox.warning(self, "Invalid Input", "Confidence threshold must be between 0 and 1")
                return

            # Simpan ke config. json
            config = {
                "model_path": model_path,
                "telegram_token":  self.token_input.text(),
                "chat_id": self.chat_id_input.text(),
                "camera_index":  int(self.camera_index_input.text()),
                "confidence_threshold": threshold,
                "device": "auto"  # Atau bisa ditambahkan input untuk device
            }
            
            ConfigManager.save_config(config)

            # Update WarningManager secara langsung jika tersedia
            if self.warning_manager:
                self.warning_manager.conf_threshold = threshold
                self. warning_manager.detector.conf_threshold = threshold
                self.warning_manager.telegram_token = config["telegram_token"]
                self.warning_manager.chat_id = config["chat_id"]

            QMessageBox.information(self, "Success", "Settings saved and applied successfully!")
            
        except ValueError: 
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for threshold and camera index")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {e}")