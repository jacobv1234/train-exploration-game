from tkinter import *
from time import sleep

# import objects
from objects.line import Line
from objects.map import Map

window = Tk()

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white')
c.pack()

# create the map
start_map = 'map'
area = Map(start_map, c)

# loop
while True:
    window.update()
    sleep(0.08)