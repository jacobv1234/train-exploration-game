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

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white', xscrollincrement=1, yscrollincrement=1)
c.place(x=4,y=0)

area = Map(map_name, c, [f'{map_name}/{name}' for name in map_manifest['lines']])

x = -1
y = -1
chosen = False
def get_mouse_pos(event: Event):
    global x, y, chosen
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    chosen = True

# get mouse coords
def get_coordinates():
    global chosen, x, y
    print('Choose a coordinate')
    c.bind_all('<Button-1>', get_mouse_pos)
    while not chosen:
        sleep(0.017)
        window.update()
    c.unbind_all('<Button-1>')
    chosen = False
    x = x //8 * 8
    y = y //8 * 8

    return x, y


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
7) Station

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
                    case 2:
                        y2 = y1-abs(x2-x1)
                    case 3:
                        y2 = y1-(abs(x2-x1)/2)
                    case 4:
                        y2=y1
                    case 5:
                        y2 = y1-(-abs(x2-x1)/2)
                    case 6:
                        y2 = y1+abs(x2-x1)
                    case 7:
                        y2 = y1-(-2*abs(x2-x1))
                    case 8:
                        x2=x1
                    case 9:
                        y2 = y1+(2*abs(x2-x1))
                    case 10:
                        y2 = y1+abs(x2-x1)
                    case 11:
                        y2 = y1+(abs(x2-x1)/2)
                    case 12:
                        y2=y1
                    case 13:
                        y2 = y1+(abs(x2-x1)/2)
                    case 14:
                        y2 = y1-abs(x2-x1)
                    case 15:
                        y2 = y1-(2*abs(x2-x1))

                line_data['segments'].append([x1,y1,x2,y2])
            
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
            
            case 7:
                print()
                station = input('Choose a station to add to this line: ')
                line_data['stations'].append(station)
            
        
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


                

c.bind_all('<space>', create_object)

while True:
    sleep(0.017)
    window.update()