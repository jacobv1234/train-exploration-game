from tkinter import *

class JunctionChoice:
    def __init__(self, junction, window, width):
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
            
        self.cursor = self.canvas.create_polygon(13,3,70,3,80,13,80,70,70,80,13,80,3,70,3,13, outline='black', fill='')
        self.choice = 0
        self.pos = 0

        self.canvas.bind_all('<Left>', self.move_left)
        self.canvas.bind_all('<Right>', self.move_right)
    
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
    
    def move_right(self, event):
        if self.choice < self.num_options - 1:
            self.choice += 1
    
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