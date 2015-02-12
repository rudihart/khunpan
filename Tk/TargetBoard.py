__author__ = 'Rudolf Hart'

import Tk.Board


class TargetBoard(Tk.Board):
    VERSION = '1.0.0'
    SIZE_FACTOR = 5
    DIVISION_SIZE = 0.25

    def scale_board(self):
        zoom = TargetBoard.SIZE_FACTOR * self.zoom
        self.scale('board', 0, 0, zoom/2, zoom/2)
        self.move(
            'all',
            (self.board.xmax + 1) * TargetBoard.DIVISION_SIZE * zoom,
            (self.board.ymax + 1) * TargetBoard.DIVISION_SIZE * zoom
        )

    def scale_piece(self, piece):

        self.scale(piece.name, 0, 0, self.zoom/2, self.zoom/2)
        self.move(
            piece.name,
            (self.board.xmax + 1) * TargetBoard.DIVISION_SIZE * self.zoom * TargetBoard.SIZE_FACTOR,
            (self.board.ymax + 1) * TargetBoard.DIVISION_SIZE * self.zoom * TargetBoard.SIZE_FACTOR
        )

    def add_sensors(self, piece):
        # no sensors in target board
        pass
