from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGridWidget import LifeGridWidget
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox
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

        lay_control = QHBoxLayout()
        # TODO: set left alignment
        lay_grid = QHBoxLayout()
        lbl_grid_info = QLabel("Grid size:")
        lay_grid.addWidget(lbl_grid_info)
        cbox_select_grid = QComboBox(self)
        sizes = ["100x100", "200x200", "300x300", "400x400", "500x500"]
        cbox_select_grid.addItems(sizes)
        for size in sizes:
            cbox_select_grid.activated[str].connect(self.on_size_selected)
        lay_grid.addWidget(cbox_select_grid)
        lay_grid.setAlignment(Qt.AlignLeft)
        lay_control.addLayout(lay_grid)

        lay_playpause = QHBoxLayout()
        btn_playpause = QPushButton()
        btn_playpause.setIcon(QtGui.QIcon(self.model.getIconPath('play')))
        btn_stop = QPushButton()
        btn_stop.setIcon(QtGui.QIcon(self.model.getIconPath('stop')))
        lay_playpause.addWidget(btn_playpause)
        lay_playpause.addWidget(btn_stop)
        lay_playpause.setAlignment(Qt.AlignCenter)
        lay_control.addLayout(lay_playpause)

        lay_manage_saved_sessions = QHBoxLayout()
        btn_load_sess = QPushButton()
        btn_load_sess.setIcon(QtGui.QIcon(self.model.getIconPath('open')))
        btn_save_sess = QPushButton()
        btn_save_sess.setIcon(QtGui.QIcon(self.model.getIconPath('save')))
        lay_manage_saved_sessions.addWidget(btn_load_sess)
        lay_manage_saved_sessions.addWidget(btn_save_sess)
        lay_manage_saved_sessions.setAlignment(Qt.AlignRight)
        lay_control.addLayout(lay_manage_saved_sessions)

        lay_vertical.addLayout(lay_control)

        centralwidget.setLayout(lay_vertical)
        main_window.setCentralWidget(centralwidget)

    def on_size_selected(self, selected_size):
        pass
