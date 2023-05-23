from tkinter import *
from lib.station import Station

class StationDisplay:
    def __init__(self, window: Tk, screen_width:int, screen_height:int, station: Station):
        self.c = Canvas(window, width=screen_width, height=screen_height, bg='white')
        self.c.place(x=4,y=0)
        self.c.create_text(20,10,fill='black', font='Arial 40', text=f'{station.name} Station', anchor='nw')
        self.c.create_line(0,80,screen_width,80, fill='black')
        self.c.create_line(0,110,screen_width,110,fill='black')

        self.page_contents = []
        self.possible_cursor_positions = []
        self.space = screen_height - 110
        self.width = screen_width
        self.height = screen_height
        self.station = station

        self.options = []
        self.page = 'exit'
        self.assemble_exit_page()
        self.cursor_graphic = PhotoImage(file='./graphics/train4.png').zoom(3)
        self.cursor_pos = 0
        self.cursor = self.c.create_image(self.width/4, self.possible_cursor_positions[0], image = self.cursor_graphic, anchor='center')
        window.update()

        self.c.bind_all('<Up>',self.move_cursor_up)
        self.c.bind_all('<Down>', self.move_cursor_down)


    def assemble_exit_page(self):
        for i in range(len(self.station.exits.keys())):
            exit_name = list(self.station.exits.keys())[i]
            location = ((self.space / len(self.station.exits.keys())) * (i + 0.5)) + 110
            self.page_contents.append(self.c.create_text((self.width/5)*4, location, fill='black', font='Arial 30', text=f'Exit {exit_name}', anchor='e'))
            self.possible_cursor_positions.append(location)
            self.options.append(exit_name)
    

    def assemble_passenger_page(self):
        pass

    
    def move_cursor_up(self, event):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
    
    def move_cursor_down(self, event):
        if self.cursor_pos + 1 < len(self.possible_cursor_positions):
            self.cursor_pos += 1
    

    def update_cursor(self):
        self.c.coords(self.cursor, self.width/4, self.possible_cursor_positions[self.cursor_pos])

    def select_current(self):
        return [self.page, self.options[self.cursor_pos]]
    
    def close(self):
        self.c.destroy()

    def unload_page(self):
        for obj in self.page_contents:
            obj.destroy()
        self.page_contents = []
        self.possible_cursor_positions = []
        self.options = []