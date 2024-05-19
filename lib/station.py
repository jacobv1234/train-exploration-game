from tkinter import *
from json import loads
from random import randint, choice
from lib.helper import test_requirements, get_badge

class Station:
    def __init__(self, name: str, c: Canvas, map_name: str, unlocked_lines: list):
        with open(f'map/{map_name}/stations/{name}.json', 'r') as f:
            s = loads(f.read().strip('\n'))
        self.name = s['name']
        self.pos = s['position']
        exits = s['exits']
        self.exits = {}
        self.map = map_name

        for exit in list(exits.keys()):
            if str(type(exits[exit])) == '<class \'int\'>':
                self.exits[exit] = exits[exit]
            else:
                if test_requirements(exits[exit]['requirements'], unlocked_lines):
                    self.exits[exit] = [exits[exit]['direction']]
                    if 'line' in list(exits[exit].keys()):
                        self.exits[exit].append(exits[exit]['line'])
                        if 'new_coords' in list(exits[exit].keys()):
                            self.exits[exit].extend(exits[exit]['new_coords'])
                            if 'new_map' in list(exits[exit].keys()):
                                self.exits[exit].append(exits[exit]['new_map'])

        self.shop = s['shop']
        self.col = 'white'
        if self.shop:
            self.col='lightgrey'
        self.object = c.create_oval(self.pos[0]-15, self.pos[1]-15, self.pos[0]+15,self.pos[1]+15,fill=self.col,outline='black')
        self.object_inner = c.create_oval(self.pos[0]-5, self.pos[1]-5, self.pos[0]+5,self.pos[1]+5,fill='white',outline='#333333')
        self.texts = []
        self.badges = []
        self.passenger_rules = s['passengers']
        for text in s['map_text']:
            if 'text' in list(text.keys()):
                self.texts.append(c.create_text(self.pos[0] + text['offset'][0], self.pos[1] + text['offset'][1], fill='black', font=text['font'], text=text['text'], anchor=text['anchor']))
            else:
                badge_img = get_badge(text['badge'])
                self.badges.append(badge_img)
                self.texts.append(c.create_image(self.pos[0] + text['offset'][0], self.pos[1] + text['offset'][1],image=self.badges[-1], anchor=text['anchor']))


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
                valid = False
                if p['options'][i]['line'] in unlocked:
                    valid = True
                elif str(type(p['options'][i]['line'])) == '<class \'list\'>':
                    if any([option in unlocked for option in p['options'][i]['line']]):
                        valid = True
                
                if valid:
                    chance = p['options'][i]['chance']
                    for j in range(chance):
                        dest_choice.append(i)
            
            decision = choice(dest_choice)
            return p['options'][decision]
        return 0

    # used to fix the missing exit bug (buying a new path and not having the option to go that way immediately)
    def reload_exits(self,unlocked_lines):

        with open(f'map/{self.map}/stations/{self.name}.json', 'r') as f:
            s = loads(f.read().strip('\n'))
        
        exits = s['exits']
        self.exits = {}
        for exit in list(exits.keys()):
            if str(type(exits[exit])) == '<class \'int\'>':
                self.exits[exit] = exits[exit]
            else:
                if test_requirements(exits[exit]['requirements'], unlocked_lines):
                    self.exits[exit] = [exits[exit]['direction']]
                    if 'line' in list(exits[exit].keys()):
                        self.exits[exit].append(exits[exit]['line'])