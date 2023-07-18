from tkinter import *
from json import loads,dumps
from time import sleep

from lib.map import Map

with open(f'map/manifest.json','r') as f:
    manifest = loads(f.read())

print('Active world: ' + manifest['Name'])
print()
print('Maps detected:')
for map_name in manifest['Parts']:
    print(map_name)

print()
map_name = input('Select a map to edit: ')

with open(f'map/{map_name}/manifest.json','r') as f:
    map_manifest = loads(f.read())

window = Tk()
screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75
window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'lightblue', xscrollincrement=1, yscrollincrement=1)
c.place(x=4,y=0)


area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])

x = -1
y = -1
chosen = False
def get_mouse_pos(event: Event):
    global x, y, chosen
    x, y = event.x, event.y
    chosen = True

pressed_space = False
def space_pressed(event):
    global pressed_space
    pressed_space = True

# get mouse coords
def get_coordinates(space_cancel = False, screen = c, div_value = 8):
    global chosen, x, y, pressed_space
    if space_cancel:
        screen.bind_all('<c>', space_pressed)
    print('Choose a coordinate')
    screen.bind_all('<Button-1>', get_mouse_pos)
    while not chosen:
        if pressed_space:
            screen.unbind_all('<c>')
            pressed_space = False
            screen.unbind_all('<Button-1>')
            return 'c', 'c'
        sleep(0.017)
        window.update()
    screen.unbind_all('<Button-1>')
    chosen = False
    x = screen.canvasx(x)
    y = screen.canvasy(y)

    x = x //div_value * div_value
    y = y //div_value * div_value

    return int(x), int(y)


def choose_requirements():
    print()
    print('REQUIREMENTS - NEED TO BE UNLOCKED')
    print('Write as format: \'map_name/line_name\'')
    req = []
    while True:
        add = input('>>> ')
        if add == '':
            break
        else:
            req.append(add)
    no = []
    print('REQUIREMENTS - MUST NOT BE UNLOCKED')
    while True:
        add = input('>>> ')
        if add == '':
            break
        else:
            no.append(add)
    
    return {"unlocked": req, "not": no}


# screen scroll functions
def scroll_left(event):
    c.xview_scroll(-40,'units')
def scroll_right(event):
    c.xview_scroll(40,'units')
def scroll_up(event):
    c.yview_scroll(-40,'units')
def scroll_down(event):
    c.yview_scroll(40,'units')
c.bind_all('<Left>', scroll_left)
c.bind_all('<Right>', scroll_right)
c.bind_all('<Up>', scroll_up)
c.bind_all('<Down>', scroll_down)

