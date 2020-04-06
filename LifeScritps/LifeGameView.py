from functools import partial

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGridWidget import LifeGridWidget
from LifeScritps.LifeGameController import LifeGameController
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFormLayout, QMainWindow, \
    QInputDialog, QLineEdit, QComboBox, QSlider, QWidget
import os


class LifeGameView(QtWidgets.QWidget):
    def __init__(self, model: LifeGameModel, controller: LifeGameController):
        super(LifeGameView, self).__init__()
        self.model = model
        self.controller = controller
        self.mainLayout = QVBoxLayout()
        self.grid_widget = LifeGridWidget(self, model, controller)
        self.cBoxSize = QComboBox()
        self.btn_playpause = QPushButton()
        self.btn_step = QPushButton()
        self.btn_stop = QPushButton()
        self.step_label = QLabel()
        self.clear_btn = QPushButton()
        self.cbox_select_conf = QComboBox(self)
        self.fps_label = QLabel()
        self.fps_slider = QSlider(Qt.Horizontal, self)

    def method_called(self, a: list):
        pass

    def setupUi(self, main_window: QMainWindow):
        main_window.setObjectName("main_window")
        centralwidget = QtWidgets.QWidget(main_window)

        lay_control = QHBoxLayout()
        self.cBoxSize.addItems(['{}x{}'.format(w, h) for w, h in self.model.grid_sizes])
        self.cBoxSize.currentIndexChanged.connect(self.controller.on_grid_change_request)
        self.cBoxSize.setMaximumWidth(70)
        lay_control.addWidget(self.cBoxSize)

        lay_playpause = QHBoxLayout()

        self.btn_playpause.setIcon(QtGui.QIcon(self.model.getIconPath('play')))
        self.btn_step.setIcon(QtGui.QIcon(self.model.getIconPath('step')))
        self.btn_stop.setIcon(QtGui.QIcon(self.model.getIconPath('stop')))
        self.clear_btn.setIcon(QtGui.QIcon(self.model.getIconPath('clear')))

        self.btn_playpause.clicked.connect(self.controller.play_pause_requested)
        self.btn_step.clicked.connect(self.controller.step_requested)
        self.btn_stop.clicked.connect(self.controller.stop_requested)
        self.clear_btn.clicked.connect(self.controller.clearRequested)

        lay_playpause.addWidget(self.btn_playpause)
        lay_playpause.addWidget(self.btn_step)
        lay_playpause.addWidget(self.btn_stop)
        lay_playpause.addWidget(self.clear_btn)
        lay_playpause.setAlignment(Qt.AlignCenter)
        lay_control.addLayout(lay_playpause)

        lay_manage_saved_sessions = QHBoxLayout()
        btn_save_sess = QPushButton()
        btn_save_sess.setIcon(QtGui.QIcon(self.model.getIconPath('save')))
        btn_save_sess.clicked.connect(self.controller.save_configuration_requested)
        lay_manage_saved_sessions.addWidget(btn_save_sess)
        lay_manage_saved_sessions.setAlignment(Qt.AlignRight)
        wid_right = QWidget()
        wid_right.setFixedWidth(70)
        wid_right.setLayout(lay_manage_saved_sessions)
        lay_control.addWidget(wid_right)

        self.mainLayout.addLayout(lay_control)

        self.grid_widget.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.mainLayout.addWidget(self.grid_widget)

        lay_footer = QHBoxLayout()
        self.step_label.setText("Step: 0")
        self.fps_label.setText("Fps: 1")
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(50)
        self.fps_slider.setValue(1)
        # self.fps_slider.setTickPosition(QSlider.TicksBelow)
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

        self.mainLayout.addLayout(lay_footer)

        centralwidget.setLayout(self.mainLayout)
        main_window.setCentralWidget(centralwidget)
        self.initConnectors()

    def initConnectors(self):
        self.model.onPlayStateChanged.connect(self.playStateChanged)
        self.model.onStepChanged.connect(self.stepChanged)
        self.model.onFpsChanged.connect(self.fpsChanged)
        self.model.onSizeChanged.connect(self.setGridSizeUI)
        self.setGridSizeUI(self.model.rows, self.model.cols)
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
        pass  # self.grid_label.setText("%dx%d" % (rows, cols))
