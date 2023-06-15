from tkinter import *

class Homepage:
    def __init__(self, window, width, height):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        self.name = self.c.create_text(width/2, height/3, fill='black', font='Arial 30', text='Unnamed Train Game', anchor='center')

        self.newgame = self.c.create_text((width/2)+5, (2*height/3)-15, fill='black', font='Arial 20', text='New Game', anchor='w')
        self.cont_text = self.c.create_text((width/2)+5, (2*height/3)+10, fill='black', font='Arial 20', text='Continue', anchor='w')

        self.cursor_positions = [(2*height/3)-15, (2*height/3)+10]
        self.selected = 0

        self.space_pressed = False
        self.c.bind_all('<Space>', self.press_space)

        self.cursor_image = PhotoImage(file='/graphics/train4.png')
        self.cursor = self.c.create_image((width/2)-5, (2*height/3)-15, anchor='e', image=self.cursor_image)

    def press_space(self, event):
        self.space_pressed = True