import pygame
from PIL import Image
import os

pygame.mixer.init()

class Pokemon:
    def __init__(self, name: str, type: str, health: int, power: int, file_path: str, is_flying: bool, icon: str, audio_path: str) -> None:
        self.name = name
        self.type = type
        self.health = health
        self.remaining_health = health
        self.power = power
        self.file_path = file_path
        self.icon = icon
        self.audio_path = audio_path
        self.frames_number = 0
        self.is_flying = is_flying
        self.size = (0, 0)
        self.temporary_power = self.power

    # Convert gif file to multiple images/frames
    def animation_frames(self):
        self.frames = []
        gif = Image.open(self.file_path)
        self.frames_number = gif.n_frames
        self.size = gif.size
        for frame in range(self.frames_number):
            gif.seek(frame)
            frame_image = gif.copy()
            frame_path = (f"./bin/{self.name}frame_{frame}.png")
            frame_image.save(frame_path)
            self.frames.append(frame_path)
        return self.frames
    
    def animation_clean_up(self):
        for frame in range(self.frames_number):
            os.remove(f"./bin/{self.name}frame_{frame}.png")

    def play_audio(self):
        pygame.mixer.init()
        pokemon_audio = pygame.mixer.Channel(1)
        sound = pygame.mixer.Sound(self.audio_path)
        if pokemon_audio.get_busy():
            pokemon_audio.stop()
        pokemon_audio.play(sound, loops= 0)
            
# Example Pokémon objects
bulbasaur = Pokemon("Bulbasaur", "Grass", 10, 30, "./assets/pokemon/bulbasaur.gif", False, "./assets/pokemon-icons/bulbasaur-icon.png", "./assets/audio/bulbasaur-sound.mp3")
charizard = Pokemon("Charizard", "Fire", 30, 100, "./assets/pokemon/charizard.gif", False, "./assets/pokemon-icons/charizard-icon.png", "./assets/audio/charizard-sound.mp3")
blastoise = Pokemon("Blastoise", "Water", 50, 50, "./assets/pokemon/blastoise.gif", False, "./assets/pokemon-icons/blastoise-icon.png", "./assets/audio/blastoise-sound.mp3")
weepinbell = Pokemon("Weepinbell", "Grass", 90, 40, "./assets/pokemon/weepinbell.gif", False, "./assets/pokemon-icons/weepinbell-icon.png", "./assets/audio/weepinbell-sound.mp3")
arcanine = Pokemon("Arcanine", "Fire", 40, 90, "./assets/pokemon/arcanine.gif", False, "./assets/pokemon-icons/arcanine-icon.png", "./assets/audio/arcanine-sound.mp3")
psyduck = Pokemon("Psyduck", "Water", 45, 45, "./assets/pokemon/psyduck.gif", False, "./assets/pokemon-icons/psyduck-icon.png", "./assets/audio/psyduck-sound.mp3")
scyther = Pokemon("Scyther", "Grass", 110, 30, "./assets/pokemon/scyther.gif", False, "./assets/pokemon-icons/scyther-icon.png", "./assets/audio/scyther-sound.mp3")
magmar = Pokemon("Magmar", "Fire", 30, 110, "./assets/pokemon/magmar.gif", False, "./assets/pokemon-icons/magmar-icon.png", "./assets/audio/magmar-sound.mp3")
piplup = Pokemon("Piplup", "Water", 55, 50, "./assets/pokemon/piplup.gif", False, "./assets/pokemon-icons/piplup-icon.png", "./assets/audio/piplup-sound.mp3")
farfetchd = Pokemon("Farfetchd", "Grass", 100, 35, "./assets/pokemon/farfetchd.gif", False, "./assets/pokemon-icons/farfetchd-icon.png", "./assets/audio/farfetchd-sound.mp3")
moltres = Pokemon("Moltres", "Fire", 35, 100, "./assets/pokemon/moltres.gif", False, "./assets/pokemon-icons/moltres-icon.png", "./assets/audio/moltres-sound.mp3")
vaporeon = Pokemon("Vaporeon", "Water", 50, 55, "./assets/pokemon/vaporeon.gif", False, "./assets/pokemon-icons/vaporeon-icon.png", "./assets/audio/vaporeon-sound.mp3")
