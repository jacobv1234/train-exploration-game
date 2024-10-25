from tkinter import *
from lib.audio import AudioHandler

# skin selection window
class SkinSelect:
    def __init__(self, window, width, height, audio: AudioHandler):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        with open('./skins.txt', 'r') as f:
            self.options = [skin[:-1] for skin in f.readlines()]
        self.pos = 0
        self.display_text = self.c.create_text(width/2, 2*height/3, fill='black', font='Arial 20', text=f'{self.options[0]}', anchor='center')
        self.space_pressed = False

        self.c.create_text(width/2, height/4, fill='black', font='Arial 30', text='Choose your skin:', anchor='center')

        self.images = [PhotoImage(file=f'./skins/{skin}.png') for skin in self.options]

        self.images = [i.zoom(3) for i in self.images]

        self.display = self.c.create_image(width/2,height/2,image=self.images[0], anchor='center')

        self.left = self.c.create_text(width/3, 2*height/3, fill='black', font = 'Arial 20', text = '<', anchor='center')
        self.right = self.c.create_text(2*width/3, 2*height/3, fill='black', font = 'Arial 20', text = '>', anchor='center')
        self.c.itemconfig(self.left, state='hidden')

        self.c.bind_all('<Left>', self.scroll_left)
        self.c.bind_all('<Right>', self.scroll_right)
        self.c.bind_all('<space>', self.press_space)
        self.c.bind_all('<Button-1>', self.track_mouse)

        self.audio = audio

        self.width = width
    
    def scroll_right(self, event):
        if self.pos + 1 < len(self.options):
            self.pos += 1
            self.audio.play_sound_effect('scroll')
        
        if self.pos + 1 == len(self.options):
            self.c.itemconfig(self.right, state='hidden')
        else:
            self.c.itemconfig(self.right, state='normal')
        
        self.c.itemconfig(self.left, state='normal')
        
        self.c.itemconfig(self.display, image=self.images[self.pos])
        self.c.itemconfig(self.display_text, text=self.options[self.pos])

    def scroll_left(self, event):
        if self.pos > 0:
            self.pos -= 1
            self.audio.play_sound_effect('scroll')
        
        if self.pos == 0:
            self.c.itemconfig(self.left, state='hidden')
        else:
            self.c.itemconfig(self.left, state='normal')

        self.c.itemconfig(self.right, state='normal')
        
        self.c.itemconfig(self.display, image=self.images[self.pos])
        self.c.itemconfig(self.display_text, text=self.options[self.pos])

    def press_space(self, event):
        self.audio.play_sound_effect('select')
        self.space_pressed = True

    def get_selected(self):
        return self.options[self.pos]
    
    def remove(self):
        self.c.unbind_all('<Left>')
        self.c.unbind_all('<Right>')
        self.c.unbind_all('<space>')
        self.c.unbind_all('<Button-1>')
        self.c.destroy()
    
    def track_mouse(self, event: Event):
        x, y = (event.x_root, event.y_root)
        if x < self.width * 0.4:
            self.scroll_left(None)
        elif x > self.width * 0.6:
            self.scroll_right(None)
        else:
            self.press_space(None)