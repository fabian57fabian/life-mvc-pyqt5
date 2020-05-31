from PyQt5.QtCore import pyqtSignal, QObject
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from LifeScritps.LifeGameModel import LifeGameModel
import numpy as np
from GameTimer import Evolutioner


class LifeGameController(QWidget):
    onBlankConfigRequested = pyqtSignal()

    def __init__(self, model: LifeGameModel):
        super(LifeGameController, self).__init__()
        self.model = model

    def on_cell_clicked(self, row: int, col: int):
        """
        Changes state of given (row, col) cell.
        :param row:
        :param col:
        :return:
        """
        new_state = 1 if self.model.cells[row, col] == 0 else 0
        self.model.changeCellStatus(row, col, new_state)

    def on_grid_change_request(self, val: int):
        """
        Changes grid size to given index.
        :param val:
        :return:
        """
        if 0 <= val < len(self.model.grid_sizes):
            self.model.changeGridSize(val)

    def on_fps_change_request(self, val: float):
        """
        Changes fps based on given float value.
        :param val:
        :return:
        """
        self.model.changeFps(val)

    def on_conf_change_requested(self, i: int):
        """
        Changes environment putting a new configuration given by index.
        :param i:
        :return:
        """
        self.model.load_config(self.model.configurations[i])

    def save_configuration_requested(self):
        """
        Saves current environment cells.
        :return:
        """
        complete_path, _choice = QFileDialog.getSaveFileName(self, directory=self.model.data_path,
                                                             filter="{} files (*{})".format(self.model.config_ext[1:],
                                                                                            self.model.config_ext))
        if complete_path:
            self.model.save_config(complete_path)

    def step_requested(self):
        """
        Steps forward in evolution.
        :return:
        """
        self.model.step_life()

    def stop_requested(self):
        """
        Stops the evolution to current state.
        :return:
        """
        self.model.stop()

    def play_pause_requested(self):
        """
        Plays or pauses according to current state.
        :return:
        """
        if not self.model.is_playing:
            self.model.start()
        else:
            self.model.pause()

    def clearRequested(self):
        """
        Clears the environment putting all cells to dead.
        :return:
        """
        self.model.load_config('blank')
        self.onBlankConfigRequested.emit()
