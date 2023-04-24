from tkinter import *

class SpeedTracker:
    def __init__(self,window,width,height):
        self.canvas = Canvas(window, width=80,height=240,bg='white')
        self.canvas.place(x=width-79,y=(height//2)-120)
        self.canvas.create_rectangle(2,2,81,241,outline='black')

        # icons
        self.canvas.create_polygon(41,111,61,131,21,131, fill='yellow', outline='black')
        self.canvas.create_polygon(41,26,61,46,51,46,61,56,21,56,31,46,21,46, fill='green', outline='black')
        self.canvas.create_rectangle(26,190,56,197,fill='red',outline='black')
        self.canvas.create_rectangle(26,210,56,203,fill='red',outline='black')

        self.pointer = self.canvas.create_polygon(13,163,70,163,80,173,80,230,70,240,13,240,3,230,3,173, outline='black', fill='')
        self.x = 200
    
    def update(self, destination):
        if destination > self.x:
            self.canvas.move(self.pointer,0,16)
            self.x += 16
        elif destination < self.x:
            self.canvas.move(self.pointer,0,-16)
            self.x -= 16