from PyQt5 import QtWidgets
from LifeScritps.LifeGameView import LifeGameView
from LifeScritps.LifeGameModel import LifeGameModel
from LifeScritps.LifeGameController import LifeGameController

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # this is a mockup for data. next time save a configuration file
    model = LifeGameModel()
    model.load_data()
    controller = LifeGameController(model)
    ui = LifeGameView(model, controller)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
