from tkinter import *

class MapNameDisplay:
    def __init__(self, text, size, window, height):
        self.canvas = Canvas(window, width = 300, height = size + 24, bg='white')
        self.canvas.place(x=0, y=height - size - 24)
        self.canvas.create_text(150,8, fill='black', font=f'Arial {size}', text=text, anchor='n')

    def remove(self):
        self.canvas.destroy()