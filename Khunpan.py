__author__ = 'Rudolf Hart'

import os
import re
import string

from Tkinter import *
import tkMessageBox
import tkFileDialog
import Game


class Khunpan(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        master.title("Khun Pan")
        self.menubar = Menu(self)

        self.gamemenu = Menu(self.menubar, tearoff=0)

        self.gamemenu.add_command(label="New", command=self.game_new)
        self.gamemenu.add_separator()
        self.gamemenu.add_command(label="Reset", command=self.game_reset)
        self.gamemenu.add_separator()
        self.gamemenu.add_command(label="Quit", command=self.game_quit)

        self.menubar.add_cascade(label="Game", menu=self.gamemenu)

        self.replaymenu = Menu(self.menubar, tearoff=0)

        self.replaymenu.add_command(label="Play", command=self.replay_play)
        self.replaymenu.add_separator()
        self.replaymenu.add_command(label="Load", command=self.replay_load)
        self.replaymenu.add_command(label="Save", command=self.replay_save)

        self.menubar.add_cascade(label="Replay", menu=self.replaymenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.helpmenu.add_command(label="Quick", command=self.help_quick)
        self.helpmenu.add_command(label="Contents", command=self.help_contents)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About", command=self.help_about)

        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.add_toolbar()
        self.init_config()
        self.game_new()

    def init_config(self):
        self.config = {"zoom": 20}

    def get_config(self, key):
        return self.config[key]

    def add_toolbar(self):
        game = StringVar()
        gamedir = os.path.dirname(__file__) + '/games'
        self.toolbar = Frame(self)
        self.toolbar.games = OptionMenu(self.toolbar, game, _game_list())

        self.toolbar.games.pack({"side": 'left'})
        load_button = Button(text='Load Game',
                             command=lambda g=game: self.Khunpan.game_load(g))
        load_button.pack({"side": 'left'})
        self.toolbar.pack({"side": 'top', "fill": 'x'})

    def init_boards(self):

        if self.boards:
            self.boards.destroy()

        self.boards = Frame(self)
        self.boards.pack({"side": 'bottom', "fill": 'both'})
        board = self.game.get_board()
        target = self.game.get_target()

        pb = self.boards.PlayBoard(board, self.game, self.get_config('zoom'))

        pb.pack({"side": 'left'})
        lab = Label(self.boards, text='  :  ', background='white')
        lab.pack({"side": 'left', "fill": 'y'})
        tb = self.boards.TargetBoard(target, self.game, self.get_config('zoom'))
        tb.pack({"side": 'left'})

    ### Callbacks ###

    ## Game ##

    def game_new(self):
        self.game = Game.Game()
        self.game.load()
        self.init_boards()

    def game_load(self, game):
        if game:
            filename = os.path.dirname(__file__) + "/games/game.game"
        else:
            filename = tkFileDialog.askopenfilename({
                "initialdir": os.path.dirname(__file__) + '/games',
                "defaultextension": '.game',
                "filetypes": [("Games", '.game')],
                "initialfile": '00-ling.game'
            })

            if not filename:
                return

        self.game = Game(filename)
        self.game.load()
        self.init_boards()

    def game_save(self):
        filename = tkFileDialog.asksaveasfilename({
            "initialdir": os.path.dirname(__file__) + '/games',
            "defaultextension": '.game',
            "filetypes": [("Games", '.game')],
        })

        if not filename:
            return
        self.game.save(filename)

    def game_reset(self):
        self.game.load()
        self.init_boards()
        self.game.clear_history()
        return

    def game_quit(self):
        os.exit(0)

    ## Replay ##

    def replay_play(self):
        REPLAY_STEP_TIME = 100

        self.game.load()
        self.init_boards()
        self.game.rewind()

        self.after(REPLAY_STEP_TIME, lambda g=self.game: self.tkboard.replay_move(g))

    def replay_load(self):
        filename = tkFileDialog.askopenfilename({
            "initialdir": os.path.dirname(__file__) + '/histories',
            "defaultextension": '.sol',
            "filetypes": [("Solutions", '.sol'), ("Game History", '.hist')],
        })
        if not filename:
            return
        if self.game.load_history(filename) != 0:
            tkMessageBox.showerror("No Game Loaded", 'History requires game '
                                   + os.path.basename(filename)
                                   + ".\n\n"
                                   + '                  NOT LOADED!'
            )

    def replay_save(self):
        filename = tkFileDialog.asksaveasfilename({
            "initialdir": os.path.dirname(__file__) + '/histories',
            "defaultextension": '.hist',
            "filetypes": [("Game History", '.hist')],
        })
        if not filename:
            return
        self.game.save_history(filename)

    ## Help ##

    def help_quick(self):
        help = """

  Move the red piece (Khun Pan) into the position indicated at the right.
  To move a piece click on it near the free area.

  You will get a message about success if you move all the pieces to the
  position indicated on the right.

"""
        tkMessageBox.showinfo("Khunpan Quick Help", help)

    def help_contents(self):
        tkMessageBox.showerror("Programmer Laziness Error", "Not yet implemented")

    def help_about(self):
        about = """
            Khun Pan VREL_VERSION
           Copyright 2004 Rudolf Hart

   If you have problems and understand German
  you might have a look at http://www.khunpan.de/

"""
        tkMessageBox.showinfo("About Khunpan", about)


def _game_list():
    gamedir = os.path.dirname(__file__) + '/games'
    contents = os.listdir(gamedir)
    contents.sort()
    games = []
    regex = re.compile(".*\.game")
    for fname in contents:
        if regex.match(fname):
            games.append(string.replace(fname, ".game", ""))
    return games

