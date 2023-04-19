from json import loads

class Line():
    def __init__(self, map_name, line_name, canvas):
        self.name = line_name
        
        with open(f'/{map_name}/lines/{line_name}.json', 'r') as f:
            line_data = loads(f.read().strip('\n'))

        self.segments = []
        for segment in line_data['segments']:
            canvas.create_line(segment[0], segment[1], segment[2], segment[3], fill=line_data['colour'])
        
        self.corners = line_data['corners']