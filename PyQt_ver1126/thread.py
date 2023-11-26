# This Python file uses the following encoding: utf-8
import numpy as np
from PySide2.QtCore import Signal, QThread
from cv2 import VideoCapture


class RunVideo(QThread):
    matSignal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = None
        self.running = True

    def run(self):
        try:
            if self.cap is None:
                self.cap = VideoCapture(1)
                if not self.cap.isOpened():
                    raise RuntimeError("Failed to o+pen cam")
                while self.running:
                    ret, img = self.cap.read()
                    if ret:
                        self.matSignal.emit(img)
        except Exception as e:
            print(f"Error : {e}")

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.quit()
