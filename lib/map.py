from json import loads
from lib.line import Line
from lib.decoline import DecoLine
from lib.station_group import StationGroup
from tkinter import *

class Map():
    def __init__(self, name: str, canvas: Canvas, unlocked_lines: list[str], mode = 'main'):
        # load the manifest file
        folder = 'map'
        with open(f'./{folder}/{name}/manifest.json', 'r') as f:
            manifest = loads(f.read().strip('\n'))
        
        # create water
        if manifest['water']:
            self.water = canvas.create_polygon(tuple(manifest['water']), fill='white', outline='')
        else:
            self.water = canvas.create_line(-100,-100,-99,-100, fill='white')

        # load each line
        created_stations = {}
        self.lines = {}
        for line in manifest['lines']:
            if f'{name}/{line}' in unlocked_lines:
                # cosmetic line split
                if line[0] != '_':
                    line_object = Line(name, line, canvas, unlocked_lines, created_stations, folder, mode)
                else:
                    line_object = DecoLine(name, line, canvas, unlocked_lines, folder)
                    if line_object.name == 0:
                        continue

                self.lines[line_object.name] = line_object

        self.lz = manifest['loadingzones']

        self.name = manifest['display_name']
        self.size = manifest['fontsize']

        self.internal_name = name
        self.water_coords = manifest['water']

        self.scroll_boundary = manifest['scroll_bounds']

        for line in list(self.lines.keys()):
            for segment in self.lines[line].segments:
                canvas.tag_lower(segment)

        self.station_groups = {}
        for group in manifest['station_groups']:
            self.station_groups[group] = StationGroup(group, canvas, name, unlocked_lines)

        canvas.tag_lower(self.water)
        self.manifest = manifest

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