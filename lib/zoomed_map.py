from tkinter import *
from lib.map import Map
from lib.helper import get_line_poly_coords, get_complete_percent
from lib.passengers import Passengers
from json import loads
from lib.audio import AudioHandler


class ZoomedMap:
    def __init__(self, window: Tk, width: int, height: int, map: Map, train_x: int, train_y: int, water_coords: list, scroll: dict, passengers = False, audio: AudioHandler = None):
        self.c = Canvas(window, width=width, height=height, bg='lightblue', xscrollincrement=1, yscrollincrement=1)
        self.c.place(x=4,y=0)
        water_coords = [coord // 4 for coord in water_coords]
        self.water = self.c.create_polygon(water_coords, fill='white', outline='')
        self.station_name_popup = self.c.create_text(width/2,50,fill='black', font='Arial 25', text='', anchor='n')

        # get the maximum number of lines in a map
        complete_percent = get_complete_percent(map)
        self.complete_message = self.c.create_text(width - 50, height - 50, fill='black', font = 'Arial 20', text = f'Routes unlocked in this area: {complete_percent}%', anchor = 'se')
        
        self.stations = []
        self.limits = scroll
        self.audio = audio
        self.played_click = False
        self.width = width
        self.height = height


        for group_name in list(map.station_groups.keys()):
            group = map.station_groups[group_name]
            for line in group.created:
                self.c.create_line(line[0]//4, line[1]//4, line[2]//4, line[3]//4, fill='black')


        for line_name in list(map.lines.keys()):
            line = map.lines[line_name]
            col = line.col
            for s in line.seg_coords:
                s = [i / 4 for i in s]
                obj = self.c.create_polygon(get_line_poly_coords(s, radius=1.5), fill=col)
                self.c.tag_lower(obj)
            
            if line_name[0] != '_':
                for s in line.stations:
                    self.stations.append([s.pos[0]//4,s.pos[1]//4, s.name])
                    self.c.create_oval(s.pos[0]//4 - 5, s.pos[1]//4 - 5, s.pos[0]//4 + 5, s.pos[1]//4 + 5, outline='black', fill='white')


        # create markers for passengers
        if passengers:
            for passenger in passengers.passengers:
                station_map, name = tuple(passenger['station'].split('/'))
                if station_map == map.internal_name:
                    try:
                        self.create_passenger_marker(station_map, name)
                    except FileNotFoundError:
                        stations = []
                        try:
                            with open(f'./map/{station_map}/station_groups/{name}.json', 'r') as f:
                                stations = loads(f.read())['stations']
                            for station in stations:
                                self.create_passenger_marker(station_map, station)
                        except FileNotFoundError:
                            # station is part of group that does not exist yet
                            # find the missing suffix
                            lines = passenger['line']
                            for line in lines:
                                stations_on_line = map.lines[line.split('/')[1]].stations
                                for station in stations:
                                    if station.split('@')[0] == name:
                                        self.create_passenger_marker(station_map, station)

        
        
        self.c.create_oval(train_x//4 - 12,train_y//4 - 12,train_x//4 + 12,train_y//4 + 12,fill='', outline='red', width = 2)
        self.c.create_oval(train_x//4 - 8,train_y//4 - 8,train_x//4 + 8,train_y//4 + 8,fill='', outline='red', width = 2)
        
        self.c.bind_all('<Left>', self.scroll_left)
        self.c.bind_all('<Right>', self.scroll_right)
        self.c.bind_all('<Up>', self.scroll_up)
        self.c.bind_all('<Down>', self.scroll_down)
        self.c.bind_all('<Motion>', self.track_motion)

        self.c.xview_scroll(-width//2,'units')
        self.c.yview_scroll(-height//2, 'units')
        self.c.xview_scroll(train_x//4, 'units')
        self.c.yview_scroll(train_y//4, 'units')
        self.c.move(self.station_name_popup,-width//2,-height//2)
        self.c.move(self.station_name_popup,train_x//4,train_y//4)
        self.c.move(self.complete_message,-width//2,-height//2)
        self.c.move(self.complete_message,train_x//4,train_y//4)

        self.screen_left = (train_x // 4) - (width//2)
        self.screen_right = (train_x // 4) + (width//2)
        self.screen_top = (train_y // 4) - (height//2)
        self.screen_bottom = (train_y // 4) + (height//2)

        # scroll to be within limits
        self.scroll_into_bounds()

        self.c.tag_raise(self.station_name_popup)
        self.c.tag_raise(self.complete_message)
        self.c.tag_lower(self.water)

    
    def scroll_left(self,event):
        if self.screen_left > self.limits['left']:
            self.c.xview_scroll(-40, 'units')
            self.c.move(self.station_name_popup,-40,0)
            self.c.move(self.complete_message, -40,0)
            self.screen_left -= 40
            self.screen_right -= 40
        
    def scroll_right(self,event):
        if self.screen_right < self.limits['right']:
            self.c.xview_scroll(40,'units')
            self.c.move(self.station_name_popup,40,0)
            self.c.move(self.complete_message, 40,0)
            self.screen_left += 40
            self.screen_right += 40

    def scroll_up(self,event):
        if self.screen_top > self.limits['top']:
            self.c.yview_scroll(-40, 'units')
            self.c.move(self.station_name_popup,0,-40)
            self.c.move(self.complete_message, 0, -40)
            self.screen_top -= 40
            self.screen_bottom -= 40
    
    def scroll_down(self,event):
        if self.screen_bottom < self.limits['bottom']:
            self.c.yview_scroll(40,'units')
            self.c.move(self.station_name_popup,0,40)
            self.c.move(self.complete_message, 0, 40)
            self.screen_top += 40
            self.screen_bottom += 40
    
    def close(self):
        self.c.unbind_all('<Left>')
        self.c.unbind_all('<Right>')
        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.c.unbind_all('<Motion>')
        self.c.destroy()

    def track_motion(self, event: Event):
        x,y = self.c.canvasx(event.x), self.c.canvasy(event.y)

        if event.x < 20:
            self.scroll_left(None)
            return
        if event.x > self.width - 20:
            self.scroll_right(None)
            return
        if event.y < 20:
            self.scroll_up(None)
            return
        if event.y > self.height - 20:
            self.scroll_down(None)
            return

        for station in self.stations:
            if int(x) in range(station[0]-12, station[0]+12) and int(y) in range(station[1]-12, station[1]+12):

                if self.played_click == False:
                    self.played_click = True
                    self.audio.play_sound_effect('select')

                message = station[2]
                if '@' in message:
                    index = message.index('@')
                    message = message[:index]
                self.c.itemconfig(self.station_name_popup, text=message)
                return
        self.c.itemconfig(self.station_name_popup, text='')
        self.played_click = False
    
    def scroll_into_bounds(self):
        if self.screen_left < self.limits['left']:
            difference = self.limits['left'] - self.screen_left 
            self.c.xview_scroll(difference, 'units')
            self.c.move(self.station_name_popup,difference,0)
            self.c.move(self.complete_message, difference,0)
            self.screen_left += difference
            self.screen_right += difference

        elif self.screen_right > self.limits['right']:
            difference = self.limits['right'] - self.screen_right
            self.c.xview_scroll(difference, 'units')
            self.c.move(self.station_name_popup,difference,0)
            self.c.move(self.complete_message, difference,0)
            self.screen_left += difference
            self.screen_right += difference
        

        if self.screen_bottom > self.limits['bottom']:
            difference = self.limits['bottom'] - self.screen_bottom
            self.c.yview_scroll(difference,'units')
            self.c.move(self.station_name_popup,0,difference)
            self.c.move(self.complete_message,0,difference)
            self.screen_top += difference
            self.screen_bottom += difference

        elif self.screen_top < self.limits['top']:
            difference = self.limits['top'] - self.screen_top
            self.c.yview_scroll(difference,'units')
            self.c.move(self.station_name_popup,0,difference)
            self.c.move(self.complete_message,0,difference)
            self.screen_top += difference
            self.screen_bottom += difference


    def create_passenger_marker(self, station_map, name):
        with open(f'./map/{station_map}/stations/{name}.json', 'r') as f:
            station_coords = loads(f.read())['position']
            x = station_coords[0] // 4
            y = station_coords[1] // 4
            self.c.create_oval(x - 10, y - 10, x + 10, y + 10, fill = '', outline = '#2eebaf', width = 2)