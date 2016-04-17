#!/usr/bin/env python

#from ctypes import cdll
#
#def move_mouse(x,y):
#    dll = cdll.LoadLibrary('libX11.so')
#    d = dll.XOpenDisplay(None)
#    root = dll.XDefaultRootWindow(d)
#    dll.XWarpPointer(d,None,root,0,0,0,0,x,y)
#    dll.XCloseDisplay(d)

from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


mouse = PyMouse()
keyboard = PyKeyboard()

class Click(object):

    def __init__(self, x, y):
        self.x, self.y = (x, y)

    def eval(self):
        mouse.click(self.x, self.y)

class DoubleClick(object):

    def __init__(self, x, y):
        self.x, self.y = (x, y)

    def eval(self):
        mouse.click(self.x, self.y, 1, 2)


class MouseSelect(object):

    def __init__(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2

    def eval(self):
        mouse.press(*self.coord1)
        mouse.release(*self.coord2)

class Move(object):

    def __init__(self, x, y):
        self.x, self.y = (x, y)

    def eval(self):
        mouse.move(self.x, self.y)


class Type(object):

    def __init__(self, msg):
        self.msg = msg

    def eval(self):
        keyboard.type_string(self.msg)

class SelectAll(object):

    def eval(args):
        keyboard.press_key(keyboard.control_key)
        keyboard.tap_key('a')
        keyboard.release_key(keyboard.control_key)
        

class Copy(object):

    def eval(args):
        keyboard.press_key(keyboard.control_key)
        keyboard.tap_key('c')
        keyboard.release_key(keyboard.control_key)
 

class GetCl(object):

    def eval(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        return clipboard.wait_for_text()


class Action(object):

    SLEEP = 2

    def __init__(self, controls):
        self.controls = controls

    def eval(self):
        outs = []
        for control in self.controls:
            out = control.eval()
            if out is not None:
                outs.append(out)
            sleep(self.SLEEP)

        if len(outs) == 1:
            return outs[0]
        if outs:
            return outs
        else:
            return None

            
        

        

def main():
#    from locations import W_COOR
#    from locations import MINES
#    action = Action([Move(*c) for c in MINES])

#    action = Action([Move(*W_COOR), SelectAll(), Copy(), GetCl()])
#    print(action.eval())
    s = MouseSelect((200, 200), (400, 400))
    s.eval()

if __name__ == '__main__':
    main()
