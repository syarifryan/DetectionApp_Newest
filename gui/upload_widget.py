#new 10/1/26
# import os
# import cv2
# import threading
# import time
# from datetime import datetime
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
# from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt
# import torch  # pastikan torch sudah terinstall

# class UploadWidget(QWidget):
#     def __init__(self, warning_manager, parent=None):
#         super().__init__(parent)
#         self.warning_manager = warning_manager
#         self.is_processing = False  # Flag untuk tracking proses
#         self.stop_flag = False  # Flag untuk stop proses video

#         # # Pastikan YOLO berjalan di GPU jika tersedia
#         # if torch.cuda.is_available():
#         #     self.warning_manager.detector.model.to('cuda')
#         #     print("✅ Model dijalankan di GPU")
#         # else:
#         #     print("⚠ GPU tidak terdeteksi, menggunakan CPU")

#         layout = QVBoxLayout()

#         # ✅ PERBAIKAN:  Ubah dari setFixedSize ke setMinimumSize dan tambahkan styling
#         self.preview_label = QLabel("Preview akan muncul di sini")
#         self.preview_label.setAlignment(Qt.AlignCenter)
#         self.preview_label. setMinimumSize(640, 480)  # ✅ Ubah dari setFixedSize
#         self.preview_label.setStyleSheet("background: #fff; border: 1px solid #888;")  # ✅ Tambahkan styling
#         layout.addWidget(self. preview_label)

#         # ✅ TAMBAHAN: Layout horizontal untuk button Upload dan Clear
#         button_layout = QHBoxLayout()
        
#         self.upload_btn = QPushButton("Upload File")
#         self.upload_btn.clicked.connect(self. upload_file)
#         button_layout.addWidget(self.upload_btn)
        
#         self.clear_btn = QPushButton("Clear")
#         self.clear_btn.clicked.connect(self.clear_preview)
#         self.clear_btn.setEnabled(False)  # Disabled saat belum ada file
#         button_layout.addWidget(self.clear_btn)
        
#         layout.addLayout(button_layout)
#         self.setLayout(layout)

#     def upload_file(self):
#         file_path, _ = QFileDialog.getOpenFileName(
#             self, "Pilih File", "", "Video/Gambar (*.mp4 *.avi *.jpg *.jpeg *. png)"
#         )
#         if file_path:
#             self. clear_btn.setEnabled(True)  # ✅ Enable button clear
#             self.stop_flag = False  # ✅ Reset stop flag
            
#             ext = os.path. splitext(file_path)[1].lower()
#             if ext in [".jpg", ".jpeg", ". png"]: 
#                 self.detect_image(file_path)
#             elif ext in [".mp4", ".avi"]:
#                 self.is_processing = True  # ✅ Set flag processing
#                 threading.Thread(target=self.detect_video, args=(file_path,), daemon=True).start()

#     def clear_preview(self):
#         """✅ TAMBAHAN: Kosongkan preview dan stop proses video jika sedang berjalan"""
#         # Set stop flag untuk menghentikan video processing
#         if self.is_processing:
#             self.stop_flag = True
#             self.is_processing = False
#             print("⏹ Proses deteksi dihentikan")
        
#         # Kosongkan preview
#         self.preview_label. clear()
#         self.preview_label.setText("Preview akan muncul di sini")
#         self.clear_btn.setEnabled(False)

#     def detect_image(self, file_path):
#         frame = cv2.imread(file_path)
#         processed_frame = self.warning_manager.process_frame(frame)
#         self.display_frame(processed_frame)

#         # Simpan hasil deteksi
#         out_path = f"output_result/image/detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
#         cv2.imwrite(out_path, processed_frame)
#         print(f"Gambar hasil deteksi tersimpan:  {out_path}")

#     def detect_video(self, file_path):
#         cap = cv2.VideoCapture(file_path)
#         if not cap.isOpened():
#             print("Gagal membuka video")
#             self.is_processing = False  # ✅ Reset flag
#             return

#         # Ambil FPS asli
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         fps = fps if fps and fps > 0 else 30.0
#         frame_delay = max(1 / fps, 0.001)

#         # Siapkan VideoWriter
#         fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#         out_path = f"output_result/video/detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

#         # ✅ PERBAIKAN: Tambahkan pengecekan stop_flag
#         while cap.isOpened() and not self.stop_flag:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             processed_frame = self.warning_manager.process_frame(frame)
#             out.write(processed_frame)
#             self.display_frame(processed_frame)

