from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout, QGridLayout, QLayout
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
        self.model.onSizeChanged.connect(self.setGridSize)

    def setGridSize(self, rows, cols):
        self.all_cells = []
        self.clearLayout(self.lay)
        # for i in range(self.lay.count()): self.lay.itemAt(i).widget().close()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        for i in range(rows):
            self.all_cells.append([])
            for j in range(cols):
                cell = LifeCell(self, i, j)
                cell.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
                cell.cell_clicked.connect(self.controller.on_cell_clicked)
                self.all_cells[-1].append(cell)
                self.lay.addWidget(cell, i, j)
        self.setLayout(self.lay)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def setupUi(self):
        self.setMinimumSize(640, 480)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(173, 127, 168);")
        self.setGridSize(self.model.rows, self.model.cols)
        # QtCore.QMetaObject.connectSlotsByName(self)

    def cell_changed(self, i, j, new_state):
        self.all_cells[i][j].setState(new_state)
