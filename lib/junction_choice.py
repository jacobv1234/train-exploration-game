from tkinter import *
from lib.audio import AudioHandler
from lib.junction_indicator import Junction_Indicator

class JunctionChoice:
    def __init__(self, junction, window, width, audio: AudioHandler, master_canvas: Canvas):
        self.options = junction['approach']['options']
        self.num_options = len(self.options)
        self.canvas = Canvas(window, width = 80*self.num_options, height=80, bg='white')
        self.canvas.place(x=(width / 2) - (40 * self.num_options), y=3)
        self.canvas.create_rectangle(2,2,(80*self.num_options) + 1,81,fill='', outline='black')

        for i in range(self.num_options):
            option = self.options[i]
            match option:
                case 'left':
                    self.create_left_arrow(i)
                case 'straight':
                    self.create_up_arrow(i)
                case 'right':
                    self.create_right_arrow(i)
            
        self.choice = junction['approach']['default']
        self.pos = self.choice * 80

        c3 = self.pos + 3
        c13 = self.pos + 13
        c70 = self.pos + 70
        c80 = c70 + 10

        self.cursor = self.canvas.create_polygon(c13,3,c70,3,c80,13,c80,70,c70,80,c13,80,c3,70,c3,13, outline='black', fill='')

        self.canvas.bind_all('<Left>', self.move_left)
        self.canvas.bind_all('<Right>', self.move_right)
        self.canvas.bind_all('<Button-1>', self.mouse_set_choice, add = True)

        self.audio = audio

        self.line_indicator = Junction_Indicator(junction, master_canvas)
        self.junction = junction
        self.width = width
    
    def create_left_arrow(self, pos):
        x = (pos * 80) + 40
        self.canvas.create_polygon(x-20,41,x,21,x,31,x+20,31,x+20,51,x,51,x,61,fill='lightblue',outline='black')
    
    def create_up_arrow(self,pos):
        x = (pos * 80) + 40
        self.canvas.create_polygon(x,21,x+20,41,x+10,41,x+10,61,x-10,61,x-10,41,x-20,41,fill='lightblue',outline='black')

    def create_right_arrow(self,pos):
        x = (pos * 80) + 40
        self.canvas.create_polygon(x+20,41,x,21,x,31,x-20,31,x-20,51,x,51,x,61,fill='lightblue',outline='black')
    
    def move_left(self, event):
        if self.choice > 0:
            self.choice -= 1
            self.audio.play_sound_effect('scroll')
            new_direction = self.junction[self.options[self.choice]]['direction']
            self.line_indicator.update(new_direction)

    
    def move_right(self, event):
        if self.choice < self.num_options - 1:
            self.choice += 1
            self.audio.play_sound_effect('scroll')
            new_direction = self.junction[self.options[self.choice]]['direction']
            self.line_indicator.update(new_direction)

    def mouse_set_choice(self, event: Event):
        x_offset = self.num_options * 40
        x, y = event.x_root, event.y_root
        if y < 80 and x > self.width/2 - x_offset and x < self.width/2 + x_offset:
            self.choice = int((x - (self.width/2 - x_offset)) // 80)
            self.audio.play_sound_effect('scroll')
            new_direction = self.junction[self.options[self.choice]]['direction']
            self.line_indicator.update(new_direction)

    
    def update(self):
        if self.pos < self.choice * 80:
            self.pos += 16
            self.canvas.move(self.cursor,16,0)
        elif self.pos > self.choice * 80:
            self.pos -= 16
            self.canvas.move(self.cursor,-16,0)
        
    def close(self):
        self.canvas.unbind_all('<Left>')
        self.canvas.unbind_all('<Right>')
        self.canvas.destroy()
        self.line_indicator.remove()

    # used since opening the minimap unbinds them and they need to be rebound when closed
    def re_enable_controls(self):
        self.canvas.bind_all('<Left>', self.move_left)
        self.canvas.bind_all('<Right>', self.move_right)