from PyQt5 import QtWidgets
from LifeScritps.LifeGameView import LifeGameView
from LifeScritps.LifeGameModel import LifeGameModel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # this is a mockup for data. next time save a configuration file
    model = LifeGameModel()
    ui = LifeGameView(model)
    ui.setupUi(MainWindow)
    model.load_data()
    MainWindow.show()
    sys.exit(app.exec_())
