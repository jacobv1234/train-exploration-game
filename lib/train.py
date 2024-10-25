from tkinter import PhotoImage, Event, Canvas
from lib.helper import opp_dir, get_train_graphics
from lib.speedtracker import SpeedTracker

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

    def __init__(self, startx, starty, startdir, start_line, c: Canvas, skin, screen_width, screen_height):
        self.x = startx
        self.y = starty
        self.direction = startdir
        self.speed = 0
        self.speedup_1 = False
        self.speedup_2 = False
        self.controls_enabled = True
        self.line = start_line
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.graphics = get_train_graphics(skin)
        self.object = c.create_image(startx, starty, image = self.graphics[startdir], anchor = 'center')
        c.bind_all('<Up>', self.speed_up)
        c.bind_all('<Down>', self.slow_down)
        c.bind_all('<Button-1>', self.mouse_set_speed)
        
    
    def speed_up(self, event):
        if self.speed == 0:
            self.speed = 1

        elif self.speed == 1:
            # done differently to ensure stay on grid
            self.speedup_1 = True

        elif self.speed == 2:
            self.speedup_2 = True
    
    def slow_down(self, event):
        if self.speed == 4:
            self.speed = 2

        elif self.speed == 2:
            self.speed = 1

        elif self.speed == 1:
            self.speed = 0
    
    def mouse_set_speed(self, event: Event):
        x, y = event.x_root, event.y_root
        if x > self.screen_width - 80 and y > self.screen_height/2 -160 and y < self.screen_height/2 +160 and self.controls_enabled:
            selected =  3 - ((y - (self.screen_height/2 - 160)) // 80)
            match selected:
                case 0:
                    self.speed = 0
                case 1:
                    self.speed = 1
                case 2:
                    self.speedup_1 = True
                case 3:
                    self.speedup_2 = True


    def move_train(self, c: Canvas):
        dir_vect = self.directions[self.direction]

        # handle speeding up in a way that maintains grid alignment
        if self.speedup_1 and self.x % 4 == 0 and self.y % 4 == 0:
            self.speed = 2
            self.speedup_1 = False
        if self.speedup_2 and self.x % 8 == 0 and self.y % 8 == 0:
            self.speed = 4
            self.speedup_2 = False

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
        if len(corner) == 5:
            self.line = corner[4]
    
    def stop(self, stop, c: Canvas):
        if self.direction != stop[2]:
            self.speed = 0
            self.speedup_1 = False
            self.speedup_2 = False
            self.disable_speed_controls(c)
        else:
            self.enable_speed_controls(c)
    
    def disable_speed_controls(self, c: Canvas):
        c.unbind_all('<Up>')
        c.unbind_all('<Down>')
        self.controls_enabled = False

    
    def enable_speed_controls(self, c: Canvas):
        c.bind_all('<Up>', self.speed_up)
        c.bind_all('<Down>', self.slow_down)
        self.controls_enabled = True

    
    def junction(self, junction, choice):
        outcome = junction[choice]
        if outcome != 'continue':
            self.line = outcome['line']
            self.direction = outcome['direction']