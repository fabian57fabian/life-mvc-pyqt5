import numpy as np
import os


class ConfigParser(object):
    def __init__(self):
        super(ConfigParser).__init__()
        self.comment_char = '!'
        self.alive_char = '.'
        self.dead_char = 'O'

    def read_file(self, filename):
        config = []
        max_width = 0
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if not line.startswith(self.comment_char) and line != "":
                    config.append([])
                    for symbol in line:
                        config[-1].append(1 if symbol == self.alive_char else 0)
                    max_width = len(config[-1]) if len(config[-1]) > max_width else max_width
        arr = np.zeros((len(config), max_width))
        for i in range(len(config)):
            for j in range(len(config[i])):
                arr[i, j] = config[i][j]
        return arr

    def write_file(self, filename, array):
        with open(filename, 'w') as file:
            file.write(self.comment_char + os.path.basename(filename) + "\n")
            for row in array:
                for el in row:
                    file.write(self.alive_char if el == 1 else self.dead_char)
                file.write("\n")
