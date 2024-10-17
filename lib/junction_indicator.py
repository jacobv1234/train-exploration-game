# line that appears to show where a junction choice will take you
# created alongside junction_choice
from tkinter import *
from lib.helper import short_line_coord_generator

class Junction_Indicator:
    def __init__(self, junction, canvas: Canvas):
        self.x, self.y = tuple(junction['coords'])
        self.dir = junction[junction['approach']['options'][junction['approach']['default']]]['direction']
        coords = short_line_coord_generator(self.x, self.y, self.dir)
        self.object = canvas.create_polygon(coords, fill='white', outline='white')
        self.canvas = canvas
    
    def update(self, new_dir: int):
        self.dir = new_dir
        coords = short_line_coord_generator(self.x, self.y, self.dir)
        self.canvas.delete(self.object)
        self.object = self.canvas.create_polygon(coords, fill='white', outline='white')

    def remove(self):
        self.canvas.delete(self.object)