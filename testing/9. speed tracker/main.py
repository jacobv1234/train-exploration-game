from tkinter import *
from time import sleep

# import objects
from objects.map import Map
from objects.train import Train
from objects.speedtracker import SpeedTracker

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

# loop
while True:
    train.move_train(c)
    corner = area.check_corners(train.x, train.y, train.line)
    if corner != 0:
        train.corner(corner)
    
    # update HUD
    match train.speed:
        case 0:
            destination = 200
        case 2:
            destination = 120
        case 4:
            destination = 40
    speedtracker.update(destination)

    window.update()
    sleep(0.03)