__author__ = 'Rudolf Hart'

import string
import os
import Utils
import Board
import Piece


class Game:
    VERSION = '1.0.0'
    GAME_LINE_SIZE = 6

    def __init__(self, filename=None):
        self.history = []
        self.hcnt = 0
        self.board = Board.Board()
        self.btarget = Board.Board()
        if filename is not None:
            self.filename = filename

    def get_board(self):
        return self.board

    def get_target(self):
        return self.btarget

    def get_history(self):
        return self.history

    def add_move(self, piecename, direction):
        self.history.append({'name': piecename, 'direction': direction})

    def rewind(self):
        self.hcnt = 0

    def clear_history(self):
        self.hcnt = 0
        self.history = []

    def play_move(self):
        rv = self.history[self.hcnt]
        self.hcnt += 1
        return rv

    def load(self):
        game_description = ()

        if self.filename is not None:
            try:
                game = open(self.filename, "r")
                game_description = game.readlines()
                game.close()
            except IOError:
                pass
        else:
            game_description = (
                '#khunpan.pl',
                '3,4',
                'V1,1,2,blue,0,0',
                'D1,2,2,red,1,0',
                'V2,1,2,blue,3,0',
                'H1,2,1,blue,1,2',
                'V3,1,2,blue,0,3',
                'S1,1,1,yellow,1,3',
                'S2,1,1,yellow,2,3',
                'S3,1,1,yellow,1,4',
                'S4,1,1,yellow,2,4',
                'V4,1,2,blue,3,3',
                'END',
                'V1,1,2,blue,0,0',
                'V2,1,2,blue,1,0',
                'V3,1,2,blue,2,0',
                'V4,1,2,blue,3,0',
                'S1,1,1,yellow,0,2',
                'S2,1,1,yellow,1,2',
                'H1,2,1,blue,2,2',
                'D1,2,2,red,1,3',
                'S3,1,1,yellow,3,3',
                'S4,1,1,yellow,3,4',
                'END',
            )
            self.filename = '00-ling.game'

        line = game_description.pop(0)
        if line is None:
            raise Utils.KhunpanError('No valid khunpan.pl game description')

        line = game_description.pop(0)
        (x_size, y_size) = string.split(line, ',', 2)

        self.board.reset(x_size, y_size)
        self.btarget.reset(x_size, y_size)

        for line in game_description:
            if line == 'END':
                break
            (name, szx, szy, color, xpos, ypos) = string.split(line, ',', Game.GAME_LINE_SIZE)
            piece = Piece.Piece(name, szx, szy, color)
            self.board.board_set(piece, xpos, ypos)

        for line in game_description:
            if line == 'END':
                break
            (name, szx, szy, color, xpos, ypos) = string.split(line, ',', Game.GAME_LINE_SIZE)
            piece = Piece.Piece(name, szx, szy, color)
            self.btarget.board_set(piece, xpos, ypos)

    def save(self, filename):
        try:
            out = open(filename, "w")
            out.write("%d,%d" % (self.board.xmax, self.board.ymax))
            print_state(out, self.board.pieces)
            print_state(out, self.btarget.pieces)
            out.close()
        except:
            raise Utils.KhunpanError("save %s failed" % filename)

    def save_history(self, filename):
        try:
            out = open(filename, "w")
            out.write("%s\n" % self.filename)
            for move in self.history:
                out.write("%s:%s\n" % (move.name, move.direction))
            out.close()
        except:
            raise Utils.KhunpanError("save history %s failed" % filename)

    def load_history(self, filename):
        self.history = []
        try:
            fhist = open(filename, "r")
            lines = fhist.readlines()
            fhist.close()
        except:
            raise Utils.KhunpanError("read history %s failed" % filename)
        line = lines.pop(0)
        if line != os.path.basename(self.filename):
            print 'History does not match game'
            return
        for line in lines:
            line = line.strip()
            (name, direction) = string.split(line, ':', 2)
            self.history.append({'name': name, 'direction': direction})


def print_state(dest, pieces):
    for piece in pieces.values():
        (sx, sy) = piece.get_size()
        (px, py) = piece.get_position()
        dest.write("%s,%d,%d,%s,%d,%d\n" %
                   (piece.get_name(), sx, sy, piece.get_color(), px, py))
        dest.write("END\n")

