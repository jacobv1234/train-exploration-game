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
        for line in self.data['connecting_lines']:
            if any([val in unlocked_lines for val in self.data['station_lines'][line[0]]]) \
                and \
                any([val in unlocked_lines for val in self.data['station_lines'][line[1]]]):

                self.line_objects.append(c.create_line(line[2],line[3],line[4],line[5],fill='black'))

    
    def unload(self, c: Canvas):
        for i in range(len(self.line_objects)-1, -1, -1):
            c.delete(self.line_objects[i])