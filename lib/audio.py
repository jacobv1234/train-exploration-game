# class to handle audio systems, such as playing sound effects and shuffling background audio

from pygame import mixer
from random import choice

class AudioHandler:
    def __init__(self):
        # load the background song list
        self.bg_songs = []
        with open('./audio/bg_songs.txt', 'r') as f:
            self.bg_songs = [line[:-1] for line in f.readlines()]

        mixer.init()
        mixer.music.set_volume(0.8)

        self.playing = False

    def next_bg_music(self):
        if self.playing:
            next_song = ''
            while True:
                next_song = choice(self.bg_songs)
                if next_song != self.playing:
                    self.playing = next_song
                    break
        else:
            self.playing = choice(self.bg_songs)
        
        mixer.music.load(f'./audio/{self.playing}.mp3')
        mixer.music.play()

    def play_sound_effect(self, name: str):
        sound = mixer.Sound(f'./audio/{name}.mp3')
        sound.play()

    def is_playing(self):
        return mixer.music.get_busy()