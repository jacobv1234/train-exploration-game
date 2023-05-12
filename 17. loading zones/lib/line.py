from json import loads
from lib.station import Station

class Line():
    def __init__(self, map_name, line_name, canvas):
        self.name = line_name
        
        with open(f'./map/{map_name}/lines/{line_name}.json', 'r') as f:
            line_data = loads(f.read().strip('\n'))

        self.segments = []
        for segment in line_data['segments']:
            self.segments.append(canvas.create_line(segment[0], segment[1], segment[2], segment[3], fill=line_data['colour']))
        
        self.corners = line_data['corners']

        self.stops = line_data['stops']

        self.junctions = line_data['junctions']

        self.stations = [Station(name, canvas, map_name) for name in line_data['stations']]
    
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

    def check_stations(self, x, y):
        for station in self.stations:
            pos = station.pos
            if x in range(pos[0]-12, pos[0]+12) and y in range(pos[1]-12, pos[1]+12):
                return station
        return 0
    
    def unload(self, c):
        for i in range(len(self.segments)-1,-1,-1):
            c.delete(self.segments[i])
        for i in range(len(self.stations)-1,-1,-1):
            self.stations[i].unload(c)