__author__ = 'Rudolf Hart'


class Board:
    VERSION = '1.0.0'
    MAP_FREE_MARKER = '00'

    def __init__(self):
        self.xmax = 0
        self.ymax = 0
        self.map = []
        self.pieces = {}

    def reset(self, x_max, y_max):
        self.xmax = x_max
        self.ymax = y_max
        self.map = []
        self.pieces = {}
        for x in range(0, x_max):
            for y in range(0, y_max):
                self.map[x][y] = Board.MAP_FREE_MARKER

    def board_set(self, piece, xpos, ypos):
        (szx, szy) = piece.get_size()

        # check if free
        for x in range(1, szx):
            for y in range(1, szy):
                if self.map[xpos + x - 1][ypos + y - 1] != Board.MAP_FREE_MARKER:
                    return
        # set piece
        for x in range(1, szx):
            for y in range(1, szy):
                self.map[xpos + x - 1][ypos + y - 1] = "%d%d" % (szx, szy)

        piece.set_position(xpos, ypos)
        self.pieces[piece.get_name()] = piece
        return piece

    def move(self, piece, direction):
        if direction == 'e':
            return self.move_right(piece)
        if direction == 'w':
            return self.move_left(piece)
        if direction == 'n':
            return self.move_up(piece)
        if direction == 's':
            return self.move_down(piece)

    def move_right(self, piece):
        (dx, dy) = (1, 0)
        (szx, szy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        if xpos + szx - 1 + dx > self.xmax:
            return
        for y in range(1, szy):
            if self.map[xpos + szx - 1 + dx][ypos + y - 1] != Board.MAP_FREE_MARKER:
                return
        for y in range(1, szy):
            self.map[xpos + szx - 1 + dx][ypos + y - 1] = "%d%d" % (szx, szy)
            self.map[xpos][ypos + y - 1] = Board.MAP_FREE_MARKER

        piece.set_position(xpos + dx, ypos + dy)
        return dx, dy

    def move_left(self, piece):
        (dx, dy) = (-1, 0)
        (szx, szy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        if xpos + dx < 0:
            return
        for y in range(1, szy):
            if self.map[xpos + dx][ypos + y - 1] != Board.MAP_FREE_MARKER:
                return
        for y in range(1, szy):
            self.map[xpos + dx][ypos + y - 1] = "%d%d" % (szx, szy)
            self.map[xpos + szx - 1][ypos + y - 1] = Board.MAP_FREE_MARKER

        piece.set_position(xpos + dx, ypos + dy)
        return dx, dy

    def move_up(self, piece):
        (dx, dy) = (0, -1)
        (szx, szy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        if ypos + dy < 0:
            return
        for x in range(1, szx):
            if self.map[xpos + x - 1][ypos + dy] != Board.MAP_FREE_MARKER:
                return
        for x in range(1, szx):
            self.map[xpos + x - 1][ypos + dy] = "%d%d" % (szx, szy)
            self.map[xpos + x - 1][ypos + szy - 1] = Board.MAP_FREE_MARKER
        piece.set_position(xpos + dx, ypos + dy)
        return dx, dy

    def move_down(self, piece):
        (dx, dy) = (0, 1)
        (szx, szy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        if ypos + szy - 1 + dy > self.ymax:
            return
        for x in range(1, szx):
            if self.map[xpos + x - 1][ypos + szy - 1 + dy] != Board.MAP_FREE_MARKER:
                return
        for x in range(1, szx):
            self.map[xpos + x - 1][ypos + szy - 1 + dy] = "%d%d" % (szx, szy)
            self.map[xpos + x - 1][ypos] = Board.MAP_FREE_MARKER
        piece.set_position(xpos + dx, ypos + dy)
        return dx, dy

    def check_solution(self, target):
        for x in range(0, self.xmax):
            for y in range(0, self.ymax):
                if self.map[x][y] != target.map[x][y]:
                    return 0
        return 1

