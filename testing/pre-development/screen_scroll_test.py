from tkinter import *
from tkinter import PhotoImage
from time import sleep

window = Tk()
c = Canvas(window, width=300, height=300, background='white')
c.pack()

background = PhotoImage(file='Logo.gif')

image = c.create_image(-350,150, image = background)

def move_image(event):
    if event.keysym == 'Up':
        c.move(image, 0, -5)
    elif event.keysym == 'Down':
        c.move(image, 0, 5)
    elif event.keysym == 'Left':
        c.move(image, -5, 0)
    elif event.keysym == 'Right':
        c.move(image, 5, 0)

c.bind_all('<Key>', move_image)

while True:
    window.update()
    sleep(0.01)