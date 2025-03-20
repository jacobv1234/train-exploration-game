# contains helper functions

from tkinter import *
from json import loads
from math import floor

from PIL import Image, ImageTk

# returns the opposite direction
def opp_dir(dir):
    return (dir + 8) % 16

# check if a requirements meets the unlocked lines
def test_requirements(req, unlocked):
    return all([line in unlocked for line in req['unlocked']]) and not any([line in unlocked for line in req['not']])

# get savedata
def get_unlocked_lines(savepath):
    with open(f'{savepath}/unlocked_lines.txt', 'r') as f:
        unlocked_lines = [line[:-1] for line in f.readlines()]
    return unlocked_lines

def get_bought_items(savepath):
    with open(f'{savepath}/bought.txt', 'r') as f:
        bought = [line[:-1] for line in f.readlines()]
    return bought

def get_pos_save(savepath):
    with open(f'{savepath}/pos.txt','r') as f:
        values = tuple([val[:-1] for val in f.readlines()])
    return values


# save pos.txt
def save_pos(x: int, y: int, dir: int, map: str, line: str, points: int):
    values = [str(val) + '\n' for val in [x,y,dir,map,line,points]]
    with open('savedata/pos.txt','w') as f:
        f.writelines(values)

# load whole map manifest.json
def get_map_manifest():
    with open('map/manifest.json') as f:
        data = loads(f.read())
    return data


# creates a popup message in the top right, with
# a title, message, and number of frames until removed
class Popup:
    def __init__(self, window: Tk, width: int, title: str, message: str, remove: int):
        self.c = Canvas(window, width=350, height=150, bg='white')
        self.c.place(x=width-350, y=0)
        self.c.create_rectangle(2,2,348,148, fill='white', outline='black')
        self.title = self.c.create_text(25, 30, fill='black', font='Arial 20', text=title, anchor='nw')
        self.message = self.c.create_text(25, 100,fill='black', font='Arial 16', text=message, anchor='nw', width=300)
        self.timeout = remove
    
    def countdown(self):
        self.timeout -= 1
        if self.timeout == 0:
            self.c.destroy()
        return self.timeout
    
    def remove(self):
        self.c.destroy()


# get the complete set of graphics for a skin
def get_train_graphics(skin, zoom = 1):
    angles = [90, 63.5, 45, 26.5, 0, -26.5, -45, -63.5, -90, -113.5, -135, -153.5, 180, 153.5, 135, 113.5]
    results = []
    with Image.open(f'./skins/{skin}.png') as im:
        for angle in angles:
            results.append(ImageTk.PhotoImage(im.rotate(angle, Image.Resampling.BILINEAR).resize((im.width * zoom, im.height * zoom), resample= Image.Resampling.BOX)))
    
    return results

# get a station badge image
def get_badge(name):
    with Image.open(f'./badges/{name}.png') as im:
        return ImageTk.PhotoImage(im)


def get_direction(segment):
    x1,y1,x2,y2 = tuple(segment)
    if x1 == x2:
        return 0
    gradient = (y1-y2)/(x1-x2)
    match gradient:
        case 2:
            return 1
        case 1:
            return 2
        case 0.5:
            return 3
        case 0:
            return 4
        case -0.5:
            return 5
        case -1:
            return 6
        case -2:
            return 7



def get_line_poly_coords(segment, radius = 4):
    direction = get_direction(segment)
    x1,y1,x2,y2 = tuple(segment)
    x_offset = 0
    y_offset = 0
    match direction:
        case 0:
            x_offset = radius
        case 4:
            y_offset = radius
        case 6:
            x_offset = (2.8284 * radius) / 4
            y_offset = (2.8284 * radius) / 4
            if radius == 1:
                x_offset = 0.5
                y_offset = 0.5
        case 2:
            x_offset = (2.8284 * radius) / 4
            y_offset = (-2.8284 * radius) / 4
            if radius == 1:
                x_offset = 0.5
                y_offset = -0.5
        case 7:
            x_offset = (3.5776 * radius) / 4
            y_offset = (1.789 * radius) / 4
        case 1:
            x_offset = (3.5776 * radius) / 4
            y_offset = (-1.789 * radius) / 4
        case 3:
            x_offset = (1.789 * radius) / 4
            y_offset = (-3.5776 * radius) / 4
        case 5:
            x_offset = (1.789 * radius) / 4
            y_offset = (3.5776 * radius) / 4
            
    return [x1+x_offset, y1+y_offset, x1-x_offset, y1-y_offset,
            x2-x_offset, y2-y_offset, x2+x_offset, y2+y_offset]

# returns a list of all possible exit directions at a station
def get_exit_directions(station):
    exits = station.exits
    dirs = []
    for exit in list(exits.keys()):
        try:
            dirs.append(exits[exit][0])
        except TypeError:
            dirs.append(exits[exit])
    return dirs

# create the coordinate set for a short 50-pixel line that originates from a point and goes in a direction
# the returned value can then be used in canvas.create_polygon to make the line
def short_line_coord_generator(x: int, y: int, dir: int):
    coords = [x,y]
    match dir:
        case 0:
            coords.extend([x, y-50])
        case 1:
            coords.extend([x+22.36, y-44.72])
        case 2:
            coords.extend([x+35.355, y-35.355])
        case 3:
            coords.extend([x+44.72, y-22.36])
        case 4:
            coords.extend([x+50, y])
        case 5:
            coords.extend([x+44.72, y+22.36])
        case 6:
            coords.extend([x+35.355, y+35.355])
        case 7:
            coords.extend([x+22.36, y+44.72])
        case 8:
            coords.extend([x, y+50])
        case 9:
            coords.extend([x-22.36, y+44.72])
        case 10:
            coords.extend([x-35.355, y+35.355])
        case 11:
            coords.extend([x-44.72, y+22.36])
        case 12:
            coords.extend([x-50, y])
        case 13:
            coords.extend([x-44.72, y-22.36])
        case 14:
            coords.extend([x-35.355, y-35.355])
        case 15:
            coords.extend([x-22.36, y-44.72])
    return tuple(coords)


# get the completion % for a map
def get_complete_percent(area):
    lines = area.manifest['lines']
    unlocked = 0
    for line in list(area.lines.keys()):
        if line in lines:
            unlocked += 1
    # the -1 comes from the test line
    return floor((unlocked/(len(lines)-1))*100)