__author__ = 'Rudolf Hart'


class Piece:
    VERSION = '1.0.0'

    def __init__(self, name, size_x, size_y, color):
        if size_x < 1 or size_y < 1:
            return
        self.name = name
        self.color = color
        self.sizex = size_x
        self.sizey = size_y
        self.sensors = []
        self.xpos = 0
        self.ypos = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_sensor(self, name):
        self.sensors.append(name)

    def get_sensors(self):
        return self.sensors

    def get_size(self):
        return self.sizex, self.sizey

    def get_color(self):
        return self.color

    def set_position(self, x, y):
        self.xpos = x
        self.ypos = y

    def get_position(self):
        return self.xpos, self.ypos
