from json import loads
from objects.line import Line

class Map():
    def __init__(self, name, canvas):
        # load the manifest file
        with open(f'./{name}/manifest.json', 'r') as f:
            manifest = loads(f.read().strip('\n'))
        
        # load each line
        self.lines = []
        for line in manifest['lines']:
            self.lines.append(Line(name, line, canvas))
        
        self.start = manifest['start']