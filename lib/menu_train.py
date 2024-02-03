from tkinter import PhotoImage
from lib.helper import opp_dir, get_train_graphics

# menu version of train
class MenuTrain():
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

    def __init__(self, startx, starty, startdir, start_line, c, skin):
        self.x = startx
        self.y = starty
        self.direction = startdir
        self.speed = 2
        self.line = start_line
        self.graphics = get_train_graphics(skin)
        self.object = c.create_image(startx, starty, image = self.graphics[startdir], anchor = 'center')

    def move_train(self, c):
        dir_vect = self.directions[self.direction]

        c.itemconfig(self.object, image = self.graphics[self.direction])
        c.move(self.object, dir_vect[0] * self.speed, dir_vect[1] * self.speed)

        self.x += dir_vect[0] * self.speed
        self.y += dir_vect[1] * self.speed
    
    def corner(self, corner):
        if self.direction == opp_dir(corner[2]):
            self.direction = corner[3]
        elif self.direction == opp_dir(corner[3]):
            self.direction = corner[2]
        if len(corner) == 5:
            self.line = corner[4]