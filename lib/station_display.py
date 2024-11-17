from tkinter import *
from lib.station import Station
from lib.helper import get_train_graphics, get_exit_directions
from lib.audio import AudioHandler

class StationDisplay:
    tabs = ['Passengers', 'Exit']
    def __init__(self, window: Tk, screen_width:int, screen_height:int, station: Station, points: int, unlocked_lines: list, bought:list, skin: str, audio: AudioHandler, space_function):
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
        self.mouse_positions = []
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
        self.c.bind_all('<Motion>', self.mouse_motion)
        self.click = self.c.bind('<Button-1>', self.mouse_click, add = True)

        self.compass_graphic = PhotoImage(file='./compass.png').zoom(3).subsample(2)
        self.pointer = None
        possible_pointers = get_train_graphics(skin, zoom = 2)
        self.pointer_graphics = [possible_pointers[dir] for dir in get_exit_directions(station)]

        window.update()

        self.audio = audio
        self.space_function = space_function
        


    def assemble_exit_page(self):
        for i in range(len(self.station.exits.keys())):
            exit_name = list(self.station.exits.keys())[i]
            location = ((self.space / len(self.station.exits.keys())) * (i + 0.5)) + 110
            self.page_contents.append(self.c.create_text((self.width/5)*4, location, fill='black', font='Arial 30', \
                    text=' '.join([word.capitalize() for word in exit_name.split(' ')]), anchor='e'))
            self.possible_cursor_positions.append(location)
            self.options.append(exit_name)
        self.cursor = self.c.create_image(self.width/4, self.possible_cursor_positions[0], image = self.cursor_graphic, anchor='center')
        
        self.page_contents.append(self.c.create_image(self.width - 10, self.height - 10, image = self.compass_graphic, anchor = 'se'))
        
        self.pointer = self.c.create_image(self.width - 122.5, self.height - 122.5, image = self.pointer_graphics[0])

        self.c.bind_all('<Up>',self.move_cursor_up)
        self.c.bind_all('<Down>', self.move_cursor_down)

        if len(self.possible_cursor_positions) > 1:
            mouse_offset = (self.possible_cursor_positions[1] - self.possible_cursor_positions[0])/2
            self.mouse_positions = [val + mouse_offset for val in self.possible_cursor_positions]
        else:
            self.mouse_positions = []

    

    def assemble_passenger_page(self):
        self.c.unbind_all('<Motion>')
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
            self.c.bind_all('<Motion>', self.mouse_motion)
            self.options = [self.passenger, 0]

            if len(self.possible_cursor_positions) > 1:
                mouse_offset = (self.possible_cursor_positions[1] - self.possible_cursor_positions[0])/2
                self.mouse_positions = [val + mouse_offset for val in self.possible_cursor_positions]
            else:
                self.mouse_positions = []


    def move_cursor_up(self, event):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.audio.play_sound_effect('scroll')
        if self.pointer != None:
            self.c.itemconfig(self.pointer, image = self.pointer_graphics[self.cursor_pos])
    
    def move_cursor_down(self, event):
        if self.cursor_pos + 1 < len(self.possible_cursor_positions):
            self.cursor_pos += 1
            self.audio.play_sound_effect('scroll')
        if self.pointer != None:
            self.c.itemconfig(self.pointer, image = self.pointer_graphics[self.cursor_pos])
    

    def switch_tab_left(self, event):
        if self.page > 0:
            self.c.itemconfig(self.tab_text[self.page], fill='black')
            self.page -= 1
            self.change_tab()
            self.audio.play_sound_effect('scroll')
    
    def switch_tab_right(self, event):
        if self.page + 1 < len(self.tabs):
            self.c.itemconfig(self.tab_text[self.page], fill='black')
            self.page += 1
            self.change_tab()
            self.audio.play_sound_effect('scroll')


    def update_cursor(self):
        self.c.coords(self.cursor, self.c.coords(self.cursor)[0], self.possible_cursor_positions[self.cursor_pos])

    def select_current(self):
        try:
            return [self.tabs[self.page], self.options[self.cursor_pos]]
        except IndexError:
            return [-1,-1]
    
    def close(self):
        self.c.unbind_all('<Motion>')
        self.c.unbind('<Button-1>', self.click)
        self.c.destroy()

    def unload_page(self):
        for obj in self.page_contents:
            self.c.delete(obj)
        self.page_contents = []
        self.possible_cursor_positions = []
        self.options = []
        try:
            self.c.delete(self.pointer)
        except:
            pass
        self.pointer = None

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
    
    def mouse_motion(self, event:Event):
        y = event.y_root
        if y > 140 and self.mouse_positions != []:
            selected = len(self.options) - 1
            for i in range(len(self.mouse_positions)):
                if y > self.mouse_positions[i]:
                    continue
                selected = i
                break
            if self.cursor_pos != selected:
                self.audio.play_sound_effect('scroll')
                self.cursor_pos = selected
                if self.pointer != None:
                    self.c.itemconfig(self.pointer, image = self.pointer_graphics[self.cursor_pos])
    
    def mouse_click(self, event: Event):
        x, y = event.x_root, event.y_root
        if y > 140:
            self.space_function(None)
        else:
            self.c.itemconfig(self.tab_text[self.page], fill='black')
            self.page = int(x // (self.width / len(self.tabs)))
            self.change_tab()