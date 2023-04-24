from tkinter import PhotoImage
from objects.helper import opp_dir

# create train
class Train():
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
        self.speed = 0
        self.speedup = False
        self.line = start_line
        self.graphics = []
        for i in range(16):
            self.graphics.append(PhotoImage(file=f'./graphics/{skin}{i}.png'))
        self.object = c.create_image(startx, starty, image = self.graphics[startdir], anchor = 'center')
        c.bind_all('<Up>', self.speed_up)
        c.bind_all('<Down>', self.slow_down)
        c.bind_all('<space>', self.turn_180)
    
    def speed_up(self, event):
        if self.speed == 0:
            self.speed = 2
        elif self.speed == 2:
            # done differently to ensure stay on grid
            self.speedup = True
    
    def slow_down(self, event):
        if self.speed == 4:
            self.speed = 2
        elif self.speed == 2:
            self.speed = 0
    
    def turn_180(self,event):
        self.direction = opp_dir(self.direction)

    def move_train(self, c):
        dir_vect = self.directions[self.direction]

        # handle speeding up in a way that maintains grid alignment
        if self.speedup and self.x % 8 == 0 and self.y % 8 == 0:
            self.speed = 4
            self.speedup = False

        c.itemconfig(self.object, image = self.graphics[self.direction])
        c.move(self.object, dir_vect[0] * self.speed, dir_vect[1] * self.speed)

        c.xview_scroll(dir_vect[0] * self.speed, 'units')
        c.yview_scroll(dir_vect[1] * self.speed, 'units')

        self.x += dir_vect[0] * self.speed
        self.y += dir_vect[1] * self.speed
    
    def corner(self, corner):
        if self.direction == opp_dir(corner[2]):
            self.direction = corner[3]
        elif self.direction == opp_dir(corner[3]):
            self.direction = corner[2]