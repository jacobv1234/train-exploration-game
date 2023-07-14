from json import loads
from lib.line import Line
from tkinter import *

class Map():
    def __init__(self, name: str, canvas: Canvas, unlocked_lines: list[str]):
        # load the manifest file
        with open(f'./map/{name}/manifest.json', 'r') as f:
            manifest = loads(f.read().strip('\n'))
        
        # create water
        if manifest['water']:
            self.water = canvas.create_polygon(tuple(manifest['water']), fill='lightblue', outline='')
        else:
            self.water = canvas.create_line(-100,-100,-99,-100, fill='white')

        # load each line
        created_stations = []
        self.lines = {}
        for line in manifest['lines']:
            if f'{name}/{line}' in unlocked_lines:
                line_object = Line(name, line, canvas, unlocked_lines, created_stations)
                created_stations = line_object.created_stations[:]
                line_object.clear_created_stations()
                self.lines[line_object.name] = line_object
        
        self.start = manifest['start']
        self.start_line = manifest['start_line']

        self.lz = manifest['loadingzones']

        self.name = manifest['display_name']
        self.size = manifest['fontsize']

        self.internal_name = name
        self.water_coords = manifest['water']


    def check_corners(self, x, y, line):
        return self.lines[line].check_corners(x,y)
    
    def check_stops(self, x, y, line):
        return self.lines[line].check_stops(x,y)

    def check_j_approach(self, x, y, dir, line):
        return self.lines[line].check_j_approach(x,y,dir)

    def check_stations(self,x,y,line):
        return self.lines[line].check_stations(x,y)
    
    def unload(self, c):
        keys = self.lines.keys()
        for line in keys:
            self.lines[line].unload(c)
        c.delete(self.water)
    
    def check_lz(self, x, y, dir):
        for lz in self.lz:
            if lz['coords'][0] == x and lz['coords'][1] == y and lz['dir'] == dir:
                return lz
        return 0