from tkinter import *
from lib.map import Map
from lib.helper import get_line_poly_coords


class ZoomedMap:
    def __init__(self, window: Tk, width: int, height: int, map: Map, train_x: int, train_y: int, water_coords: list, scroll: dict):
        self.c = Canvas(window, width=width, height=height, bg='lightblue', xscrollincrement=1, yscrollincrement=1)
        self.c.place(x=4,y=0)
        water_coords = [coord // 4 for coord in water_coords]
        self.water = self.c.create_polygon(water_coords, fill='white', outline='')
        self.station_name_popup = self.c.create_text(width/2,50,fill='black', font='Arial 25', text='', anchor='n')
        self.stations = []
        self.limits = scroll


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
        
        self.c.create_oval(train_x//4 - 10,train_y//4 - 10,train_x//4 + 10,train_y//4 + 10,fill='', outline='red')
        
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

        self.screen_left = (train_x // 4) - (width//2)
        self.screen_right = (train_x // 4) + (width//2)
        self.screen_top = (train_y // 4) - (height//2)
        self.screen_bottom = (train_y // 4) + (height//2)

        # scroll to be within limits
        self.scroll_into_bounds()

        self.c.tag_raise(self.station_name_popup)
        self.c.tag_lower(self.water)
    
    def scroll_left(self,event):
        if self.screen_left > self.limits['left']:
            self.c.xview_scroll(-40, 'units')
            self.c.move(self.station_name_popup,-40,0)
            self.screen_left -= 40
            self.screen_right -= 40
        
    def scroll_right(self,event):
        if self.screen_right < self.limits['right']:
            self.c.xview_scroll(40,'units')
            self.c.move(self.station_name_popup,40,0)
            self.screen_left += 40
            self.screen_right += 40

    def scroll_up(self,event):
        if self.screen_top > self.limits['top']:
            self.c.yview_scroll(-40, 'units')
            self.c.move(self.station_name_popup,0,-40)
            self.screen_top -= 40
            self.screen_bottom -= 40
    
    def scroll_down(self,event):
        if self.screen_bottom < self.limits['bottom']:
            self.c.yview_scroll(40,'units')
            self.c.move(self.station_name_popup,0,40)
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
        for station in self.stations:
            if int(x) in range(station[0]-12, station[0]+12) and int(y) in range(station[1]-12, station[1]+12):
                message = station[2]
                if '@' in message:
                    index = message.index('@')
                    message = message[:index]
                self.c.itemconfig(self.station_name_popup, text=message)
                break
            else:
                self.c.itemconfig(self.station_name_popup, text='')
    
    def scroll_into_bounds(self):
        if self.screen_left < self.limits['left']:
            difference = self.limits['left'] - self.screen_left 
            self.c.xview_scroll(difference, 'units')
            self.c.move(self.station_name_popup,difference,0)
            self.screen_left += difference
            self.screen_right += difference

        elif self.screen_right > self.limits['right']:
            difference = self.limits['right'] - self.screen_right
            self.c.xview_scroll(difference, 'units')
            self.c.move(self.station_name_popup,difference,0)
            self.screen_left += difference
            self.screen_right += difference
        

        if self.screen_bottom > self.limits['bottom']:
            difference = self.limits['bottom'] - self.screen_bottom
            self.c.yview_scroll(difference,'units')
            self.c.move(self.station_name_popup,0,difference)
            self.screen_top += difference
            self.screen_bottom += difference

        elif self.screen_top < self.limits['top']:
            difference = self.limits['top'] - self.screen_top
            self.c.yview_scroll(difference,'units')
            self.c.move(self.station_name_popup,0,difference)
            self.screen_top += difference
            self.screen_bottom += difference
