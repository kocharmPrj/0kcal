# This Python file uses the following encoding: utf-8
import np
from PySide2.QtCore import Signal, QThread, QObject
from cv2 import VideoCapture

class ThreadWorker(QThread):
    matSignal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            self.num += 1

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False


class RunVideo(ThreadWorker):
    def __init__(self):
        super().__init__()
        self.cap = VideoCapture(0)

    def run(self):
        while self.running:
            ret, img = self.cap.read()
            if ret:
                self.matSignal.emit(img)
