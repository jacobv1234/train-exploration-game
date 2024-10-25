# class to handle audio systems, such as playing sound effects and shuffling background audio

from pygame import mixer
from random import choice

class AudioHandler:
    def __init__(self, music_vol: float = 1, sound_vol: float = 1, loop_vol: float = 1):
        # load the background song list
        self.bg_songs = []
        with open('./audio/bg_songs.txt', 'r') as f:
            self.bg_songs = [line[:-1] for line in f.readlines()]

        self.music_vol = music_vol
        self.sound_vol = sound_vol
        self.loop_vol = loop_vol

        mixer.init()
        mixer.music.set_volume(music_vol)

        # preloaded sound effects
        # these ones are preloaded as they are longer and would cause a massive lag spike if loaded live
        self.preloaded_sound_effects = {}
        with open('./audio/preload_sounds.txt', 'r') as f:
            for sound in [line[:-1] for line in f.readlines()]:
                self.preloaded_sound_effects[sound] = mixer.Sound(f'./audio/{sound}.mp3')

        self.playing = False
        self.loop_sound = False

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
        if name in list(self.preloaded_sound_effects.keys()):
            sound = self.preloaded_sound_effects[name]
        else:
            sound = mixer.Sound(f'./audio/{name}.mp3')
        sound.set_volume(self.sound_vol)
        sound.play()

    def is_playing(self):
        return mixer.music.get_busy()
    
    def stop_looping_sound(self):
        if self.loop_sound:
            self.loop_sound.fadeout(100)

    def loop_sound_effect(self, name: str):
        self.stop_looping_sound()
        if name in list(self.preloaded_sound_effects.keys()):
            self.loop_sound = self.preloaded_sound_effects[name]
        else:
            self.loop_sound = mixer.Sound(f'./audio/{name}.mp3')
        self.loop_sound.set_volume(self.loop_vol)
        self.loop_sound.play(loops=-1)

    def update_volumes(self, music_vol, sound_vol, loop_vol):
        self.music_vol = music_vol
        self.sound_vol = sound_vol
        self.loop_vol = loop_vol
        mixer.music.set_volume(music_vol)