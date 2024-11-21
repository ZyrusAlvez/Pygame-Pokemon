from PIL import Image
import os

class Pokemon:
    def __init__(self, name:str, type:str, health:str, power:str, file_path:str) -> None:
        self.name = name
        self.type = type
        self.health = health
        self.power = power
        self.file_path = file_path
        
    # convert gif file to multiple images/frames
    def animation_frames(self):
        self.frames = []
        gif = Image.open(self.file_path)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.copy()
            frame_path = (f"./bin/frame_{frame}.png")
            frame_image.save(frame_path)
            self.frames.append(frame_path)
        return self.frames
    
    def animation_clean_up(self):
        for frame in self.frames:
            os.remove(frame)
            
butterfree = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/butterfree.gif")  
charizard = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/charizard.gif")
dugtrio = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/dugtrio.gif")
golbat = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/golbat.gif")
kadabra = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/kadabra.gif")
meowth = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/meowth.gif")
nidoking = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/nidoking.gif")
pidgeot = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/pidgeot.gif")
pikachu = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/pikachu.gif")
venonat = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/venonat.gif")
venusaur = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/venusaur.gif")
wartortle = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/wartortle.gif")