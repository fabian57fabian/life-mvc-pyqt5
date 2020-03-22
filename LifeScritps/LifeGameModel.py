import os
import numpy as np
import json
from PyQt5.QtCore import pyqtSignal, QObject
from LifeScritps.GameSettings import LifeSettings


class LifeGameModel(QObject):
    oncellStatusChanged = pyqtSignal(int, int, int)

    def __init__(self):
        super(LifeGameModel, self).__init__()
        self.data_path = "Configs"
        self.icon_path = "icons"
        self.settings_file = "settings.json"
        self.settings = self.load_settings(self.settings_file)
        self.icons_dataset = self.load_icons()
        self.config_ext = ".cells"
        self.configurations = self.load_configs(self.data_path)
        self.cells = np.zeros((self.settings.cells_h, self.settings.cells_w))

    def load_configs(self, confs_dir):
        confs = os.listdir(confs_dir)
        return [conf[:-len(self.config_ext)] for conf in confs if conf.endswith(self.config_ext)]

    def load_settings(self, filename, exit_if_error=False):
        if not os.path.exists(filename):
            sett = LifeSettings()
            with open(filename, 'w') as out_file:
                out_file.write(json.dumps(sett.__dict__))
        settings = LifeSettings()
        try:
            with open(filename, 'r') as in_file:
                sett_dict = json.load(in_file)
            settings.__dict__ = sett_dict
        except:
            if exit_if_error: exit(-1)
            print("Error loading settings file. Writing temporany settings file.")
            self.load_settings("settings_tmp.json", True)
        return settings

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

    def getsizes(self):
        return ["100x100", "200x200", "300x300", "400x400", "500x500"]

    def changeCellStatus(self, i, j):
        new_state = 1 if self.cells[i, j] == 0 else 0
        self.cells[i, j] = new_state
        self.oncellStatusChanged.emit(i, j, new_state)
