from tkinter import *
class PressSpaceToEnter:
    def __init__(self, window: Tk, width: int, height: int, space_function):
        self.c = Canvas(window, width=300,height=40,bg='white')
        self.c.place(x= (width/2)-150, y = height-38)
        self.c.create_rectangle(3,3,299,295,outline='black', fill='')
        self.c.create_text(150,20,fill='black', font='Arial 10', text='Press Space or click here to enter', anchor='center')
        self.live = True
        self.c.bind_all('<Button-1>', self.mouse_click, add = True)
        self.space_function = space_function
        self.screen_width = width
        self.screen_height = height
    
    def mouse_click(self, event: Event):
        x, y = (event.x_root, event.y_root)
        screen_x_center = self.screen_width / 2
        if y > self.screen_height - 40 and x > screen_x_center - 75 and x < screen_x_center + 75:
            self.space_function(None)
    
    def remove(self):
        self.c.destroy()
        self.live = False