from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGridWidget import LifeGridWidget
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QLineEdit
import os


class LifeGameView(QtWidgets.QWidget):
    def __init__(self, model: LifeGameModel):
        super().__init__()
        self.model = model
        self.grid_widget = LifeGridWidget(self)
        self.model.onSomethingHappened.connect(self.method_called)

    def method_called(self, a: list):
        pass

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMaximumWidth(800)
        main_window.setMaximumHeight(600)
        centralwidget = QtWidgets.QWidget(main_window)
        lay_vertical = QVBoxLayout()
        centralwidget.setLayout(lay_vertical)
        main_window.setCentralWidget(centralwidget)
