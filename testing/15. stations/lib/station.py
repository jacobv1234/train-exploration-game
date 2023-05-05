from tkinter import *
from json import loads

class Station:
    def __init__(self, name: str, c: Canvas):
        with open(f'map/stations/{name}.json', 'r') as f:
            s = loads(f.read().strip('\n'))
        self.name = s['name']
        self.pos = s['position']
        self.exits = s['exits']
        self.object = c.create_oval(self.pos[0]-15, self.pos[1]-15, self.pos[0]+15,self.pos[1]+15,fill='white',outline='black')