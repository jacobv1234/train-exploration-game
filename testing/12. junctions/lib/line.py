from json import loads

class Line():
    def __init__(self, map_name, line_name, canvas):
        self.name = line_name
        
        with open(f'./{map_name}/lines/{line_name}.json', 'r') as f:
            line_data = loads(f.read().strip('\n'))

        for segment in line_data['segments']:
            canvas.create_line(segment[0], segment[1], segment[2], segment[3], fill=line_data['colour'])
        
        self.corners = line_data['corners']

        self.stops = line_data['stops']

        self.junctions = line_data['junctions']
    
    def check_corners(self, x,y):
        for corner in self.corners:
            if corner[0] == x and corner[1] == y:
                return corner
        return 0

    def check_stops(self, x,y):
        for stop in self.stops:
            if stop[0] == x and stop[1] == y:
                return stop
        return 0

    def check_j_approach(self, x,y,dir):
        for junction in self.junctions:
            if junction['approach']['coords'][0] == x and junction['approach']['coords'][1] == y and dir == junction['approach']['direction']:
                return junction
        return 0