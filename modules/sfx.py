import pygame

BASE_SFX_PATH = "assets/audio"

class SFX:
    sfx_list = []
    def __init__(self,name, audio_path):
        self.name = name
        self.path = audio_path
        self.audio = pygame.mixer.Sound(f"{BASE_SFX_PATH}/{audio_path}")
        SFX.sfx_list.append(self)
    @classmethod
    def play(cls,name):
        for s in cls.sfx_list:
            if name == s.name:
                s.audio.play()
                break