import mss
import numpy as np

class ScreenCapture:
    def __init__(self, region):
        # region: (x1, y1, x2, y2)
        self.left = int(region[0])
        self.top = int(region[1])
        self.width = int(region[2] - region[0])
        self.height = int(region[3] - region[1])
        self.sct = mss.mss()

    def grab(self):
        monitor = {
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height
        }
        img = self.sct.grab(monitor)
        # mss returns BGRA, convert to RGB
        arr = np.array(img)[..., :3]
        arr = arr[..., ::-1]  # BGR to RGB
        return arr 