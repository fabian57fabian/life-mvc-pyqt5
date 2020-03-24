from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import time


class Evolutioner(QObject):
    onStepTrieggered = pyqtSignal()

    def __init__(self):
        super(Evolutioner, self).__init__()
        self.timer = QTimer()
        self.fps = 0
        self.set_fps(1)
        self.timer.timeout.connect(self.onTimeoutShot)

    def onTimeoutShot(self):
        start_ts = time.time()
        self.onStepTrieggered.emit()
        slot_time = 10 ** 6 / self.fps
        remainig_time = (slot_time - (time.time() - start_ts))/1000
        if remainig_time>0:
            self.timer.setInterval(remainig_time)

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start()

    def set_fps(self, fps: int):
        self.fps = fps
        self.timer.setInterval(1000 / fps)
