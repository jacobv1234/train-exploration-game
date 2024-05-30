# group of stations under a single name
from tkinter import *
from lib.station import Station
from json import loads

class StationGroup:
    def __init__(self, name: str, c: Canvas, map_name: str, unlocked_lines: list):
        self.name = name
        with open(f'map/{map_name}/station_groups/{name}.json', 'r') as f:
            self.data = loads(f.read().strip('\n'))

        self.line_objects = []
        self.created = []
        for line in self.data['connecting_lines']:
            if any([val in self.data['station_lines'][line[0]] for val in unlocked_lines]) \
                and \
                any([val in self.data['station_lines'][line[1]] for val in unlocked_lines]):

                self.line_objects.append(c.create_line(line[2],line[3],line[4],line[5],fill='black'))
                self.created.append(line[2:])

        for line in self.line_objects:
            c.tag_lower(line)
    
    def unload(self, c: Canvas):
        for i in range(len(self.line_objects)-1, -1, -1):
            c.delete(self.line_objects[i])