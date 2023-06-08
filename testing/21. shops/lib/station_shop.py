from lib.station_display import StationDisplay
from lib.station import Station
from tkinter import *

# version of station display with a shop
class ShopStation(StationDisplay):
    tabs = ['Shop','Passengers', 'Exit']

    def assemble_shop_page(self):
        self.options = list(self.station.shop.keys())