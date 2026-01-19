# from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
# import cv2
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer, Qt

# class RealtimeWidget(QWidget):
#     def __init__(self, warning_manager):
#         super().__init__()
#         self.warning_manager = warning_manager

#         self.init_ui()
#         self.cap = None
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)

#     def init_ui(self):
#         self.start_button = QPushButton("Start Real-Time")
#         self.stop_button = QPushButton("Stop Real-Time")
#         self.image_label = QLabel()
#         self.image_label.setFixedSize(640, 480)
#         self.image_label.setStyleSheet("border: 1px solid black")

#         self.start_button.clicked.connect(self.start_realtime)
#         self.stop_button.clicked.connect(self.stop_realtime)

#         layout = QVBoxLayout()
#         layout.addWidget(self.image_label)
#         layout.addWidget(self.start_button)
#         layout.addWidget(self.stop_button)
#         self.setLayout(layout)

#     def start_realtime(self):
#         self.cap = cv2.VideoCapture(0)
#         self.timer.start(30)

#     def stop_realtime(self):
#         if self.cap:
#             self.cap.release()
#         self.timer.stop()

#     def update_frame(self):
#         if self.cap:
#             ret, frame = self.cap.read()
#             if ret:
#                 frame = self.warning_manager.process_frame(frame)

#                 frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = frame_rgb.shape
#                 qimg = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
#                 pixmap = QPixmap.fromImage(qimg)
#                 scaled_pixmap = pixmap.scaled(
#                     self.image_label.width(),
#                     self.image_label.height(),
#                     Qt.KeepAspectRatio,
#                     Qt.SmoothTransformation
#                 )
#                 self.image_label.setPixmap(scaled_pixmap)

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2

class RealtimeWidget(QWidget):
    def __init__(self, warning_manager):
        super().__init__()
        self.warning_manager = warning_manager

        # Dropdown pilihan kamera
        self.camera_selector = QComboBox()
        self.scan_cameras()  # isi daftar kamera yang tersedia

        self.start_button = QPushButton("Start Real-Time")
        self.stop_button = QPushButton("Stop Real-Time")
        self.stop_button.setEnabled(False)

        self.image_label = QLabel("Click the Start button to begin")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("background: #fff; border: 1px solid #888;")

        self.start_button.clicked.connect(self.start_realtime)
        self.stop_button.clicked.connect(self.stop_realtime)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Select Camera:"))
        top_layout.addWidget(self.camera_selector)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.image_label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def scan_cameras(self):
        """Scan semua kamera yang tersedia dan tambahkan ke combo box."""
        self.camera_selector.clear()
        found = False
        for index in range(5):  # cek kamera index 0-4
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                self.camera_selector.addItem(f"Camera {index}", index)
                found = True
                cap.release()
        if not found:
            self.camera_selector.addItem("No camera detected", -1)

    def start_realtime(self):
        selected_index = self.camera_selector.currentData()
        if selected_index == -1:
            QMessageBox.warning(self, "Error", "No camera available.")
            return

        self.cap = cv2.VideoCapture(selected_index)
        if self.cap.isOpened():
            self.timer.start(30)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Error", f"Failed to open camera {selected_index}")

    # def stop_realtime(self):
    #     self.timer.stop()
    #     if self.cap:
    #         self.cap.release()
    #     self.start_button.setEnabled(True)
    #     self.stop_button.setEnabled(False)
    
    def stop_realtime(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None  # ✅ Reset ke None
        
        # ✅ Hapus gambar dan tampilkan teks
        self.image_label.clear()
        self.image_label.setText("Click the Start button to begin")
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)    
    

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = self.warning_manager.process_frame(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qimg = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qimg).scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

