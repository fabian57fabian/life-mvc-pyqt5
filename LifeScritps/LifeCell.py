from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout, QGridLayout


class LifeCell(QWidget):
    cell_clicked = pyqtSignal(int, int)

    def __init__(self, parent: QWidget, i: int, j: int):
        super(LifeCell, self).__init__(parent)
        self.parent = parent
        self.frame = QFrame(self)
        self.current_state = -1
        self.row = i
        self.column = j
        self.setupUi()

    def setupUi(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(0.9)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setState(0)

    def setState(self, state):
        if self.current_state != state:
            self.current_state = state
            if self.current_state == 0:
                self.setStyleSheet("background-color: rgb(255, 255, 255);")  # border:0.5px solid rgb(0, 0, 0);")
            elif self.current_state == 1:
                self.setStyleSheet("background-color: rgb(19, 214, 39);")  # border:0.5px solid rgb(0, 0, 0);")
            else:
                pass

    def getState(self):
        return self.current_state

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.cell_clicked.emit(self.row, self.column)
