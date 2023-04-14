from tkinter import *
window = Tk()
c = Canvas(window, width = 350, height = 250, bg = 'white')
c.pack()

directions = (
    (0,-2), #0, up
    (1,-2), #1, up-up-right
    (2,-2), #2, up-right
    (2,-1), #3, up-right-right
    (2,0),  #4, right
    (2,1),  #5, down-right-right
    (2,2),  #6, down-right
    (1,2),  #7, down-down-right
    (0,2),  #8, down
    (-1,2), #9, down-down-left
    (-2,2), #10 down-left
    
)

# create train
train = c.create_rectangle