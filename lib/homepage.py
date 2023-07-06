from tkinter import *
from json import loads

class Homepage:
    def __init__(self, window, width, height, skin):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        self.name = self.c.create_text(width/2, height/3, fill='black', font='Arial 30', text='Untitled Train Game', anchor='center')
        self.author = self.c.create_text(width/2, (height/3)+30, fill='black', font='Arial 10', text='By Jacob Vincent', anchor='center')

        self.newgame = self.c.create_text((width/2)+5, (2*height/3)-15, fill='black', font='Arial 20', text='New Game', anchor='w')
        self.cont_text = self.c.create_text((width/2)+5, (2*height/3)+10, fill='black', font='Arial 20', text='Continue', anchor='w')

        self.cursor_positions = [(2*height/3)-15, (2*height/3)+10]
        self.selected = 0
        self.options = ['New Game', 'Continue']

        self.space_pressed = False
        self.c.bind_all('<space>', self.press_space)

        self.cursor_image = PhotoImage(file=f'./skins/{skin}.png')
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

    
    def save_selection(self, map_manifest, width, height):
        self.c.delete(self.name, self.newgame, self.cont_text, self.cursor, self.author)

        names = list(map_manifest['Saves'].keys())

        self.cursor_positions = []
        self.selected = 0
        self.options = []

        mapname = map_manifest['Name']
        self.c.create_text(width/2, 20, fill='black', font='Arial 30', text='Choose your mode:', anchor='center')
        self.c.create_text(width/2, 53, fill='black', font='Arial 15', text=f'Map: {mapname}', anchor='center')

        for i in range(len(names) + 1):
            if i != len(names):
                option_name = names[i]
                option_desc = map_manifest['Saves'][option_name]['desc']
                self.options.append(map_manifest['Saves'][option_name]['path'])
            else:
                option_name = 'Back'
                option_desc = ''
                self.options.append('Back')
            
            pos = (((height-60)/(len(names)+2)) + 60) * (i + 1)
            self.cursor_positions.append(pos)
            
            self.c.create_text(width/2, pos, fill='black', font='Arial 20', text=option_name, anchor='center')
            self.c.create_text(3*width/4, pos, fill='black', font='Arial 15', text=option_desc, anchor='center', width=width/4.5)
        
        self.cursor_image.zoom(2)
        self.cursor = self.c.create_image((width/4), self.cursor_positions[0], anchor='center', image=self.cursor_image)