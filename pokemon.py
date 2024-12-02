from PIL import Image
import os

class Pokemon:
    def __init__(self, name:str, type:str, health:str, power:str, file_path:str, is_flying: bool, icon:str) -> None:
        self.name = name
        self.type = type
        self.health = health
        self.remaining_health = health
        self.power = power
        self.file_path = file_path
        self.icon = icon
        self.frames_number = 0
        self.is_flying = is_flying
        self.size = (0,0)
        self.temporary_power = self.power
    
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
            
bulbasaur = Pokemon("Bulbasaur", "Grass", 100, 30, "./assets/pokemon/bulbasaur.gif", False, "./assets/pokemon-icons/bulbasaur-icon.png")  
charizard = Pokemon("Charizard", "Fire", 30, 100, "./assets/pokemon/charizard.gif", False, "./assets/pokemon-icons/charizard-icon.png")
blastoise = Pokemon("Blastoise", "Water", 50, 50, "./assets/pokemon/blastoise.gif", False, "./assets/pokemon-icons/blastoise-icon.png")
weepinbell = Pokemon("Weepinbell", "Grass", 90, 40, "./assets/pokemon/weepinbell.gif", False, "./assets/pokemon-icons/weepinbell-icon.png")
arcanine  = Pokemon("Arcanine", "Fire", 40, 90, "./assets/pokemon/arcanine.gif", False, "./assets/pokemon-icons/arcanine-icon.png")
psyduck = Pokemon("Psyduck", "Water", 45, 45, "./assets/pokemon/psyduck.gif", False, "./assets/pokemon-icons/psyduck-icon.png")
scyther = Pokemon("Scyther", "Grass", 110, 30, "./assets/pokemon/scyther.gif", False, "./assets/pokemon-icons/scyther-icon.png")
magmar = Pokemon("Magmar", "Fire", 30, 110, "./assets/pokemon/magmar.gif", False, "./assets/pokemon-icons/magmar-icon.png")
piplup = Pokemon("Piplup", "Water", 55, 50, "./assets/pokemon/piplup.gif", False, "./assets/pokemon-icons/piplup-icon.png")
farfetchd = Pokemon("Farfetchd", "Grass", 100, 35, "./assets/pokemon/farfetchd.gif", False, "./assets/pokemon-icons/farfetchd-icon.png")
moltres = Pokemon("Moltres", "Fire", 35, 100, "./assets/pokemon/moltres.gif", False, "./assets/pokemon-icons/moltres-icon.png")
vaporeon = Pokemon("Vaporeon", "Water", 50, 55, "./assets/pokemon/vaporeon.gif", False, "./assets/pokemon-icons/vaporeon-icon.png")
