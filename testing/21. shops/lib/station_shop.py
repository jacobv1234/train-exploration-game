from lib.station_display import StationDisplay
from lib.station import Station
from tkinter import *
from lib.helper import test_requirements, get_unlocked_lines

# version of station display with a shop
class ShopStation(StationDisplay):
    tabs = ['Shop','Passengers', 'Exit']

    def assemble_shop_page(self):
        self.options = [option for option in list(self.station.shop.keys()) if (test_requirements(self.station.shop[option]['requirements'], self.unlocked)) and self.station.shop[option]['unique_name'] not in self.bought]
        if self.options != []:
            self.page_contents.extend([
self.c.create_text(self.width/2, 130, fill='black', font='Arial 20', text='New area', anchor = 'center'),
self.c.create_text(self.width*3/4, 130, fill='black', font='Arial 14', text='Price')
            ])
            for i in range(len(self.options)):
                option = self.options[i]
                shop_item = self.station.shop[option]
                pos = 150 + ((i+0.5)*(self.height - 150) / len(self.options))
                self.possible_cursor_positions.append(pos)
                self.page_contents.extend([
self.c.create_text(self.width/2, pos, fill='black', font='Arial 14', text=option, anchor='center'),
self.c.create_text(self.width*3/4, pos, fill='black', font='Arial 14', text=shop_item['cost'])
                ])
            
            self.cursor = self.c.create_image(self.width/4, self.possible_cursor_positions[0], image = self.cursor_graphic, anchor='center')
            self.c.bind_all('<Up>',self.move_cursor_up)
            self.c.bind_all('<Down>', self.move_cursor_down)
        
        else:
            self.page_contents.append(
                self.c.create_text(self.width/2, ((self.height-110)/2)+110, fill='black', font='Arial 18', text='There\'s nothing left in the shop!', anchor='center')
            )