from tkinter import *
from json import loads

class Station:
    def __init__(self, name: str, c: Canvas, map_name: str):
        with open(f'map/{map_name}/stations/{name}.json', 'r') as f:
            s = loads(f.read().strip('\n'))
        self.name = s['name']
        self.pos = s['position']
        self.exits = s['exits']
        self.object = c.create_oval(self.pos[0]-15, self.pos[1]-15, self.pos[0]+15,self.pos[1]+15,fill='white',outline='black')
        self.object_inner = c.create_oval(self.pos[0]-5, self.pos[1]-5, self.pos[0]+5,self.pos[1]+5,fill='white',outline='#333333')
        self.texts = []
        for text in s['map_text']:
            self.texts.append(c.create_text(self.pos[0] + text['offset'][0], self.pos[1] + text['offset'][1], fill='black', font=text['font'], text=text['text'], anchor=text['anchor']))

    def unload(self, c: Canvas):
        c.delete(self.object)
        c.delete(self.object_inner)
        for i in range(len(self.texts)-1, -1, -1):
            c.delete(self.texts[i])