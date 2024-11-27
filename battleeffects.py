from PIL import Image
import os
class BattleEffects:
    def __init__(self, gif_location, element) -> None:
        self.gif_location = gif_location
        self.element = element

    # convert gif file to multiple images/frames
    def animation_frames(self):
        self.frames = []
        gif = Image.open(self.gif_location)
        self.frames_number = gif.n_frames
        self.size = gif.size
        for frame in range(self.frames_number):
            gif.seek(frame)
            frame_image = gif.copy()
            frame_path = (f"./bin/{self.element}frame_{frame}.png")
            frame_image.save(frame_path)
            self.frames.append(frame_path)
        return self.frames
    
    def clear_residue(self):
        for frames in self.frames:
            os.remove(frames)

fireball = BattleEffects("assets/Attack_Balls/Fire.gif", "Fire")
waterball = BattleEffects("assets/Attack_Balls/Water.gif", "Water")
grassball = BattleEffects("assets/Attack_Balls/Grass.gif", "Grass")