from functools import partial
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout, QGridLayout, QLayout
from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGameController import LifeGameController
import time


class LifeGridWidget(QWidget):
    def __init__(self, parent: QWidget, model: LifeGameModel, controller: LifeGameController):
        super(LifeGridWidget, self).__init__(parent)
        self.parent = parent
        self.model = model
        self.controller = controller
        self.lay = QGridLayout()
        self.all_cells = []
        self.setupUi()
        self.initConnectors()

    def initConnectors(self):
        self.model.oncellStatusChanged.connect(self.cell_changed)
        self.model.onSizeChanged.connect(self.resizeGrid)

    def setupUi(self):
        """
        Initializes ui and grid.
        :return:
        """
        self.setMinimumSize(400, 200)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        self.initGrid(self.model.rows, self.model.cols)
        self.setLayout(self.lay)

    def initGrid(self, rows: int, cols: int, newData: np.ndarray = None):
        """
        Initializes grid with given rows, cols and current data (last param is DEPRECATED).
        :param rows:
        :param cols:
        :param newData:
        :return:
        """
        for i in range(rows):
            self.all_cells.append([])
            for j in range(cols):
                cell = QFrame(self)
                self.setupFrame(cell)
                cell.setSizePolicy(
                    QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
                cell.mousePressEvent = partial(self.cell_clicked, (i, j))
                self.all_cells[-1].append(cell)
                self.lay.addWidget(cell, i, j)

    def cell_clicked(self, _coords, _event):
        """
        Slot connected to QFrame cell clicked with given coordinates.
        :param _coords:
        :param _event:
        :return:
        """
        self.controller.on_cell_clicked(_coords[0], _coords[1])

    def clearLayout(self):
        """
        Clears current layout freeing all cells.
        :return:
        """
        self.all_cells.clear()
        self.all_cells = []
        for i in reversed(range(self.lay.count())):
            self.lay.itemAt(i).widget().setParent(None)

    @pyqtSlot(int, int, np.ndarray)
    def resizeGrid(self, rows, cols, newData):
        self.clearLayout()
        self.initGrid(rows, cols, newData)

    def setupFrame(self, frame):
        """
        Initializes frame with ui positioning.
        :param frame:
        :return:
        """
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(0.9)
        frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        frame.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    @pyqtSlot(int, int, int)
    def cell_changed(self, i, j, new_state):
        self.all_cells[i][j].setStyleSheet(
            "background-color: rgb(255, 255, 255);" if new_state == 0 else "background-color: rgb(19, 214, 39);")
