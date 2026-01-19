from ultralytics import YOLO

class YoloV11Wrapper:
    def __init__(self, model_path, device='cpu'):
        self.model = YOLO(model_path)
        self.device = device  # 'cpu' or 'cuda' or '0' etc.
        # optional: move model to cuda if using torch-style .to()
        try:
            # Ultralytics model has .to() — memindahkan model ke device jika ingin
            if str(self.device).startswith("cuda") or self.device == "0" or self.device == "1":
                self.model.to('cuda')
        except Exception:
            pass

    def predict(self, frame):
        # berjalan di device yang kita set
        results = self.model.predict(source=frame, device=self.device, stream=False, verbose=False)
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_name = self.model.names[cls_id]
                detections.append((class_name, conf, (x1, y1, x2, y2)))
        return detections
