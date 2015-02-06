__author__ = 'Rudolf Hart'

import Tkinter


class Board(Tkinter.Canvas):
    VERSION = '1.0.0'

    SIZE_FACTOR = 5
    BOARD_WIDTH = 4
    BOARD_HEIGHT = 5
    DOT_RADIUS = 0.2

    def __init__(self, parent, **args):
        Tkinter.Canvas.__init__(self, parent, **args)
        self.zoom = args['-zoom']
        self.board = args['-board']
        self.game = args['-game']
        self.height = Board.BOARD_HEIGHT * Board.SIZE_FACTOR * self.zoom
        self.width = Board.BOARD_WIDTH * Board.SIZE_FACTOR * self.zoom

        self.draw_board()

    def scale_board(self):
        pass

    def scale_piece(self, piece):
        pass

    def add_sensors(self, piece):
        pass

    def draw_board(self):
        board = self.board
        for x in range(0, board.xmax):
            self.addtag('board', 'withtag', self.create_line(x, 0, x, board.ymax + 1))
        for y in range(0, board.ymax):
            self.addtag('board', 'withtag', self.create_line(0, y, board.xmax + 1, y))
        self.addtag('board', 'withtag', self.create_rectangle(0, 0, board.xmax + 1, board.ymax + 1))
        self.scale_board()
        for piece in board.pieces.values():
            self.draw_piece(piece)

    def draw_piece(self, piece):
        (sx, sy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        piececolor = '#cb8'
        name = self.create_rectangle(
            xpos * Board.SIZE_FACTOR,
            ypos * Board.SIZE_FACTOR,
            (xpos + sx) * Board.SIZE_FACTOR,
            (ypos + sy) * Board.SIZE_FACTOR,
            fill=piececolor
        )
        self.addtag(piece.name, 'withtag', name)
        self.addtag(
            piece.name,
            'withtag',
            self.create_oval(
                (xpos + sx / 2 - Board.DOT_RADIUS) * Board.SIZE_FACTOR,
                (ypos + sy / 2 + Board.DOT_RADIUS) * Board.SIZE_FACTOR,
                (xpos + sx / 2 + Board.DOT_RADIUS) * Board.SIZE_FACTOR,
                (ypos + sy / 2 - Board.DOT_RADIUS) * Board.SIZE_FACTOR,
                fill=piece.get_color()
            ))
        self.scale_piece(piece)
        piece.set_id(piece.name)
        self.add_sensors(piece)
