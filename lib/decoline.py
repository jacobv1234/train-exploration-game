from json import loads
from lib.helper import test_requirements, get_line_poly_coords

class DecoLine():
    def __init__(self, map_name, line_name, canvas, unlocked_lines, folder):
        self.name = line_name
        
        with open(f'./{folder}/{map_name}/lines/{line_name}.json', 'r') as f:
            line_data = loads(f.read().strip('\n'))
        
        # decolines have requirements
        if not test_requirements(line_data['requirements'],unlocked_lines):
            self.name = 0
            return


        self.segments = []

        # this is so zoomed_map doesn't break
        self.stations = []
        
        self.seg_coords = line_data['segments']
        self.col = line_data['colour']
        for segment in self.seg_coords:
            #self.segments.append(canvas.create_line(segment[0], segment[1], segment[2], segment[3], fill=self.col))
            self.segments.append(canvas.create_polygon(get_line_poly_coords(segment), fill=self.col))
        
        
        self.corners = line_data['corners']
        for corner in self.corners:
            self.segments.append(canvas.create_oval(corner[0]-4, corner[1]-4, corner[0]+3, corner[1]+3, fill=self.col,outline=self.col))

        for segment in self.segments:
            canvas.tag_lower(segment)

    
    def unload(self, c):
        for i in range(len(self.segments)-1,-1,-1):
            c.delete(self.segments[i])