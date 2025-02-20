from tkinter import *
from json import loads
from lib.map import Map
from PIL import Image, ImageTk
from lib.audio import AudioHandler

class Homepage:
    def __init__(self, window, width, height, skin, audio: AudioHandler):
        self.c = Canvas(window, width=width, height=height, bg='white')
        self.c.place(x=4,y=0)
        self.create_homepage(width,height,skin)
        self.width = width
        self.height = height
        self.audio = audio
        self.allow_cursor = True
        self.music_slider = False

    def press_space(self, event):
        self.audio.play_sound_effect('select')
        self.space_pressed = True

    def move_cursor_up(self, event):
        if self.selected > 0:
            self.audio.play_sound_effect('scroll')
            self.selected -= 1
    
    def move_cursor_down(self, event):
        if self.selected + 1 < len(self.cursor_positions):
            self.audio.play_sound_effect('scroll')
            self.selected += 1

    def update_cursor(self):
        if self.allow_cursor:
            self.c.coords(self.cursor, self.c.coords(self.cursor)[0], self.cursor_positions[self.selected])
    
    def get_choice(self):
        return self.options[self.selected]
    

    def remove(self):
        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.c.unbind_all('<space>')
        self.c.unbind_all('<Button-1>')
        self.c.unbind_all('<Motion>')
        self.c.destroy()

    
    def save_selection(self, map_manifest, width, height):
        self.c.delete(self.logo, self.newgame, self.cont_text, self.cursor, self.howtoplay, self.audio_settings)

        names = list(map_manifest['Saves'].keys())

        self.cursor_positions = []
        self.mouse_positions = []
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
            
            pos = (((height-60)/(len(names)*2)) + 60) * (i + 1)
            self.cursor_positions.append(pos)
            
            self.c.create_text(width/2, pos, fill='black', font='Arial 20', text=option_name, anchor='center')
            self.c.create_text(3*width/4, pos, fill='black', font='Arial 15', text=option_desc, anchor='center', width=width/4.5)
        
        self.cursor_image.zoom(2)
        self.cursor = self.c.create_image((width/4), self.cursor_positions[0], anchor='center', image=self.cursor_image)

        mouse_offset = (self.cursor_positions[1] - self.cursor_positions[0]) / 2
        self.mouse_positions = [val + mouse_offset for val in self.cursor_positions]
    
    def create_homepage(self, width, height, skin):
        # background
        with Image.open('menu_background.png') as im:
            im = im.resize([width,height])
            self.background = ImageTk.PhotoImage(im)
        self.c.create_image(0,0,image=self.background,anchor='nw')

        # logo
        with Image.open('logo.png') as im:
            im = im.resize([672,250])
            self.logo_img = ImageTk.PhotoImage(im)
        self.logo = self.c.create_image(width/2,height/2 - 100,image=self.logo_img,anchor='center')

        self.newgame = self.c.create_text((width/2)-15, (2*height/3)-15, fill='black', font='Arial 20', text='New Game', anchor='w')
        self.cont_text = self.c.create_text((width/2)-15, (2*height/3)+10, fill='black', font='Arial 20', text='Continue', anchor='w')
        self.howtoplay = self.c.create_text((width/2)-15, (2*height/3)+35, fill='black', font='Arial 20', text='How to Play', anchor='w')
        self.audio_settings = self.c.create_text((width/2)-15, (2*height/3)+60, fill='black', font='Arial 20', text='Audio Settings', anchor='w')

        self.sound_license = self.c.create_text(10, height - 10, fill='black', font = 'Arial 8', text = 'Sounds licensed for free from zapsplat.com', anchor='sw')

        self.cursor_positions = [(2*height/3)-15, (2*height/3)+10, (2*height/3)+35, (2*height/3)+60]
        self.selected = 0
        self.options = ['New Game', 'Continue', 'How to Play', 'Audio Settings']

        self.space_pressed = False
        self.c.bind_all('<space>', self.press_space)
        self.c.bind_all('<Button-1>', self.press_space)

        self.cursor_image = PhotoImage(file=f'./skins/{skin}.png')
        self.cursor = self.c.create_image((width/2)-35, (2*height/3)-15, anchor='e', image=self.cursor_image)
        self.c.bind_all('<Up>', self.move_cursor_up)
        self.c.bind_all('<Down>', self.move_cursor_down)

        self.c.bind_all('<Motion>', self.track_mouse)
        self.mouse_positions = [val + 10 for val in self.cursor_positions]

    
    def go_to_how_to_play(self):
        self.c.delete(self.logo, self.newgame, self.cont_text, self.cursor, self.howtoplay, self.audio_settings, self.sound_license)

        self.c.create_text(self.width/2, 10, fill='black', font='Arial 25', text='How to Play',anchor='n')

        with open('./howtoplay.txt','r') as f:
            text = f.read()

        self.c.create_text(self.width/2, self.height/2, fill='black',font='Arial 15', text=text, width=4*self.width/5, anchor='center', justify='center')

        self.options = ['Back']
        self.selected = 0

        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.allow_cursor = False

    def open_audio_settings(self, window:Tk, music_volume,sound_volume,train_volume):
        self.c.delete(self.logo, self.newgame, self.cont_text, self.cursor, self.howtoplay, self.audio_settings, self.sound_license)

        self.music_slider = Scale(window, from_= 0, to = 100, orient='horizontal')
        self.music_slider.place(relx=0.4, rely=0.3, relwidth=0.4, relheight=0.05, anchor = 'w')
        self.music_slider.set(music_volume*100)
        self.c.create_text(self.width * 0.35, self.height * 0.3, fill = 'black', font = 'Arial 15', text = 'Music:', anchor = 'e')

        self.sound_slider = Scale(window, from_= 0, to = 100, orient='horizontal')
        self.sound_slider.place(relx=0.4, rely=0.45, relwidth=0.4, relheight=0.05, anchor = 'w')
        self.sound_slider.set(sound_volume*100)
        self.c.create_text(self.width * 0.35, self.height * 0.45, fill = 'black', font = 'Arial 15', text = 'Sounds:', anchor = 'e')

        self.train_slider = Scale(window, from_= 0, to = 100, orient='horizontal')
        self.train_slider.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.05, anchor = 'w')
        self.train_slider.set(train_volume*100)
        self.c.create_text(self.width * 0.35, self.height * 0.6, fill = 'black', font = 'Arial 15', text = 'Train rumbles:', anchor = 'e')

        self.c.create_text(self.width * 0.48, self.height * 0.75, fill = 'black', font = 'Arial 15', text = 'SAVE AND CLOSE', anchor = 'w')
        self.c.create_image(self.width * 0.47, self.height * 0.75, image = self.cursor_image, anchor = 'e')


        self.options = ['Close Audio Settings']
        self.selected = 0
        self.c.unbind_all('<Up>')
        self.c.unbind_all('<Down>')
        self.allow_cursor = False
    
    def track_mouse(self, event: Event):
        y = self.c.canvasy(event.y)

        if self.music_slider:
            if y > self.height * 0.65:
                self.c.bind_all('<Button-1>', self.press_space)
            else:
                self.c.unbind_all('<Button-1>')
            return

        selected = len(self.options) - 1
        for i in range(len(self.mouse_positions)):
            if y > self.mouse_positions[i]:
                continue
            selected = i
            break
        if self.selected != selected:
            self.selected = selected
            self.audio.play_sound_effect('scroll')

