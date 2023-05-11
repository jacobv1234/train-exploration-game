from tkinter import *
from time import sleep

# import objects
from lib.map import Map
from lib.train import Train
from lib.speedtracker import SpeedTracker
from lib.junction_choice import JunctionChoice
from lib.space_to_enter import PressSpaceToEnter
from lib.station_display import StationDisplay

window = Tk()

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white', xscrollincrement=1, yscrollincrement=1)
c.place(x=4,y=0)

# create the map
start_map = 'main'
# called area cause map is a function
area = Map(start_map, c)
 
# hud
speedtracker = SpeedTracker(window,screen_width,screen_height)

# train
train = Train(area.start[0], area.start[1], area.start[2], area.start_line, c, skin='train')

# center on screen
c.xview_scroll(area.start[0] - (round(screen_width / 2)), 'units')
c.yview_scroll(area.start[1] - (round(screen_height / 2)), 'units')

# initialise certain variables
junc = False
press_space = False
space_pressed = False
in_station = False
mapnamecounter = -1

# functions that work better in main than in lib.helper
def pressed_space(event):
    global space_pressed
    space_pressed = True

def HandleMapNameCounter():
    global mapnamecounter
    if mapnamecounter >= 0:
        mapnamecounter -= 1
        if mapnamecounter == 0:
            pass


# loop
while True:
    train.move_train(c)

    # check collisions with objects
    corner = area.check_corners(train.x, train.y, train.line)
    if corner != 0:
        train.corner(corner)

    if junc != False:
        if junc['coords'][0] == train.x and junc['coords'][1] == train.y:
            train.junction(junc, chooser.options[chooser.choice])
            junc = False
            chooser.close()
            del chooser
    
    stop = area.check_stops(train.x,train.y,train.line)
    if stop != 0:
        train.stop(stop, c)

    junction = area.check_j_approach(train.x,train.y,train.direction, train.line)
    if junction != 0:
        chooser = JunctionChoice(junction,window,screen_width)
        junc = junction

    # loading zones
    lz = area.check_lz(train.x, train.y, train.direction)
    if lz != 0:
        area.unload(c)
        area = Map(lz['map'], c)
        # move train and camera
        # dir
        train.direction = lz['new_dir']
        # coords
        current_x = train.x
        current_y = train.y
        train.x = lz['new_pos'][0]
        train.y = lz['new_pos'][1]
        # camera
        scroll_x = train.x - current_x
        scroll_y = train.y - current_y
        c.xview_scroll(scroll_x, 'units')
        c.yview_scroll(scroll_y, 'units')
        # object
        c.move(train.object,scroll_x, scroll_y)
        c.tag_raise(train.object)
        # line
        train.line = lz['new_line']
    

    # station entry
    station = area.check_stations(train.x, train.y, train.line)
    if station != 0 and train.speed == 0 and not press_space:
        press_space = PressSpaceToEnter(window, screen_width, screen_height)
        c.bind_all('<space>', pressed_space)
    elif train.speed != 0 and press_space:
        press_space.remove()
        c.unbind_all('<space>')
        del press_space
        press_space = False
    
    if space_pressed and not in_station:
        space_pressed = False
        train.disable_speed_controls(c)
        in_station = StationDisplay(window, screen_width, screen_height, station)
    
    # handle station choices
    elif space_pressed and in_station:
        space_pressed = False
        result = in_station.select_current()
        if result[0] == 'exit':
            # exit and move the train
            # dir
            train.direction = station.exits[result[1]]
            # coords
            current_x = train.x
            current_y = train.y
            train.x = station.pos[0]
            train.y = station.pos[1]
            # camera
            scroll_x = train.x - current_x
            scroll_y = train.y - current_y
            c.xview_scroll(scroll_x, 'units')
            c.yview_scroll(scroll_y, 'units')

            # object
            c.move(train.object,scroll_x, scroll_y)

            # exit the menu
            in_station.close()
            del in_station
            in_station = False
            train.enable_speed_controls(c)



    # update HUD
    match train.speed:
        case 0:
            destination = 280
        case 1:
            destination = 200
        case 2:
            destination = 120
        case 4:
            destination = 40
    speedtracker.update(destination)

    try:
        chooser.update()
    except: pass

    if in_station:
        in_station.update_cursor()

    window.update()
    sleep(0.015)
    print(train.x, train.y, train.line)