#             time.sleep(frame_delay)  # Playback sesuai FPS

#         cap.release()
#         out.release()
        
#         # ✅ TAMBAHAN:  Pesan berbeda untuk stop manual vs selesai normal
#         if self.stop_flag:
#             print(f"⚠ Video processing dihentikan.  Hasil parsial tersimpan:  {out_path}")
#         else:
#             print(f"✅ Video hasil deteksi tersimpan: {out_path}")
        
#         self.is_processing = False  # ✅ Reset flag processing

#     def display_frame(self, frame):
#         """Tampilkan frame di QLabel preview."""
#         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(qimg)
        
#         # ✅ PERBAIKAN: Tambahkan Qt. SmoothTransformation untuk kualitas lebih baik
#         self.preview_label.setPixmap(pixmap.scaled(
#             self.preview_label.width(), 
#             self.preview_label.height(), 
#             Qt.KeepAspectRatio,
#             Qt.SmoothTransformation  # ✅ Tambahkan parameter ini
#         ))


import os
import cv2
import threading
import time
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import torch  # pastikan torch sudah terinstall

class UploadWidget(QWidget):
    def __init__(self, warning_manager, parent=None):
        super().__init__(parent)
        self.warning_manager = warning_manager
        self.is_processing = False  # Flag untuk tracking proses
        self.stop_flag = False  # Flag untuk stop proses video

        layout = QVBoxLayout()

        self.preview_label = QLabel("Preview akan muncul di sini")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label. setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("background:  #fff; border: 1px solid #888;")
        layout.addWidget(self.preview_label)

        # Layout horizontal untuk button Upload dan Clear
        button_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload File")
        self.upload_btn.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_btn)
        
        self. clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self. clear_preview)
        self.clear_btn.setEnabled(False)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File", "", "Video/Gambar (*.mp4 *.avi *.jpg *. jpeg *.png)"
        )
        if file_path: 
            self.clear_btn.setEnabled(True)
            self.stop_flag = False
            
            ext = os. path.splitext(file_path)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:  
                self.detect_image(file_path)
            elif ext in [".mp4", ". avi"]:
                self. is_processing = True
                threading.Thread(target=self.detect_video, args=(file_path,), daemon=True).start()

    def clear_preview(self):
        """Kosongkan preview dan stop proses video jika sedang berjalan"""
        if self.is_processing:
            self.stop_flag = True
            self.is_processing = False
            print("⏹ Proses deteksi dihentikan")
        
        self.preview_label.clear()
        self.preview_label.setText("Preview akan muncul di sini")
        self.clear_btn.setEnabled(False)

    def detect_image(self, file_path):
        frame = cv2.imread(file_path)
        processed_frame = self.warning_manager.process_frame(frame)
        self.display_frame(processed_frame)

        out_path = f"output_result/image/detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(out_path, processed_frame)
        print(f"Gambar hasil deteksi tersimpan:  {out_path}")

    def detect_video(self, file_path):
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Gagal membuka video")
            self.is_processing = False
            return

        # Ambil FPS asli
        fps = cap.get(cv2.CAP_PROP_FPS)
        fps = fps if fps and fps > 0 else 30.0
        frame_delay = 1.0 / fps
        
        print(f"[INFO] Video FPS: {fps}, Frame delay: {frame_delay:.4f}s")

        # Siapkan VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out_path = f"output_result/video/detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        # Timing yang dinamis
        while cap. isOpened() and not self.stop_flag:
            frame_start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break

            # Proses frame
            processed_frame = self.warning_manager. process_frame(frame)
            out.write(processed_frame)
            self.display_frame(processed_frame)

            # Hitung waktu yang sudah terpakai dan sleep jika perlu
            elapsed = time.time() - frame_start_time
            remaining = frame_delay - elapsed
            
            if remaining > 0:
                time.sleep(remaining)

        cap.release()
        out.release()
        
        if self.stop_flag:
            print(f"⚠ Video processing dihentikan.  Hasil parsial tersimpan:  {out_path}")
        else:
            print(f"✅ Video hasil deteksi tersimpan: {out_path}")
        
        self.is_processing = False

    def display_frame(self, frame):
        """Tampilkan frame di QLabel preview."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        
        self.preview_label.setPixmap(pixmap.scaled(
            self.preview_label.width(), 
            self.preview_label.height(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))