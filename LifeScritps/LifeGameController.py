from PyQt5.QtCore import pyqtSignal, QObject
from LifeScritps.LifeGameModel import LifeGameModel
import numpy as np
from GameTimer import Evolutioner


class LifeGameController(object):
    onSomethingHappened = pyqtSignal(list)

    def __init__(self, model: LifeGameModel):
        super(LifeGameController, self).__init__()
        self.model = model

    def on_cell_clicked(self, row, col):
        print("Cell %d, %d clicked!" % (row, col))
        new_state = 1 if self.model.cells[row, col] == 0 else 0
        self.model.changeCellStatus(row, col, new_state)

    def on_size_selected(self, selected_size):
        print("Grid size changed: %s!" % selected_size)
        pass

    def on_conf_changed(self, i):
        print("Configuration changed: %d!" % i)
        # TODO: check if blank selected or real configuration
        pass

    def step_requested(self):
        self.model.step_life()

    def stop_requested(self):
        self.model.stop()

    def play_pause_requested(self):
        if not self.model.is_playing:
            self.model.start()
        else:
            self.model.pause()
