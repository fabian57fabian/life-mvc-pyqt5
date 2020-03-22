from PyQt5.QtCore import QTimer, pyqtSignal, QObject


class Evolutioner(QObject):
    onStepTrieggered = pyqtSignal()

    def __init__(self):
        super(Evolutioner, self).__init__()
        self.timer = QTimer()
        self.set_fps(1)
        self.timer.timeout.connect(self.onTimeoutShot)

    def onTimeoutShot(self):
        self.onStepTrieggered.emit()

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start()

    def set_fps(self, fps: int):
        self.timer.setInterval(1000 / fps)