# important thingy
def create_object(event):
    global area
    add_to_existing_line = input('''
1) Add object to existing line
2) Create new line
3) Get coords of a spot
4) Create station
5) Station settings
6) WATER
>>> ''')
    if int(add_to_existing_line) == 1:
        line = input('''
Choose a line to add to: ''')
        
        with open(f'map/{map_name}/lines/{line}.json','r') as f:
            line_data = loads(f.read())

        object_choice = input(f'''
Choose object to add to {line}
1) Line segment
2) Corner
3) Conditional Corner
4) Junction
5) Stop
6) Conditional Stop

>>> ''')
        
        match int(object_choice):
            case 1:
                x1,y1 = get_coordinates()
                print(f'coords are ({x1},{y1})')
                dir = int(input('Choose a direction: '))
                x2, y2 = get_coordinates()
                match dir:
                    case 0:
                        x2=x1
                    case 1:
                        y2 = y1-(2*abs(x2-x1))
                        if x2 % 8 == 4:
                            x2 += 4
                            y2 -= 8
                    case 2:
                        y2 = y1-abs(x2-x1)
                    case 3:
                        y2 = y1-(abs(x2-x1)/2)
                        if y2 % 8 == 4:
                            y2 -= 4
                            x2 += 8
                    case 4:
                        y2=y1
                    case 5:
                        y2 = y1-(-abs(x2-x1)/2)
                        if y2 % 8 == 4:
                            y2 += 4
                            x2 += 8
                    case 6:
                        y2 = y1+abs(x2-x1)
                    case 7:
                        y2 = y1-(-2*abs(x2-x1))
                        if x2 % 8 == 4:
                            x2 += 4
                            y2 += 8
                    case 8:
                        x2=x1
                    case 9:
                        y2 = y1+(2*abs(x2-x1))
                        if x2 % 8 == 4:
                            x2 -= 4
                            y2 += 8
                    case 10:
                        y2 = y1+abs(x2-x1)
                    case 11:
                        y2 = y1+(abs(x2-x1)/2)
                        if y2 % 8 == 4:
                            y2 += 4
                            x2 -= 8
                    case 12:
                        y2=y1
                    case 13:
                        y2 = y1+(abs(x2-x1)/2)
                        if y2 % 8 == 4:
                            y2 -= 4
                            x2 -= 8
                    case 14:
                        y2 = y1-abs(x2-x1)
                    case 15:
                        y2 = y1-(2*abs(x2-x1))
                        if x2 % 8 == 4:
                            x2 -= 4
                            y2 -= 8

                line_data['segments'].append([x1,y1,x2,int(y2)])
                c1.create_line(x1/8,y1/8,x2/8,y2/8, fill=line_data['colour'])
            
            case 2:
                x1, y1 = get_coordinates()
                print(x1, y1)
                dir1 = int(input('Direction 1: '))
                dir2 = int(input('Direction 2: '))
                change_line = input('Change line? (y/n) ')
                if change_line == 'y':
                    change_to = input('Line to change to: ')
                    line_data['corners'].append([x1,y1,dir1,dir2,change_to])
                else:
                    line_data['corners'].append([x1,y1,dir1,dir2])
            
            case 3:
                req = choose_requirements()
                x1, y1 = get_coordinates()
                print(x1, y1)
                dir1 = int(input('Direction 1: '))
                dir2 = int(input('Direction 2: '))
                change_line = input('Change line? (y/n) ')
                if change_line == 'y':
                    change_to = input('Line to change to: ')
                    line_data['conditional_corners'].append({
                        'requirements': req,
                        'corner': [x1,y1,dir1,dir2,change_to]
                    })
                else:
                    line_data['conditional_corners'].append({
                        'requirements': req,
                        'corner': [x1,y1,dir1,dir2]
                    })
            
            case 4:
                req = choose_requirements()
                x1,y1 = get_coordinates()
                junc_type = int(input('''Choose a junction type:
1) Left, straight
2) Straight, right
3) Left, right (default left)
4) Left, right (default right)
5) Left, straight, right
>>> '''))
                match int(junc_type):
                    case 1:
                        options = ['left', 'straight']
                        default = 1
                    case 2:
                        options = ['straight', 'right']
                        default = 0
                    case 3:
                        options = ['left','right']
                        default = 0
                    case 4:
                        options = ['left','right']
                        default = 1
                    case 5:
                        options = ['left','straight','right']
                        default = 1
                
                print('Choose a coordinate to activate the choice window')
                x2,y2 = get_coordinates()
                dir = int(input('Moving in direction: '))

                junction = {
                    'requirements': req,
                    'coords': [x1,y1],
                    'approach': {
                        'coords': [x2,y2],
                        'direction': dir,
                        'options': options,
                        'default': default
                    }
                }

                for option in options:
                    print()
                    print(f'Going {option}:')
                    dir = int(input('New direction: '))
                    newline = input('New line: ')
                    junction[option] = {
                        'line': newline,
                        'direction': dir
                    }
                
                line_data['junctions'].append(junction)
            
            case 5:
                x1,y1 = get_coordinates()
                dir = int(input('Exit direction: '))
                line_data['stops'].append([x1,y1,dir])
            
            case 6:
                x1,y1 = get_coordinates()
                req = choose_requirements()
                dir = int(input('Exit direction: '))

                line_data['conditional_stops'].append({
                    'requirements': req,
                    'stop': [x1,y1,dir]
                })
            
        
        with open(f'map/{map_name}/lines/{line}.json','w') as f:
            f.write(dumps(line_data, indent=4))
        
        area.unload(c)
        del area
        area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])
    

    elif int(add_to_existing_line) == 2:
        name = input('Enter a name: ')
        col = input('Colour: ')
        with open(f'map/{map_name}/lines/{name}.json','w') as f:
            f.write(dumps({
                'colour': col,
                'segments': [],
                'corners': [],
                'conditional_corners':[],
                "stops": [],
                "conditional_stops": [],
                'junctions': [],
                'stations': []
            }, indent=4))
        
        map_manifest['lines'].append(name)
        with open(f'map/{map_name}/manifest.json','w') as f:
            f.write(dumps(map_manifest, indent=4))
    
    elif int(add_to_existing_line) == 3:
        print(get_coordinates())
    
    elif int(add_to_existing_line) == 4:
        station_name = input('Enter name: ')
        x, y = get_coordinates()
        station_data = {
            "name": station_name,
            "position": [x,y],
            "exits": {},
            "map_text": [],
            "passengers": {
                "chance_of_any": int(input('Chance of any passengers appearing: ')),
                "options": []
            },
            "shop": False
        }

        while True:
            name = input('Exit name (eg. westbound): ')
            if name == '':
                break
            dir = int(input('Direction: '))
            req = choose_requirements()
            line = input('Line: ')
            station_data['exits'][name] = {
                'direction': dir,
                'requirements': req,
                'line': line
            }
        

        line_name = input('Add to line: ')

        with open(f'map/{map_name}/lines/{line_name}.json','r') as f:
            line_data = loads(f.read())
        
        line_data['stations'].append(station_name)

        with open(f'map/{map_name}/lines/{line_name}.json','w') as f:
            f.write(dumps(line_data, indent=4))


        print('''Station created.
Control map text, passengers, and shop via the JSON.
''')
        
        with open(f'map/{map_name}/stations/{station_data["name"]}.json','w') as f:
            f.write(dumps(station_data, indent=4))
        
        x//=8
        y//=8

        c1.create_oval(x-2,y-2,x+2,y+2,fill='',outline='black')


        area.unload(c)
        del area
        area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])
    

    elif int(add_to_existing_line) == 5:
        station_name = input('Station to edit: ')
        with open(f'map/{map_name}/stations/{station_name}.json', 'r') as f:
            station_data = loads(f.read())
        mode = int(input('''Pick one:
1) Add passengers to this station
2) Add text to the map
3) Add a shop item
>>> '''))
        match mode:
            case 1:
                chance = int(input('Relative chance of appearing: '))
                points = int(input('Reward: '))
                lines = []
                while True:
                    line = input('This station is on line (mapname/line): ')
                    if line == '':
                        break
                    lines.append(line)
                passenger = {
                    'chance': chance,
                    'station': f'{map_name}/{station_name}',
                    'line': lines,
                    'reward': points
                }
                while True:
                    start = input('Station from (mapname/name): ')
                    if start == '':
                        break
                    start = start.split('/')
                    with open(f'map/{start[0]}/stations/{start[1]}.json','r') as f:
                        data = loads(f.read())
                    data['passengers']['options'].append(passenger)
                    with open(f'map/{start[0]}/stations/{start[1]}.json','w') as f:
                        f.write(dumps(data, indent=4))
                    print('Added.')
            
            case 2:
                print('Coords for the text object')
                x,y = get_coordinates()
                dx,dy = x - station_data['position'][0], y - station_data['position'][1]
                text = input('Text: ')
                font = input('Font: ')
                anchor = input('Anchor: ')
                station_data['map_text'].append({
                    "offset": [dx,dy],
                    "text": text,
                    "font": font,
                    "anchor": anchor
                })
            
            case 3:
                if not station_data['shop']:
                    station_data['shop'] = {}
                
                name = input('Item name: ')
                price = int(input('Cost: '))
                req = choose_requirements()
                unlock = []
                while True:
                    get = input('Unlocks line (map_name/line): ')
                    if get == '':
                        break
                    unlock.append(get)
                
                station_data['shop'][name] = {
                    "cost": price,
                    "requirements": req,
                    "unlock": unlock,
                    "unique_name": f'{map_name}/{station_name}/{name}'
                }

        
        with open(f'map/{map_name}/stations/{station_data["name"]}.json','w') as f:
            f.write(dumps(station_data, indent=4))

        area.unload(c)
        del area
        area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])

    elif int(add_to_existing_line) == 6:
        global land
        coords = []
        c1.delete(land)
        land = c1.create_line(-100,-100,-99,-100, fill='white')
        while True:
            x,y = get_coordinates(space_cancel=True, screen=c1, div_value=1)
            if x == 'c':
                break
            coords.extend([x,y])
            c1.delete(land)
            land = c1.create_polygon(tuple(coords), fill='', outline='white')
            
        map_manifest['water'] = [coord*8 for coord in coords]
        area.unload(c)
        with open(f'map/{map_name}/manifest.json','w') as f:
            f.write(dumps(map_manifest, indent=4))
        print('done')
        area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])


