from json import loads
from lib.line import Line

class Map():
    def __init__(self, name, canvas):
        # load the manifest file
        with open(f'./map/{name}/manifest.json', 'r') as f:
            manifest = loads(f.read().strip('\n'))
        
        # load each line
        self.lines = {}
        for line in manifest['lines']:
            line_object = Line(name, line, canvas)
            self.lines[line_object.name] = line_object
        
        self.start = manifest['start']
        self.start_line = manifest['start_line']

        self.lz = manifest['loadingzones']

        self.name = manifest['display_name']
        self.size = manifest['fontsize']
    
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
    
    def check_lz(self, x, y, dir):
        for lz in self.lz:
            if lz['coords'][0] == x and lz['coords'][1] == y and lz['dir'] == dir:
                return lz
        return 0