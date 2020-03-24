from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGridWidget import LifeGridWidget
from LifeScritps.LifeGameController import LifeGameController
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox, QSlider
import os


class LifeGameView(QtWidgets.QWidget):
    def __init__(self, model: LifeGameModel, controller: LifeGameController):
        super(LifeGameView, self).__init__()
        self.model = model
        self.controller = controller
        self.grid_widget = LifeGridWidget(self, model, controller)
        self.grid_label = QLabel()
        #self.grid_size_slider = QSlider(Qt.Horizontal, self)
        self.step_label = QLabel()
        self.clear_btn = QPushButton()
        self.cbox_select_conf = QComboBox(self)
        self.fps_label = QLabel()
        self.fps_slider = QSlider(Qt.Horizontal, self)

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
        #self.grid_label.setText("Grid: size:")
        #self.grid_size_slider.setMinimum(1)
        #self.grid_size_slider.setMaximum(len(self.model.grid_sizes) - 1)
        #self.grid_size_slider.setValue(1)
        #self.grid_size_slider.setTickPosition(QSlider.TicksBelow)
        #self.grid_size_slider.setTickInterval(1)
        #self.grid_size_slider.valueChanged.connect(self.controller.on_grid_change_request)
        self.setGridSizeUI(self.model.rows, self.model.cols)
        lay_grid.addWidget(self.grid_label)
        #lay_grid.addWidget(self.grid_size_slider)
        lay_grid.setAlignment(Qt.AlignLeft)
        lay_control.addLayout(lay_grid)

        lay_playpause = QHBoxLayout()
        btn_step = QPushButton()
        self.btn_playpause = QPushButton()
        self.btn_playpause.setIcon(QtGui.QIcon(self.model.getIconPath('play')))
        self.btn_playpause.clicked.connect(self.controller.play_pause_requested)
        btn_step.setIcon(QtGui.QIcon(self.model.getIconPath('step')))
        btn_step.clicked.connect(self.controller.step_requested)
        btn_stop = QPushButton()
        btn_stop.setIcon(QtGui.QIcon(self.model.getIconPath('stop')))
        btn_stop.clicked.connect(self.controller.stop_requested)
        self.clear_btn.setIcon(QtGui.QIcon(self.model.getIconPath('clear')))
        self.clear_btn.clicked.connect(self.controller.clearRequested)
        lay_playpause.addWidget(self.btn_playpause)
        lay_playpause.addWidget(btn_step)
        lay_playpause.addWidget(btn_stop)
        lay_playpause.addWidget(self.clear_btn)
        lay_playpause.setAlignment(Qt.AlignCenter)
        lay_control.addLayout(lay_playpause)

        lay_manage_saved_sessions = QHBoxLayout()
        # btn_load_sess = QPushButton()
        # btn_load_sess.setIcon(QtGui.QIcon(self.model.getIconPath('open')))
        btn_save_sess = QPushButton()
        btn_save_sess.setIcon(QtGui.QIcon(self.model.getIconPath('save')))
        btn_save_sess.clicked.connect(self.controller.save_configuration_requested)
        # lay_manage_saved_sessions.addWidget(btn_load_sess)
        lay_manage_saved_sessions.addWidget(btn_save_sess)
        lay_manage_saved_sessions.setAlignment(Qt.AlignRight)
        lay_control.addLayout(lay_manage_saved_sessions)

        lay_vertical.addLayout(lay_control)

        # lay_vertical.setAlignment(Qt.AlignCenter)
        self.grid_widget.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        lay_vertical.addWidget(self.grid_widget)

        lay_footer = QHBoxLayout()
        self.step_label.setText("Step: 0")
        self.fps_label.setText("Fps: 1")
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(50)
        self.fps_slider.setValue(1)
        #self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_slider.setTickInterval(1)
        self.fps_slider.valueChanged[int].connect(self.controller.on_fps_change_request)
        lay_footer.addWidget(self.step_label)
        lay_footer.addWidget(self.fps_label)
        lay_footer.addWidget(self.fps_slider)
        confs = self.model.configurations
        confs.insert(0, "blank")
        self.cbox_select_conf.addItems(confs)
        self.cbox_select_conf.currentIndexChanged.connect(self.controller.on_conf_change_requested)
        lay_footer.addWidget(self.cbox_select_conf)

        lay_vertical.addLayout(lay_footer)

        centralwidget.setLayout(lay_vertical)
        main_window.setCentralWidget(centralwidget)

        self.model.onPlayStateChanged.connect(self.playStateChanged)
        self.model.onStepChanged.connect(self.stepChanged)
        self.model.onFpsChanged.connect(self.fpsChanged)
        self.model.onSizeChanged.connect(self.setGridSizeUI)

        self.controller.onBlankConfigRequested.connect(self.setBlankConfig)

    def setBlankConfig(self):
        self.cbox_select_conf.blockSignals(True)
        self.cbox_select_conf.setCurrentIndex(0)
        self.cbox_select_conf.blockSignals(False)

    def playStateChanged(self, is_running):
        if is_running:
            self.btn_playpause.setIcon(QtGui.QIcon(self.model.getIconPath('pause')))
        else:
            self.btn_playpause.setIcon(QtGui.QIcon(self.model.getIconPath('play')))

    def stepChanged(self, step):
        self.step_label.setText("Step: " + str(step))

    def fpsChanged(self, fps):
        self.fps_label.setText("Fps: " + str(fps))

    def setGridSizeUI(self, rows, cols):
        self.grid_label.setText("Size: %dx%d" % (rows, cols))
