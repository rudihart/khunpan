#!python
__author__ = 'Rudolf Hart'

from Tkinter import *
from Khunpan import Khunpan

root = Tk()
khunpan = Khunpan(master=root)
khunpan.mainloop()
root.destroy()
