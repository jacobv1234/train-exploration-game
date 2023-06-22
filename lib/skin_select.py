from tkinter import *

# skin selection window
class SkinSelect:
    def __init__(self, window, width, height):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        with open('./skins.txt', 'r') as f:
            self.options = [skin[:-1] for skin in f.readlines()]
        self.pos = 0
        self.display_text = self.c.create_text(width/2, 2*height/3, fill='black', font='Arial 20', text=f'{self.options[0]}>', anchor='center')
        self.space_pressed = False

        self.c.create_text(width/2, height/4, fill='black', font='Arial 30', text='Choose your skin:', anchor='center')

        self.images = [PhotoImage(file=f'./skins/{skin}.png') for skin in self.options]

        self.images = [i.zoom(3) for i in self.images]

        self.display = self.c.create_image(width/2,height/2,image=self.images[0], anchor='center')

        self.c.bind_all('<Left>', self.scroll_left)
        self.c.bind_all('<Right>', self.scroll_right)
        self.c.bind_all('<space>', self.press_space)
    
    def scroll_right(self, event):
        if self.pos + 1 < len(self.options):
            self.pos += 1
        
        if self.pos + 1 == len(self.options):
            ending = ''
        else:
            ending = '>'
        
        self.c.itemconfig(self.display, image=self.images[self.pos])
        self.c.itemconfig(self.display_text, text=f'<{self.options[self.pos]}{ending}')

    def scroll_left(self, event):
        if self.pos > 0:
            self.pos -= 1
        
        if self.pos == 0:
            start = ''
        else:
            start = '<'
        
        self.c.itemconfig(self.display, image=self.images[self.pos])
        self.c.itemconfig(self.display_text, text=f'{start}{self.options[self.pos]}>')

    def press_space(self, event):
        self.space_pressed = True

    def get_selected(self):
        return self.options[self.pos]
    
    def remove(self):
        self.c.unbind_all('<Left>')
        self.c.unbind_all('<Right>')
        self.c.unbind_all('<space>')
        self.c.destroy()