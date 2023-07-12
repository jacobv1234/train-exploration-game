from tkinter import *
from lib.map import Map


class ZoomedMap:
    def __init__(self, window: Tk, width: int, height: int, map: Map, train_x: int, train_y: int):
        self.c = Canvas(window, width=width, height=height, bg='white', xscrollincrement=1, yscrollincrement=1)
        self.c.place(x=4,y=0)
        self.station_name_popup = self.c.create_text(width/2,50,fill='black', font='Arial 20', text='', anchor='n')
        self.stations = []
        for line_name in list(map.lines.keys()):
            line = map.lines[line_name]
            col = line.col
            for s in line.seg_coords:
                self.c.create_line(s[0]//8,s[1]//8,s[2]//8,s[3]//8, fill=col)
            
            for s in line.stations:
                self.stations.append([s.pos[0]//8,s.pos[1]//8, s.name])
                self.c.create_oval(s.pos[0]//8 - 2, s.pos[1]//8 - 2, s.pos[0]//8 + 2, s.pos[1]//8 + 2, outline='black')
        
        self.c.create_oval(train_x//8 - 4,train_y//8 - 4,train_x//8 + 4,train_y//8 + 4,fill='', outline='red')
        
        self.c.bind_all('<Left>', self.scroll_left)
        self.c.bind_all('<Right>', self.scroll_right)
        self.c.bind_all('<Up>', self.scroll_up)
        self.c.bind_all('<Down>', self.scroll_down)
        self.c.bind_all('<Motion>', self.track_motion)

        self.c.xview_scroll(-width//2,'units')
        self.c.yview_scroll(-height//2, 'units')
        self.c.xview_scroll(train_x//8, 'units')
        self.c.yview_scroll(train_y//8, 'units')
        self.c.move(self.station_name_popup,-width//2,-height//2)
        self.c.move(self.station_name_popup,train_x//8,train_y//8)
    
    def scroll_left(self,event):
        self.c.xview_scroll(-40, 'units')
        self.c.move(self.station_name_popup,-40,0)
    
    def scroll_right(self,event):
        self.c.xview_scroll(40,'units')
        self.c.move(self.station_name_popup,40,0)
    
    def scroll_up(self,event):
        self.c.yview_scroll(-40, 'units')
        self.c.move(self.station_name_popup,0,-40)
    
    def scroll_down(self,event):
        self.c.yview_scroll(40,'units')
        self.c.move(self.station_name_popup,0,40)
    
    def close(self):
        self.c.unbind_all('<Left>')
        self.c.unbind_all('<Right>')
        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.c.destroy()

    def track_motion(self, event: Event):
        x,y = self.c.canvasx(event.x), self.c.canvasy(event.y)
        for station in self.stations:
            if int(x) in range(station[0]-4, station[0]+5) and int(y) in range(station[1]-4, station[1]+5):
                self.c.itemconfig(self.station_name_popup, text=station[2])
                break
            else:
                self.c.itemconfig(self.station_name_popup, text='')
