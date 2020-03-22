from PyQt5.QtCore import pyqtSignal, QObject
from LifeScritps.LifeGameModel import LifeGameModel


class LifeGameController(object):
    onSomethingHappened = pyqtSignal(list)

    def __init__(self, model: LifeGameModel):
        super(LifeGameController, self).__init__()
        self.model = model

    def on_cell_clicked(self, row, col):
        print("Cell %d, %d clicked!" % (row, col))
        self.model.changeCellStatus(row, col)

    def on_size_selected(self, selected_size):
        print("Grid size changed: %s!" % selected_size)
        pass

    def on_conf_changed(self, i):
        print("Configuration changed: %d!" % i)
        # TODO: check if blank selected or real configuration
        pass
