# contains helper functions

from tkinter import *

# returns the opposite direction
def opp_dir(dir):
    return (dir + 8) % 16

# check if a requirements meets the unlocked lines
def test_requirements(req, unlocked):
    return all([line in unlocked for line in req['unlocked']]) and not any([line in unlocked for line in req['not']])


# creates a popup message in the top right, with
# a title, message, and number of frames until removed
class Popup:
    def __init__(self, window: Tk, width: int, title: str, message: str, remove: int):
        self.c = Canvas(window, width=350, height=150, bg='white')
        self.c.place(x=width-350, y=0)
        self.c.create_rectangle(2,2,348,148, fill='white', outline='black')
        self.title = self.c.create_text(25, 30, fill='black', font='Arial 20', text=title, anchor='nw')
        self.message = self.c.create_text(25, 100,fill='black', font='Arial 16', text=message, anchor='nw', width=300)
        self.timeout = remove
    
    def countdown(self):
        self.timeout -= 1
        if self.timeout == 0:
            self.c.destroy()
        return self.timeout
