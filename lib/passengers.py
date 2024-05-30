from tkinter import *
from json import loads, dumps

class Passengers:
    def __init__(self, window, height, savepath):
        self.c = Canvas(window, width=150,height=300,bg='white')
        self.c.place(x=0, y=(height/2)-150)
        self.c.create_rectangle(2,2,150,50,outline='black', fill='white')
        self.c.create_rectangle(2,50,150,298,outline='black', fill='white')
        self.c.create_text(75,25,fill='black', font='Arial 16', text='Passengers:')
        self.passengers = []
        self.objects = []

        with open(f'{savepath}/passengers.json', 'r') as f:
            p = loads(f.read())
        for passenger in p:
            self.add(passenger)

    def add(self, passenger):
        if len(self.passengers) < 5:
            self.passengers.append(passenger)
            self.objects.append(self.c.create_text(75, (len(self.passengers)*50) + 25, fill='black', font='Arial 10', text=(passenger['station'].split('/')[1]), anchor='center', width=150))
            return 2
        else:
            return 3

    def remove(self, station: str):
        if station == 'ALL':
            self.passengers = []
            for object in self.objects:
                self.c.delete(object)
            self.objects = []
            return
        
        if '@' in station:
            index = station.index('@')
            station = station[:index]

        for object in self.objects:
            self.c.delete(object)
        self.objects = []

        matches = []
        for i in range(len(self.passengers)-1,-1,-1):
            p = self.passengers[i]
            if p['station'] == station:
                matches.append(p)
                del self.passengers[i]
        
        reward = 0
        for passenger in matches:
            reward += passenger['reward']
        
        self.objects = [
            self.c.create_text(75, (i*50) + 75, fill='black', font='Arial 10', text=(self.passengers[i]['station'].split('/')[1]), anchor='center', width=150)
            for i in range(len(self.passengers))]
        
        return reward
    
    def save(self):
        with open('savedata/passengers.json', 'w') as f:
            f.write(dumps(self.passengers))