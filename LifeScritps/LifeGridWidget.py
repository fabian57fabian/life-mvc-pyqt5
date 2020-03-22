from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QFormLayout, QFrame, QVBoxLayout, QGridLayout


class LifeGridWidget(QWidget):
    def __init__(self, parent=QWidget):
        super(LifeGridWidget, self).__init__(parent)
        self.parent = parent
        self.lay = QGridLayout()
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(100, 60)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(173, 127, 168);")

        self.setLayout(self.lay)
        QtCore.QMetaObject.connectSlotsByName(self)
