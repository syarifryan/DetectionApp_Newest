#latest
# import cv2
# import os
# import datetime
# import threading
# import time
# import requests

# from detection.detector import Detector
# from config.config_manager import ConfigManager

# class WarningManager:
#     def __init__(self, model_path, telegram_token, chat_id, conf_threshold=0.25, device='cuda'):
#         """
#         model_path      : Path model YOLO
#         telegram_token  : Token bot Telegram
#         chat_id         : Chat ID penerima notifikasi
#         conf_threshold  : Batas minimum confidence deteksi
#         device          : 'cuda' untuk GPU, 'cpu' jika tidak ada GPU
#         """
#         self.detector = Detector(model_path, conf_threshold, device)
#         self.telegram_token = telegram_token
#         self.chat_id = chat_id
#         self.conf_threshold = conf_threshold

#         # Buffer & timer untuk notifikasi setiap 10 detik
#         self.alert_buffer = []  # Simpan tuple (conf, class_name, frame, box)
#         self.last_alert_sent_time = time.time()
#         self.alert_interval = 10  # detik

#     def process_frame(self, frame):
#         detections = self.detector.predict(frame)  # tanpa argumen conf
#         print(f"[INFO] Detections: {detections}")
#         alert_triggered = False

#         for class_name, conf, (x1, y1, x2, y2) in detections:
#             if conf >= self.conf_threshold:
#                 alert_triggered = True
#                 label = f"{class_name} ({conf:.2f})"
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                 cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                             0.5, (0, 255, 0), 2)

#                 # Tambahkan ke buffer kandidat notifikasi
#                 self.alert_buffer.append((conf, class_name, frame.copy(), (x1, y1, x2, y2)))

#         # Cek waktu: jika sudah lewat 10 detik, kirim notifikasi
#         current_time = time.time()
#         if current_time - self.last_alert_sent_time >= self.alert_interval and self.alert_buffer:
#             self.last_alert_sent_time = current_time
#             threading.Thread(target=self.send_top_confidence_alert, daemon=True).start()

#         return frame  # tetap kembalikan frame untuk ditampilkan

#     def send_top_confidence_alert(self):
#         if not self.alert_buffer:
#             return

#         # Ambil deteksi dengan confidence tertinggi
#         top = max(self.alert_buffer, key=lambda x: x[0])
#         conf, class_name, frame, (x1, y1, x2, y2) = top

#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f'detected_{timestamp}.jpg'
#         filepath = os.path.join("temp", filename)
#         os.makedirs("temp", exist_ok=True)

#         try:
#             # Tambahkan bounding box (opsional)
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#             cv2.putText(frame, f'{class_name} ({conf:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                         0.5, (0, 255, 0), 2)
#             cv2.imwrite(filepath, frame)
#         except Exception as e:
#             print(f"[ERROR] Gagal menyimpan gambar alert: {e}")
#             return

#         message = f"🚨 Early Warning System 🚨\n"
#         message += f"Date_Time: {timestamp}\n"
#         message += f"• {class_name} ({conf:.2f})\n"

#         try:
#             url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
#             with open(filepath, 'rb') as photo:
#                 response = requests.post(
#                     url,
#                     data={'chat_id': self.chat_id, 'caption': message},
#                     files={'photo': photo},
#                     timeout=10
#                 )
#                 response.raise_for_status()
#                 print("[INFO] Notifikasi Telegram dikirim.")
#         except Exception as e:
#             print(f"[ERROR] Gagal kirim notifikasi: {e}")

#         # Kosongkan buffer setelah dikirim
#         self.alert_buffer.clear()


#new
import cv2
import os
import datetime
import threading
import time
import requests

from detection.detector import Detector
from config.config_manager import ConfigManager

