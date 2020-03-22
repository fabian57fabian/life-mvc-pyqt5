from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout, QGridLayout
from LifeScritps.LifeCell import LifeCell
from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGameController import LifeGameController


class LifeGridWidget(QWidget):
    def __init__(self, parent: QWidget, model: LifeGameModel, controller: LifeGameController):
        super(LifeGridWidget, self).__init__(parent)
        self.parent = parent
        self.model = model
        self.controller = controller
        self.lay = QGridLayout()
        self.all_cells = []
        self.setupUi()
        self.model.oncellStatusChanged.connect(self.cell_changed)

    def setupUi(self):
        self.setMinimumSize(640, 480)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(173, 127, 168);")
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        for i in range(self.model.rows):
            self.all_cells.append([])
            for j in range(self.model.cols):
                cell = LifeCell(self, i, j)
                cell.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
                cell.cell_clicked.connect(self.controller.on_cell_clicked)
                self.all_cells[-1].append(cell)
                self.lay.addWidget(cell, i, j)
        self.setLayout(self.lay)
        QtCore.QMetaObject.connectSlotsByName(self)

    def cell_changed(self, i, j, new_state):
        self.all_cells[i][j].setState(new_state)