w1 = Tk()
c1 = Canvas(w1, width=screen_width,height=screen_height, bg='lightblue', xscrollincrement=1, yscrollincrement=1)
c1.pack()

coords = tuple([i//8 for i in area.water_coords])
land = c1.create_polygon(coords, fill='white', outline='')

# zoomed out window
for line in map_manifest['lines']:
    line_obj = area.lines[line]
    for segment in line_obj.seg_coords:
        c1.create_line(segment[0]/8,segment[1]/8,segment[2]/8,segment[3]/8,fill=line_obj.col)

    for station in line_obj.stations:
        x, y = tuple([pos//8 for pos in station.pos])
        c1.create_oval(x-2,y-2,x+2,y+2,fill='',outline='black')




selected_spot = c.create_oval(0,0,2,2,fill='black')
small_selected = c1.create_oval(0,0,2,2,fill='black')

def move_cursor(event):
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    x = x//8 * 8
    y = y//8 * 8
    c.coords(selected_spot,x-1,y-1,x+1,y+1)
    x /= 8
    y /= 8
    c1.coords(small_selected,x-1,y-1,x+1,y+1)
def move_cursor_small(event):
    x, y = c1.canvasx(event.x), c1.canvasy(event.y)
    c1.coords(small_selected,x-1,y-1,x+1,y+1)
    x *= 8
    y *= 8
    c.coords(selected_spot,x-1,y-1,x+1,y+1)


# screen scroll functions
def scroll_left_1(event):
    c1.xview_scroll(-40,'units')
def scroll_right_1(event):
    c1.xview_scroll(40,'units')
def scroll_up_1(event):
    c1.yview_scroll(-40,'units')
def scroll_down_1(event):
    c1.yview_scroll(40,'units')
c1.bind_all('<Left>', scroll_left_1)
c1.bind_all('<Right>', scroll_right_1)
c1.bind_all('<Up>', scroll_up_1)
c1.bind_all('<Down>', scroll_down_1)


# click on w1 to go to respective spot in window
def scroll_snap(event: Event):
    x, y = c1.canvasx(event.x), c1.canvasy(event.y)
    x, y = x*8, y*8
    c.xview_moveto(0.0)
    c.yview_moveto(0.0)
    c.xview_scroll(int(x)-round(screen_width/2), 'units')
    c.yview_scroll(int(y)-round(screen_height/2), 'units')
    
c1.bind_all('<Button-1>', scroll_snap)


c.bind_all('<Motion>', move_cursor)
c1.bind_all('<Motion>', move_cursor_small)



c.bind_all('<space>', create_object)


while True:
    sleep(0.017)
    window.update()
    w1.update()