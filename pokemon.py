from PIL import Image
import os

class Pokemon:
    def __init__(self, name:str, type:str, health:str, power:str, file_path:str, is_flying: bool, icon:str) -> None:
        self.name = name
        self.type = type
        self.health = health
        self.power = power
        self.file_path = file_path
        self.icon = icon
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
            
bulbasaur = Pokemon("Bulbasaur", "Grass", 500, 280, "./assets/pokemon/bulbasaur.gif", False, "./assets/pokemon-icons/bulbasaur-icon.png")  
charizard = Pokemon("Charizard", "Fire", 480, 300, "./assets/pokemon/charizard.gif", False, "./assets/pokemon-icons/charizard-icon.png")
blastoise = Pokemon("Blastoise", "Water", 460, 320, "./assets/pokemon/blastoise.gif", False, "./assets/pokemon-icons/blastoise-icon.png")
weepinbell = Pokemon("Weepinbell", "Grass", 440, 340, "./assets/pokemon/weepinbell.gif", False, "./assets/pokemon-icons/weepinbell-icon.png")
arcanine  = Pokemon("Arcanine", "Fire", 420, 360, "./assets/pokemon/arcanine.gif", False, "./assets/pokemon-icons/arcanine-icon.png")
psyduck = Pokemon("Psyduck", "Water", 400, 380, "./assets/pokemon/psyduck.gif", False, "./assets/pokemon-icons/psyduck-icon.png")
scyther = Pokemon("Scyther", "Grass", 380, 400, "./assets/pokemon/scyther.gif", False, "./assets/pokemon-icons/scyther-icon.png")
magmar = Pokemon("Magmar", "Fire", 360, 420, "./assets/pokemon/magmar.gif", False, "./assets/pokemon-icons/magmar-icon.png")
poliwrath = Pokemon("Poliwrath", "Water", 340, 440, "./assets/pokemon/poliwrath.gif", False, "./assets/pokemon-icons/poliwrath-icon.png")
farfetchd = Pokemon("Farfetchd", "Grass", 320, 460, "./assets/pokemon/farfetchd.gif", False, "./assets/pokemon-icons/farfetchd-icon.png")
moltres = Pokemon("Moltres", "Fire", 300, 480, "./assets/pokemon/moltres.gif", False, "./assets/pokemon-icons/moltres-icon.png")
vaporeon = Pokemon("Vaporeon", "Water", 280, 500, "./assets/pokemon/vaporeon.gif", False, "./assets/pokemon-icons/vaporeon-icon.png")