class WarningManager: 
    def __init__(self, model_path, telegram_token, chat_id, conf_threshold=0.25, device='cuda'):
        """
        model_path      : Path model YOLO
        telegram_token  : Token bot Telegram
        chat_id         : Chat ID penerima notifikasi
        conf_threshold  :  Batas minimum confidence deteksi
        device          : 'cuda' untuk GPU, 'cpu' jika tidak ada GPU
        """
        self.detector = Detector(model_path, conf_threshold, device)
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.conf_threshold = conf_threshold

        # Buffer & timer untuk notifikasi setiap 5detik
        self.alert_buffer = []  # Simpan tuple (conf, class_name, frame, box)
        self.current_frame_detections = []  # Deteksi dalam frame saat ini
        self.last_alert_sent_time = time. time()
        self.alert_interval = 5 # detik

    def process_frame(self, frame):
        detections = self.detector.predict(frame)
        print(f"[INFO] Detections: {detections}")
        
        # Reset deteksi frame saat ini
        self.current_frame_detections = []
        alert_triggered = False

        for class_name, conf, (x1, y1, x2, y2) in detections:
            # ✅ FILTER:  Skip class "non-violence"
            if class_name. lower() == "non-violence":
                continue
                
            if conf >= self.conf_threshold:
                alert_triggered = True
                label = f"{class_name} ({conf:.2f})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

                # Simpan deteksi frame saat ini
                self.current_frame_detections.append((conf, class_name, (x1, y1, x2, y2)))

        # Jika ada deteksi valid (bukan non-violence), tambahkan ke buffer dengan snapshot frame
        if self.current_frame_detections:
            self.alert_buffer. append({
                'frame': frame.copy(),
                'detections': self.current_frame_detections. copy(),
                'timestamp': time.time()
            })

        # Cek waktu: jika sudah lewat 10 detik, kirim notifikasi
        current_time = time. time()
        if current_time - self.last_alert_sent_time >= self.alert_interval and self.alert_buffer:
            self.last_alert_sent_time = current_time
            threading.Thread(target=self. send_alert_with_all_classes, daemon=True).start()

        return frame

    def send_alert_with_all_classes(self):
        """Kirim alert dengan semua class yang terdeteksi (kecuali non-violence)"""
        if not self.alert_buffer:
            return

        # Ambil frame dengan deteksi terbanyak atau confidence tertinggi
        best_detection = max(self.alert_buffer, key=lambda x: len(x['detections']))
        frame = best_detection['frame']
        detections = best_detection['detections']

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'detected_{timestamp}.jpg'
        filepath = os.path. join("temp", filename)
        os.makedirs("temp", exist_ok=True)

        try:
            # Gambar bounding box untuk semua deteksi
            for conf, class_name, (x1, y1, x2, y2) in detections:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'{class_name} ({conf:.2f})', (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            cv2.imwrite(filepath, frame)
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan gambar alert: {e}")
            return

        # ✅ PESAN:  Tampilkan semua class yang terdeteksi
        message = f"🚨 Early Warning System 🚨\n"
        message += f"Date_Time: {timestamp}\n"
        
        # Kumpulkan semua class unik
        unique_classes = {}
        for conf, class_name, _ in detections:
            if class_name not in unique_classes or conf > unique_classes[class_name]:
                unique_classes[class_name] = conf
        
        # Tambahkan info jika multi-class terdeteksi
        if len(unique_classes) > 1:
            message += f"⚠️ MULTIPLE THREATS DETECTED ⚠️\n"
        
        # List semua class
        message += f"\nDetected Objects:\n"
        for class_name, conf in sorted(unique_classes.items(), key=lambda x: x[1], reverse=True):
            message += f"• {class_name} ({conf:.2f})\n"
        
        message += f"\nTotal:  {len(detections)} object(s) in frame"

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
            with open(filepath, 'rb') as photo:
                response = requests. post(
                    url,
                    data={'chat_id':  self.chat_id, 'caption': message},
                    files={'photo': photo},
                    timeout=10
                )
                response.raise_for_status()
                print(f"[INFO] Notifikasi Telegram dikirim:  {', '.join(unique_classes.keys())}")
        except Exception as e:
            print(f"[ERROR] Gagal kirim notifikasi: {e}")

        # Kosongkan buffer setelah dikirim
        self.alert_buffer. clear()