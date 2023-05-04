from tkinter import *
from time import sleep

# import objects
from lib.map import Map
from lib.train import Train
from lib.speedtracker import SpeedTracker
from lib.junction_choice import JunctionChoice
from lib.space_to_enter import PressSpaceToEnter

window = Tk()

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white', xscrollincrement=1, yscrollincrement=1)
c.place(x=3,y=0)

# create the map
start_map = 'map'
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

# loop
while True:
    train.move_train(c)

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
    
    station = area.check_stations(train.x, train.y, train.line)
    if station != 0 and train.speed == 0 and not press_space:
        press_space = PressSpaceToEnter(window, screen_width, screen_height)
        #c.bind_all('<space>', enter_station)
    if train.speed != 0 and press_space:
        press_space.remove()
        del press_space
        press_space = False

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

    window.update()
    sleep(0.015)