import os
from PyQt5.QtCore import pyqtSignal, QObject


class LifeGameModel(QObject):
    onSomethingHappened = pyqtSignal(list)

    def __init__(self):
        super(LifeGameModel, self).__init__()
        self.data_path = "Data"
        self.icon_path = "icons"
        self.icons_dataset = self.load_icons()

    def load_icons(self):
        icons_dts = {}
        icons_dts['play'] = "Media-Controls-Play-icon.png"
        icons_dts['pause'] = "Media-Controls-Pause-icon.png"
        icons_dts['stop'] = "Media-Controls-Stop-icon.png"
        icons_dts['open'] = "Folder-Open-icon.png"
        icons_dts['save'] = "Save-icon.png"
        return icons_dts

    def load_data(self):
        pass

    def getIconPath(self, icon_name):
        if icon_name in self.icons_dataset.keys():
            path = os.path.join(self.icon_path, self.icons_dataset[icon_name])
        else:
            path = os.path.join(self.icon_path, "Error-Delete-Icon.png")
        return path
