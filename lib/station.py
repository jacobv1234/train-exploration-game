from tkinter import *
from json import loads
from random import randint, choice
from lib.helper import test_requirements

class Station:
    def __init__(self, name: str, c: Canvas, map_name: str, unlocked_lines: list):
        with open(f'map/{map_name}/stations/{name}.json', 'r') as f:
            s = loads(f.read().strip('\n'))
        self.name = s['name']
        self.pos = s['position']
        exits = s['exits']
        self.exits = {}

        for exit in list(exits.keys()):
            if str(type(exits[exit])) == '<class \'int\'>':
                self.exits[exit] = exits[exit]
            else:
                if test_requirements(exits[exit]['requirements'], unlocked_lines):
                    self.exits[exit] = [exits[exit]['direction']]
                    if 'line' in list(exit.keys()):
                        self.exits[exit].append(exits[exit['line']])

        self.shop = s['shop']
        self.col = 'white'
        if self.shop:
            self.col='red'
        self.object = c.create_oval(self.pos[0]-15, self.pos[1]-15, self.pos[0]+15,self.pos[1]+15,fill=self.col,outline='black')
        self.object_inner = c.create_oval(self.pos[0]-5, self.pos[1]-5, self.pos[0]+5,self.pos[1]+5,fill='white',outline='#333333')
        self.texts = []
        self.passenger_rules = s['passengers']
        for text in s['map_text']:
            self.texts.append(c.create_text(self.pos[0] + text['offset'][0], self.pos[1] + text['offset'][1], fill='black', font=text['font'], text=text['text'], anchor=text['anchor']))



    def unload(self, c: Canvas):
        c.delete(self.object)
        c.delete(self.object_inner)
        for i in range(len(self.texts)-1, -1, -1):
            c.delete(self.texts[i])
    
    def generate_passenger(self, unlocked):
        p = self.passenger_rules
        if randint(1,100) <= p['chance_of_any']:
            dest_choice = []
            for i in range(len(p['options'])):
                if p['options'][i]['line'] in unlocked:
                    chance = p['options'][i]['chance']
                    for j in range(chance):
                        dest_choice.append(i)
            
            decision = choice(dest_choice)
            return p['options'][decision]
        return 0