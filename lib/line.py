from json import loads
from lib.station import Station
from lib.helper import test_requirements

class Line():
    def __init__(self, map_name, line_name, canvas, unlocked_lines):
        self.name = line_name
        
        with open(f'./map/{map_name}/lines/{line_name}.json', 'r') as f:
            line_data = loads(f.read().strip('\n'))

        self.segments = []
        self.seg_coords = line_data['segments']
        self.col = line_data['colour']
        for segment in self.seg_coords:
            self.segments.append(canvas.create_line(segment[0], segment[1], segment[2], segment[3], fill=self.col))
        
        self.corners = line_data['corners']

        # conditional corners
        cond_corner = line_data['conditional_corners']
        for corner in cond_corner:
            if test_requirements(corner['requirements'], unlocked_lines):
                self.corners.append(corner['corner'])

        self.stops = line_data['stops']

        # conditional stops
        cond_stop = line_data['conditional_stops']
        for stop in cond_stop:
            if all([line in unlocked_lines for line in stop['requirements']['unlocked']]) and not any([line in unlocked_lines for line in stop['requirements']['not']]):
                self.stops.append(stop['stop'])

        self.junctions = [junc for junc in line_data['junctions'] if test_requirements(junc['requirements'], unlocked_lines)]

        self.stations = [Station(name, canvas, map_name, unlocked_lines) for name in line_data['stations']]
    
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