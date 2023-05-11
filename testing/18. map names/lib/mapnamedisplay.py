from tkinter import *

class MapNameDisplay:
    def __init__(self, text, size, window, height):
        self.canvas = Canvas(window, width = 300, height = size + 16, bg='white')