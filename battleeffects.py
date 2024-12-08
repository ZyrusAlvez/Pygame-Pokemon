from PIL import Image
import os, pygame
class BattleEffects:
    def __init__(self, gif_location, type, sound_path = None) -> None:
        self.gif_location = gif_location
        self.type = type
        self.sound_path = sound_path
    # convert gif file to multiple images/frames
    def animation_frames(self):
        self.frames = []
        gif = Image.open(self.gif_location)
        self.frames_number = gif.n_frames
        self.size = gif.size
        for frame in range(self.frames_number):
            gif.seek(frame)
            frame_image = gif.copy()
            frame_path = (f"./bin/{self.type}frame_{frame}.png")
            frame_image.save(frame_path)
            self.frames.append(frame_path)
        return self.frames
    
    def clear_residue(self):
        for frames in self.frames:
            os.remove(frames)
    
    def play_audio(self):
        pygame.mixer.init()
        pokemon_audio = pygame.mixer.Channel(1)
        sound = pygame.mixer.Sound(self.sound_path)
        if pokemon_audio.get_busy():
            pokemon_audio.stop()
        pokemon_audio.play(sound, loops= 0)

fireball = BattleEffects("assets/Attack_Balls/Fire.gif", "Fire")
waterball = BattleEffects("assets/Attack_Balls/Water.gif", "Water")
grassball = BattleEffects("assets/Attack_Balls/Grass.gif", "Grass")
firefx = BattleEffects("assets/Attack_Impact/Fire.gif", "Fire", "assets/audio/fire-explosion.mp3")
waterfx = BattleEffects("assets/Attack_Impact/Water.gif", "Water", "assets/audio/water-splash.mp3")
grassfx = BattleEffects("assets/Attack_Impact/Grass.gif", "Grass", "assets/audio/grass-sfx.wav")
pokeball = BattleEffects("assets/layout/pokeball.gif", "LoadingEffect")
potion = BattleEffects("assets/Poison & Potion/Heal.gif", "Potion", "assets/audio/heal-sfx.wav")
poison = BattleEffects("assets/Poison & Potion/Poison.gif", "Poison", "assets/audio/heal-sfx.wav")
opening = BattleEffects("assets/Transition/Opening Transition.gif", "Opening")
closing = BattleEffects("assets/Transition/Closing Transition.gif", "Closing")