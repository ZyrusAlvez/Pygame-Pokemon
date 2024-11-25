from PIL import Image
import os

class Pokemon:
    def __init__(self, name:str, element:str, health:str, power:str, file_path:str, is_flying: bool) -> None:
        self.name = name
        self.element = element
        self.health = health
        self.power = power
        self.file_path = file_path
        self.frames_number = 0
        self.is_flying = is_flying
        self.size = (0,0)
        
    # convert gif file to multiple images/frames
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
            
bulbasaur = Pokemon("Bulbasaur", "Grass", 500, 280, "./assets/pokemon/bulbasaur.gif", False)  
charizard = Pokemon("Charizard", "Fire", 480, 300, "./assets/pokemon/charizard.gif", False)
blastoise = Pokemon("Blastoise", "Water", 460, 320, "./assets/pokemon/blastoise.gif", False)
weepinbell = Pokemon("Weepinbell", "Grass", 440, 340, "./assets/pokemon/weepinbell.gif", False)
arcanine  = Pokemon("Arcanine", "Fire", 420, 360, "./assets/pokemon/arcanine.gif", False)
psyduck = Pokemon("Psyduck", "Water", 400, 380, "./assets/pokemon/psyduck.gif", False)
scyther = Pokemon("Scyther", "Grass", 380, 400, "./assets/pokemon/scyther.gif", False)
magmar = Pokemon("Magmar", "Fire", 360, 420, "./assets/pokemon/magmar.gif", False)
poliwrath = Pokemon("Poliwrath", "Water", 340, 440, "./assets/pokemon/poliwrath.gif", False)
farfetchd = Pokemon("Farfetchd", "Grass", 320, 460, "./assets/pokemon/farfetchd.gif", False)
moltres = Pokemon("Moltres", "Fire", 300, 480, "./assets/pokemon/moltres.gif", False)
vaporeon = Pokemon("Vaporeon", "Water", 280, 500, "./assets/pokemon/vaporeon.gif", False)
