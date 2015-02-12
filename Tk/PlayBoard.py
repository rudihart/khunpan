__author__ = 'Rudolf Hart'

import Tk.Board
import tkMessageBox


class PlayBoard(Tk.Board):
    VERSION = '1.0.0'
    SIZE_FACTOR = 5
    OFFSET = 0.1
    REPLAY_TIME_STEP = 1000

    def scale_board(self):
        zoom = PlayBoard.SIZE_FACTOR * self.zoom
        self.scale('board', 0, 0, zoom, zoom)

    def scale_piece(self, piece):
        zoom = self.zoom
        self.scale(piece.name, 0, 0, zoom, zoom)

    def add_sensors(self, piece):
        (sx, sy) = piece.get_size()
        (xpos, ypos) = piece.get_position()
        piececolor = '#cb8'
        zoom = self.zoom

        idn = self.create_rectangle(
            xpos * PlayBoard.SIZE_FACTOR + 1,
            ypos * PlayBoard.SIZE_FACTOR + PlayBoard.OFFSET,
            (xpos + sx) * PlayBoard.SIZE_FACTOR - 1,
            ypos * PlayBoard.SIZE_FACTOR + 1,
            {"outline": piececolor, "fill": piececolor}
        )
        self.scale(idn, 0, 0, zoom, zoom)
        idn.bind('<Button-1>', lambda pc=piece: self.move_piece(pc, 'n'))
        piece.add_sensor(idn)

        ids = self.create_rectangle(
            xpos * PlayBoard.SIZE_FACTOR + 1,
            (ypos + sy) * PlayBoard.SIZE_FACTOR - 1,
            (xpos + sx) * PlayBoard.SIZE_FACTOR - 1,
            (ypos + sy) * PlayBoard.SIZE_FACTOR - PlayBoard.OFFSET,
            {"outline": piececolor, "fill": piececolor}
        )
        self.scale(ids, 0, 0, zoom, zoom)
        ids.bind('<Button-1>', lambda pc=piece: self.move_piece(pc, 's'))
        piece.add_sensor(ids)

        idw = self.createRectangle(
            xpos * PlayBoard.SIZE_FACTOR + PlayBoard.OFFSET,
            ypos * PlayBoard.SIZE_FACTOR + 1,
            xpos * PlayBoard.SIZE_FACTOR + 1,
            (ypos + sy) * PlayBoard.SIZE_FACTOR - 1,
            {"outline": piececolor, "fill": piececolor}
        )
        self.scale(idw, 0, 0, zoom, zoom)
        idw.bind('<Button-1>', lambda pc=piece: self.move_piece(pc, 'w'))
        piece.add_sensor(idw)

        ide = self.createRectangle(
            (xpos + sx) * PlayBoard.SIZE_FACTOR - 1,
            ypos * PlayBoard.SIZE_FACTOR + 1,
            (xpos + sx) * PlayBoard.SIZE_FACTOR - PlayBoard.OFFSET,
            (ypos + sy) * PlayBoard.SIZE_FACTOR - 1,
            {"outline": piececolor, "fill": piececolor}
        )
        self.scale(ide, 0, 0, zoom, zoom)
        ide.bind('<Button-1>', lambda pc=piece: self.move_piece(pc, 'e'))
        piece.add_sensor(ide)

    def move_piece(self, piece, direction, replay=None):
        zoom = self.zoom
        board = self.board

        delta = board.move(piece, direction)
        if not delta:
            return

        if not replay:
            self.game.add_move(piece.name, direction)

        dx = delta[0] * PlayBoard.SIZE_FACTOR * zoom
        dy = delta[1] * PlayBoard.SIZE_FACTOR * zoom
        self.move(piece.get_id(), dx, dy)
        for sensor in piece.get_sensors():
            self.move(sensor, dx, dy)
        if board.check_solution(self.game.get_target()):
            tkMessageBox.showinfo("Solved", " CONGRATULATIONS!!\n You found the solution.")

    def replay_move(self, game):
        board = self.board
        move = game.play_move()
        if move:
            self.move_piece(board.pieces.move.name, move.direction, 1)
            self.after(PlayBoard.REPLAY_TIME_STEP, lambda g=game: self.replay_move(g))
