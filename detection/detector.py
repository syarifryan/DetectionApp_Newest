from detection.yolo_wrapper import YoloV11Wrapper

class Detector:
    def __init__(self, model_path, conf_threshold=0.5, device='cuda'):
        self.wrapper = YoloV11Wrapper(model_path, device=device)
        self.conf_threshold = conf_threshold

    def predict(self, frame):
        # Gunakan wrapper YOLO untuk mendapatkan deteksi mentah
        detections = self.wrapper.predict(frame)
        # Filter berdasarkan confidence threshold
        filtered = [det for det in detections if det[1] >= self.conf_threshold]
        return filtered
