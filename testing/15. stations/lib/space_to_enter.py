from tkinter import *
class PressSpaceToEnter:
    def __init__(self, window: Tk, width: int, height: int):
        self.c = Canvas(window, width=300,height=40,bg='white')
        self.c.place(x= (width/2)-150, y = height-38)
        self.c.create_rectangle(3,3,299,295,outline='black', fill='')
        self.c.create_text(150,5,fill='black', font='Times 20', text='Press Space to enter', anchor='n')
        self.live = True
    
    def remove(self):
        self.c.destroy()
        self.live = False