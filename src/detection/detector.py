from ultralytics import YOLO
import numpy as np

# COCO class name to id mapping (основные классы)
COCO_CLASS_NAME_TO_ID = {
    "person": 0,
    "bicycle": 1,
    "car": 2,
    "motorcycle": 3,
    "bus": 5,
    "truck": 7,
    "train": 6,
    "boat": 9,
    "traffic light": 10,
    "fire hydrant": 11,
    "stop sign": 13,
    "parking meter": 14,
    "bench": 15,
    # ... можно добавить больше классов по необходимости
}

class Detector:
    def __init__(self, model_path, conf, device='cpu', monitored_classes=None):
        self.model = YOLO(model_path)
        self.conf = conf
        self.device = device
        if monitored_classes is None:
            monitored_classes = ["car", "bus", "truck"]
        self.target_classes = set(
            COCO_CLASS_NAME_TO_ID[name] for name in monitored_classes if name in COCO_CLASS_NAME_TO_ID
        )

    def detect(self, img):
        # img: numpy array (RGB)
        results = self.model(img, conf=self.conf, verbose=False, device=self.device)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in self.target_classes:
                    return True
        return False 