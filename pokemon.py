from PIL import Image
import os

class Pokemon:
    def __init__(self, name:str, type:str, health:str, power:str, file_path:str) -> None:
        self.name = name
        self.type = type
        self.health = health
        self.power = power
        self.file_path = file_path
        self.frames_number = 0
    # convert gif file to multiple images/frames
    def animation_frames(self):
        self.frames = []
        gif = Image.open(self.file_path)
        self.frames_number = gif.n_frames
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
            
butterfree = Pokemon("Butterfree", "Fire", 100, 100, "./assets/pokemon/butterfree.gif")  
charizard = Pokemon("Charizard", "Fire", 100, 100, "./assets/pokemon/charizard.gif")
dugtrio = Pokemon("Dugtrio", "Fire", 100, 100, "./assets/pokemon/dugtrio.gif")
golbat = Pokemon("Golbat", "Fire", 100, 100, "./assets/pokemon/golbat.gif")
kadabra = Pokemon("Kadabra", "Fire", 100, 100, "./assets/pokemon/kadabra.gif")
meowth = Pokemon("Meowth", "Fire", 100, 100, "./assets/pokemon/meowth.gif")
nidoking = Pokemon("Nidoking", "Fire", 100, 100, "./assets/pokemon/nidoking.gif")
pidgeot = Pokemon("Pidgeot", "Fire", 100, 100, "./assets/pokemon/pidgeot.gif")
pikachu = Pokemon("Pikachu", "Fire", 100, 100, "./assets/pokemon/pikachu.gif")
venonat = Pokemon("Venonat", "Fire", 100, 100, "./assets/pokemon/venonat.gif")
venusaur = Pokemon("Venusaur", "Fire", 100, 100, "./assets/pokemon/venusaur.gif")
wartortle = Pokemon("Wartortle", "Fire", 100, 100, "./assets/pokemon/wartortle.gif")