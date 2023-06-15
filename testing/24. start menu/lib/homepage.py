from tkinter import *
from json import loads

class Homepage:
    def __init__(self, window, width, height):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        self.name = self.c.create_text(width/2, height/3, fill='black', font='Arial 30', text='Unnamed Train Game', anchor='center')

        self.newgame = self.c.create_text((width/2)+5, (2*height/3)-15, fill='black', font='Arial 20', text='New Game', anchor='w')
        self.cont_text = self.c.create_text((width/2)+5, (2*height/3)+10, fill='black', font='Arial 20', text='Continue', anchor='w')

        self.cursor_positions = [(2*height/3)-15, (2*height/3)+10]
        self.selected = 0
        self.options = ['New Game', 'Continue']

        self.space_pressed = False
        self.c.bind_all('<space>', self.press_space)

        self.cursor_image = PhotoImage(file='./graphics/train4.png')
        self.cursor = self.c.create_image((width/2)-15, (2*height/3)-15, anchor='e', image=self.cursor_image)
        self.c.bind_all('<Up>', self.move_cursor_up)
        self.c.bind_all('<Down>', self.move_cursor_down)

        

    def press_space(self, event):
        self.space_pressed = True

    def move_cursor_up(self, event):
        if self.selected > 0:
            self.selected -= 1
    
    def move_cursor_down(self, event):
        if self.selected + 1 < len(self.cursor_positions):
            self.selected += 1

    def update_cursor(self):
        self.c.coords(self.cursor, self.c.coords(self.cursor)[0], self.cursor_positions[self.selected])
    
    def get_choice(self):
        return self.options[self.selected]
    

    def remove(self):
        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.c.unbind_all('<space>')
        self.c.destroy()