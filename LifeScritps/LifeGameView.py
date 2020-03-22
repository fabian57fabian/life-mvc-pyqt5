from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGridWidget import LifeGridWidget
from LifeScritps.LifeGameController import LifeGameController
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox
import os


class LifeGameView(QtWidgets.QWidget):
    def __init__(self, model: LifeGameModel, controller: LifeGameController):
        super(LifeGameView, self).__init__()
        self.model = model
        self.controller = controller
        self.grid_widget = LifeGridWidget(self, model, controller)
        self.step_label = QLabel()

    def method_called(self, a: list):
        pass

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        # main_window.resize(800, 600)
        # main_window.setMaximumWidth(800)
        # main_window.setMaximumHeight(600)
        centralwidget = QtWidgets.QWidget(main_window)
        lay_vertical = QVBoxLayout()

        lay_control = QHBoxLayout()
        # TODO: set left alignment
        lay_grid = QHBoxLayout()
        lbl_grid_info = QLabel("Grid size:")
        lay_grid.addWidget(lbl_grid_info)
        cbox_select_grid = QComboBox(self)
        sizes = self.model.getsizes()
        cbox_select_grid.addItems(sizes)
        cbox_select_grid.activated[str].connect(self.controller.on_size_selected)
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

        lay_vertical.setAlignment(Qt.AlignCenter)
        lay_vertical.addWidget(self.grid_widget)

        lay_footer = QHBoxLayout()
        self.step_label.setText(("Step: 0"))
        lay_footer.addWidget(self.step_label)
        cbox_select_conf = QComboBox(self)
        confs = self.model.configurations
        confs.insert(0, "blank")
        cbox_select_conf.addItems(confs)
        cbox_select_conf.currentIndexChanged.connect(self.controller.on_conf_changed)
        lay_footer.addWidget(cbox_select_conf)

        lay_vertical.addLayout(lay_footer)

        centralwidget.setLayout(lay_vertical)
        main_window.setCentralWidget(centralwidget)
