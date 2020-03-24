from PyQt5.QtCore import pyqtSignal, QObject
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from LifeScritps.LifeGameModel import LifeGameModel
import numpy as np
from GameTimer import Evolutioner


class LifeGameController(QWidget):
    onSomethingHappened = pyqtSignal(list)

    def __init__(self, model: LifeGameModel):
        super(LifeGameController, self).__init__()
        self.model = model

    def on_cell_clicked(self, row, col):
        print("Cell %d, %d clicked!" % (row, col))
        new_state = 1 if self.model.cells[row, col] == 0 else 0
        self.model.changeCellStatus(row, col, new_state)

    def on_grid_change_request(self, val):
        print("Grid size: %d" % val)
        if 0 <= val <= len(self.model.grid_sizes):
            self.model.changeGridSize(val)

    def on_fps_change_request(self, val):
        self.model.changeFps(val)

    def on_conf_change_requested(self, i):
        self.model.load_config(self.model.configurations[i + 1])
        pass

    def save_configuration_requested(self):
        complete_path, _choice = QFileDialog.getSaveFileName(self, directory=self.model.data_path, filter="{} files (*{})".format(self.model.config_ext[1:], self.model.config_ext))
        if complete_path:
            self.model.save_config(complete_path)

    def step_requested(self):
        self.model.step_life()

    def stop_requested(self):
        self.model.stop()

    def play_pause_requested(self):
        if not self.model.is_playing:
            self.model.start()
        else:
            self.model.pause()
