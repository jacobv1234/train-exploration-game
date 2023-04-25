from json import loads
from objects.line import Line

class Map():
    def __init__(self, name, canvas):
        # load the manifest file
        with open(f'./{name}/manifest.json', 'r') as f:
            manifest = loads(f.read().strip('\n'))
        
        # load each line
        self.lines = {}
        for line in manifest['lines']:
            line_object = Line(name, line, canvas)
            self.lines[line_object.name] = line_object
        
        self.start = manifest['start']
        self.start_line = manifest['start_line']
    
    def check_corners(self, x, y, line):
        return self.lines[line].check_corners(x,y)
    
    def check_stops(self, x, y, line):
        return self.lines[line].check_stops(x,y)