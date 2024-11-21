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
            
bulbasaur = Pokemon("Bulbasaur", "Grass", 500, 280, "./assets/pokemon/bulbasaur.gif")  
charizard = Pokemon("Charizard", "Fire", 480, 300, "./assets/pokemon/charizard.gif")
blastoise = Pokemon("Blastoise", "Water", 460, 320, "./assets/pokemon/blastoise.gif")
weepinbell = Pokemon("Weepinbell", "Grass", 440, 340, "./assets/pokemon/weepinbell.gif")
arcanine  = Pokemon("Arcanine", "Fire", 420, 360, "./assets/pokemon/arcanine.gif")
psyduck = Pokemon("Psyduck", "Water", 400, 380, "./assets/pokemon/psyduck.gif")
scyther = Pokemon("Scyther", "Grass", 380, 400, "./assets/pokemon/scyther.gif")
magmar = Pokemon("Magmar", "Fire", 360, 420, "./assets/pokemon/magmar.gif")
poliwrath = Pokemon("Poliwrath", "Water", 340, 440, "./assets/pokemon/poliwrath.gif")
farfetchd = Pokemon("Farfetchd", "Grass", 320, 460, "./assets/pokemon/farfetchd.gif")
moltres = Pokemon("Moltres", "Fire", 300, 480, "./assets/pokemon/moltres.gif")
vaporeon = Pokemon("Vaporeon", "Water", 280, 500, "./assets/pokemon/vaporeon.gif")
