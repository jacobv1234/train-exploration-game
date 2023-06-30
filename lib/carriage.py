from tkinter import *
from lib.train import Train
from lib.helper import get_train_graphics
class Carriage:
    def __init__(self, skin: str, train: Train, c: Canvas):
        self.images = get_train_graphics(f'{skin}_carriage')
        self.object = c.create_image(train.last_positions[-7][0], train.last_positions[-7][0], image=self.images[train.last_positions[-7][2]])