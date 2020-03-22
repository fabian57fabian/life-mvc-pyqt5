import os
from PyQt5.QtCore import pyqtSignal, QObject


class LifeGameModel(QObject):
    onSomethingHappened = pyqtSignal(list)

    def __init__(self):
        super(LifeGameModel, self).__init__()
        self.data_path = "../"

    def load_data(self):
        pass
