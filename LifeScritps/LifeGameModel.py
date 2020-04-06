import os
import numpy as np
import json
from PyQt5.QtCore import pyqtSignal, QObject
from GameSettings import LifeSettings
from GameTimer import Evolutioner
from ConfigParser import ConfigParser


class LifeGameModel(QObject):
    oncellStatusChanged = pyqtSignal(int, int, int)
    onFpsChanged = pyqtSignal(int)
    onStepChanged = pyqtSignal(int)
    onPlayStateChanged = pyqtSignal(bool)
    onSizeChanged = pyqtSignal(int, int, np.ndarray)

    def __init__(self):
        super(LifeGameModel, self).__init__()
        self.data_path = "Configs"
        self.parser = ConfigParser()
        self.icon_path = "icons"
        self.settings_file = "settings.json"
        self.grid_sizes = [[20, 10], [40, 20], [60, 30], [80, 40]]
        self.current_settings = self.load_settings(self.settings_file)
        self.rows, self.cols = self.current_settings.cells_h, self.current_settings.cells_w
        if not self.isSizeAccepted():
            self.cols = self.grid_sizes[0][0]
            self.rows = self.grid_sizes[0][1]
        self.fps = self.current_settings.current_fps
        self.icons_dataset = self.load_icons()
        self.config_ext = ".cells"
        self.configurations = self.load_configs(self.data_path)
        self.cells = self.build_cells()
        self.step = 0
        self.evolutioner = Evolutioner()
        self.onFpsChanged.connect(self.evolutioner.set_fps)
        self.evolutioner.onStepTrieggered.connect(self.step_life)
        self.is_playing = False
        self.last_step_ts = -1
        self.base_config = self.cells.copy()

    def isSizeAccepted(self):
        for w, h in self.grid_sizes:
            if w == self.cols and h == self.rows:
                return True
        return False

    def build_cells(self):
        return np.zeros((self.rows, self.cols))

    def setPlaystate(self, playing: bool):
        self.is_playing = playing
        self.onPlayStateChanged.emit(playing)

    def load_configs(self, confs_dir):
        confs = os.listdir(confs_dir)
        return [conf[:-len(self.config_ext)] for conf in confs if conf.endswith(self.config_ext)]

    def put_data_in_grid(self, data, noemit=False):
        start_i, start_j = int(self.rows / 2) - int(data.shape[0] / 2), int(self.cols / 2) - int(data.shape[1] / 2)
        # if start_i >= 0 and start_j >= 0:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                r, c = start_i + i, start_j + j
                if 0 <= r <= self.rows - 1 and 0 <= c <= self.cols - 1:
                    if noemit:
                        self.cells[r,c] = int(data[i, j])
                    else:
                        self.changeCellStatus(r, c, int(data[i, j]))

    def load_config(self, conf):
        if conf in self.configurations:
            data = self.parser.read_file(os.path.join(self.data_path, conf + self.config_ext))
            self.resetCells()
            self.put_data_in_grid(data)

    def save_config(self, complete_path: str):
        if not complete_path.endswith(self.config_ext):
            complete_path += self.config_ext
        self.parser.write_file(complete_path, self.cells)

    def resetCells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.changeCellStatus(i, j, 0)

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
        icons_dts['play'] = "Play.png"
        icons_dts['pause'] = "Pause.png"
        icons_dts['step'] = "End.png"
        icons_dts['stop'] = "Stop.png"
        icons_dts['clear'] = "clear-button.png"
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

    def changeCellStatus(self, i, j, new_state):
        if self.cells[i, j] != new_state:
            self.cells[i, j] = new_state
            self.oncellStatusChanged.emit(i, j, new_state)

    def step_life(self):
        """
        Stepping one generation
        :return:
        """
        tmp_cells = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.cells[i, j]
                new_state = self.check_step_cell(i, j)
                tmp_cells[i, j] = new_state if new_state != val else 6
        for i in range(self.rows):
            for j in range(self.cols):
                if tmp_cells[i, j] != 6:
                    self.changeCellStatus(i, j, tmp_cells[i, j])
        self.setStep(self.step + 1)

    def check_step_cell(self, i, j):
        """
            Executes a step on a given cell and returns next state
        :param i: row
        :param j: column
        :return:
        """
        if i == 1 and j == 1:
            a = 4
        mat = self.cells[max(0, i - 1): min(self.rows - 1, i + 2), max(0, j - 1):min(self.cols - 1, j + 2)]
        s = np.sum(mat, dtype=np.int32) - self.cells[i, j]
        if s <= 1:
            return 0  # loneliness
        elif s >= 4:
            return 0  # overpopulation
        else:
            if self.cells[i, j] == 1:
                return 1  # Survives
            else:
                return 1 if s == 3 else 0

    def changeFps(self, framerate: float):
        self.fps = framerate
        self.onFpsChanged.emit(framerate)

    def changeGridSize(self, value):
        data_backup = np.copy(self.cells)
        self.cols = self.grid_sizes[value][0]
        self.rows = self.grid_sizes[value][1]
        self.cells = self.build_cells()
        self.put_data_in_grid(data_backup, noemit=True)
        self.onSizeChanged.emit(self.rows, self.cols, self.cells)

    def setStep(self, new_step: int):
        self.step = new_step
        self.onStepChanged.emit(new_step)

    def stop(self):
        self.evolutioner.stop()
        self.setStep(0)
        self.resetCells()
        self.put_data_in_grid(self.base_config)
        self.setPlaystate(False)

    def start(self):
        self.base_config = self.cells.copy()
        self.evolutioner.start()
        self.setPlaystate(True)

    def pause(self):
        self.evolutioner.stop()
        self.setPlaystate(False)
