from tkinter import *
from time import sleep

window = Tk()

screen_width = window.winfo_screenwidth() - 10
screen_height = window.winfo_screenheight() - 75

window.state('zoomed')

c = Canvas(window, width = screen_width, height = screen_height, bg = 'white')
c.pack()

directions = ( #(x,y)
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
    (-2,1), #11 down-left-left
    (-2,0), #12 left
    (-2,-1),#13 up-left-left
    (-2,-2),#14 up-left
    (-1,-2) #15 up-up-left
)

# create train
class Train():
    def __init__(self, startx, starty, startdir, c = Canvas()):
        self.x = startx
        self.y = starty
        self.direction = startdir
        self.speed = 0
        self.object = c.create_rectangle(startx-10, starty-10, startx+10, starty+10, outline='black')
        c.bind_all('<Left>', self.turn_left)
        c.bind_all('<Right>', self.turn_right)
        c.bind_all('<Up>', self.speed_up)
        c.bind_all('<Down>', self.slow_down)

    def turn_left(self, event):
        self.direction -= 1
        self.direction %= 16
    
    def turn_right(self, event):
        self.direction += 1
        self.direction %= 16
    
    def speed_up(self, event):
        if self.speed == 0:
            self.speed = 4
        elif self.speed == 4:
            self.speed = 8
    
    def slow_down(self, event):
        if self.speed == 8:
            self.speed = 4
        elif self.speed == 4:
            self.speed = 0

    def move_train(self, c = Canvas()):
        dir_vect = directions[self.direction]
        c.move(self.object, dir_vect[0] * self.speed, dir_vect[1] * self.speed)
        



train = Train(screen_width / 2, screen_height / 2, 0, c)

while True:
    train.move_train(c)
    window.update()
    sleep(0.08)