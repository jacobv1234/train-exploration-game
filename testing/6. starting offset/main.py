from tkinter import *
from time import sleep

# import objects
from objects.map import Map
from objects.train import Train

window = Tk()

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white', xscrollincrement=1, yscrollincrement=1)
c.pack()

# create the map
start_map = 'map'
# called area cause map is a function
area = Map(start_map, c)

# train
train = Train(area.start[0], area.start[1], area.start[2], c, skin='train')

# center on screen
c.xview_scroll(area.start[0] - (round(screen_width / 2)), 'units')
c.yview_scroll(area.start[1] - (round(screen_height / 2)), 'units')

# loop
while True:
    train.move_train(c)
    window.update()
    sleep(0.03)