from tkinter import *
from lib.station import Station

class StationDisplay:
    tabs = ['Passengers', 'Exit']
    def __init__(self, window: Tk, screen_width:int, screen_height:int, station: Station, points: int, unlocked_lines: list, bought:list, skin: str):
        self.c = Canvas(window, width=screen_width, height=screen_height, bg='white')
        self.c.place(x=4,y=0)
        self.c.create_text(20,10,fill='black', font='Arial 40', text=station.name.replace('@', ' - '), anchor='nw')
        self.c.create_line(0,80,screen_width,80, fill='black')
        self.c.create_line(0,110,screen_width,110,fill='black')
        self.c.create_text(screen_width-25, 28, fill='black', font='Arial 24', text=f'Points: {points}', anchor='ne')

        # tabs at the top
        
        self.tab_text = [self.c.create_text((i*screen_width/len(self.tabs) + screen_width/(len(self.tabs) * 2)),95, fill='black', font='Arial 18', text=self.tabs[i], anchor='center') for i in range(len(self.tabs))]

        self.passenger = station.generate_passenger(unlocked_lines)

        self.unlocked = unlocked_lines
        self.bought = bought

        self.page_contents = []
        self.possible_cursor_positions = []
        self.space = screen_height - 110
        self.width = screen_width
        self.height = screen_height
        self.station = station

        self.cursor_graphic = PhotoImage(file=f'./skins/{skin}.png').zoom(3)
        self.cursor_pos = 0
        self.cursor = False

        self.options = []
        self.page = 0
        self.change_tab()

        self.c.bind_all('<Left>', self.switch_tab_left)
        self.c.bind_all('<Right>', self.switch_tab_right)

        window.update()

        


    def assemble_exit_page(self):
        for i in range(len(self.station.exits.keys())):
            exit_name = list(self.station.exits.keys())[i]
            location = ((self.space / len(self.station.exits.keys())) * (i + 0.5)) + 110
            self.page_contents.append(self.c.create_text((self.width/5)*4, location, fill='black', font='Arial 30', \
                    text=' '.join([word.capitalize() for word in exit_name.split(' ')]), anchor='e'))
            self.possible_cursor_positions.append(location)
            self.options.append(exit_name)
        self.cursor = self.c.create_image(self.width/4, self.possible_cursor_positions[0], image = self.cursor_graphic, anchor='center')
        self.c.bind_all('<Up>',self.move_cursor_up)
        self.c.bind_all('<Down>', self.move_cursor_down)
    

    def assemble_passenger_page(self):
        if self.passenger == 0:
            self.page_contents.append(self.c.create_text(self.width/2, ((self.height-110)/2)+110, fill='black', font='Arial 20', text='There are currently no passengers at this station.', width=self.width - 100, anchor='center'))
        
        elif self.passenger == 1:
            self.page_contents.append(self.c.create_text(self.width/2, ((self.height-110)/2)+110, fill='black', font='Arial 20', text='The passenger has gone home...', width=self.width - 100, anchor='center'))
        
        elif self.passenger == 2:
            self.page_contents.append(self.c.create_text(self.width/2, ((self.height-110)/2)+110, fill='black', font='Arial 20', text='Passenger collected!', width=self.width - 100, anchor='center'))

        elif self.passenger == 3:
            self.page_contents.append(self.c.create_text(self.width/2, ((self.height-110)/2)+110, fill='black', font='Arial 20', text='Your train is already full!', width=self.width - 100, anchor='center'))

        else:
            station_name = self.passenger['station'].split('/')[1]
            reward = self.passenger['reward']
            self.page_contents.extend([
self.c.create_text(self.width/2, ((self.height-110)/6)+110, fill='black', font='Arial 25', text='New Passenger!', anchor='center'),
self.c.create_text(self.width/2, ((self.height-110)/2)+95, fill='black', font='Arial 18', text=f'Destination:  {station_name}', anchor='center'),
self.c.create_text(self.width/2, ((self.height-110)/2)+125, fill='black', font='Arial 18', text=f'Points:  {reward}', anchor='center'),
self.c.create_text(self.width/2, (5*(self.height-110)/6)+60, fill='black', font='Arial 18', text=f'Do you accept?', anchor='center'),
self.c.create_text(5*self.width/8, (5*(self.height-110)/6)+95, fill='black', font='Arial 25', text='Yes', anchor='center'),
self.c.create_text(5*self.width/8, (5*(self.height-110)/6)+125, fill='black', font='Arial 25', text='No', anchor='center')
            ])
            self.possible_cursor_positions = [(5*(self.height-110)/6)+95, (5*(self.height-110)/6)+125]
            self.cursor = self.c.create_image(3*self.width/8, self.possible_cursor_positions[0], image = self.cursor_graphic, anchor='center')
            self.c.bind_all('<Up>',self.move_cursor_up)
            self.c.bind_all('<Down>', self.move_cursor_down)
            self.options = [self.passenger, 0]


    def move_cursor_up(self, event):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
    
    def move_cursor_down(self, event):
        if self.cursor_pos + 1 < len(self.possible_cursor_positions):
            self.cursor_pos += 1
    

    def switch_tab_left(self, event):
        if self.page > 0:
            self.c.itemconfig(self.tab_text[self.page], fill='black')
            self.page -= 1
            self.change_tab()
    
    def switch_tab_right(self, event):
        if self.page + 1 < len(self.tabs):
            self.c.itemconfig(self.tab_text[self.page], fill='black')
            self.page += 1
            self.change_tab()


    def update_cursor(self):
        self.c.coords(self.cursor, self.c.coords(self.cursor)[0], self.possible_cursor_positions[self.cursor_pos])

    def select_current(self):
        try:
            return [self.tabs[self.page], self.options[self.cursor_pos]]
        except IndexError:
            return [-1,-1]
    
    def close(self):
        self.c.destroy()

    def unload_page(self):
        for obj in self.page_contents:
            self.c.delete(obj)
        self.page_contents = []
        self.possible_cursor_positions = []
        self.options = []

    def change_tab(self):
        if self.cursor:
            self.c.delete(self.cursor)
            self.cursor = False
            self.c.unbind_all('<Up>')
            self.c.unbind_all('<Down>')
        self.unload_page()
        self.cursor_pos = 0
        self.options = []
        self.possible_cursor_positions = []

        match self.tabs[self.page]:
            case 'Passengers': self.assemble_passenger_page()
            case 'Exit': self.assemble_exit_page()
            case 'Shop': self.assemble_shop_page()

        self.c.itemconfig(self.tab_text[self.page], fill='blue')