import pygame
import os
from pokemon import *
import random
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# Desired size (e.g., 1.5 times the original size)
scale_factor1 = 1.5
scale_factor2 = 1.2
scale_factor3 = 1

# Array to store pokemons
pokemons = [bulbasaur,charizard,blastoise,weepinbell,arcanine,psyduck,scyther,magmar,poliwrath,farfetchd,moltres,vaporeon]
player1_pokemons = []
player2_pokemons = []

# store the images in a dictionary
loaded_images = {}
for i, pokemon in enumerate(pokemons):
    loaded_images[i] = [pygame.image.load(frame) for frame in pokemon.animation_frames()]

# makes sure that the index wont go beyond to the count of frames   
pokemon_frame_index = {}
for i, pokemon in enumerate(pokemons):
    pokemon_frame_index[i] = 0

map_array = [f"assets\Battleground\{file_name}" for file_name in os.listdir("assets\Battleground")]
def choose_map():
    chosen_map = random.choice(map_array)
    return chosen_map
    
update = False
focus = 2
running = True
battleground = choose_map()
pokemon1_index = random.randint(0,len(pokemons)-1)
pokemon2_index = random.randint(0,len(pokemons)-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                player1_pokemons.append(pokemons[1])
                
                         
    # background
    background_image = pygame.transform.scale(pygame.image.load(battleground), (screen.get_width(), screen.get_height()))
    # screen.fill((255, 255, 255))
    
    if not focus:
        pass
    elif focus == 1:
        pokemon1_image_rect = loaded_images[0][pokemon_frame_index[0]].get_rect(center=((screen.get_width() // 2 - 200, screen.get_height() // 2)))
        pokemon2_image_rect = loaded_images[1][pokemon_frame_index[1]].get_rect(center=((screen.get_width() // 2, screen.get_height() // 2)))
        pokemon3_image_rect = loaded_images[2][pokemon_frame_index[2]].get_rect(center=((screen.get_width() // 2 + 200, screen.get_height() // 2)))
        pokemon4_image_rect = loaded_images[3][pokemon_frame_index[3]].get_rect(center=((screen.get_width() // 2 + 400, screen.get_height() // 2)))
        screen.blit(loaded_images[0][pokemon_frame_index[0]], pokemon1_image_rect)
        screen.blit(loaded_images[1][pokemon_frame_index[1]], pokemon2_image_rect)
        screen.blit(loaded_images[2][pokemon_frame_index[2]], pokemon3_image_rect)
        screen.blit(loaded_images[3][pokemon_frame_index[3]], pokemon4_image_rect)
    elif focus == 2:
        screen.blit(background_image, (0,0))
        is_map_set = True
        pokemon1_image_rect = loaded_images[pokemon1_index][pokemon_frame_index[pokemon1_index]].get_rect(center=((int(screen.get_width() // 2) - 150, int(screen.get_height() // 2) + 10)))
        screen.blit(pygame.transform.scale(pygame.transform.flip(loaded_images[pokemon1_index][pokemon_frame_index[pokemon1_index]],True, False), tuple(i*2 for i in list(pokemons[pokemon1_index].size))), pokemon1_image_rect)
        pokemon2_image_rect = loaded_images[pokemon2_index][pokemon_frame_index[pokemon2_index]].get_rect(center=((int(screen.get_width() // 2) + 150, int((screen.get_height() // 2) + 10))))
        screen.blit(pygame.transform.scale(loaded_images[pokemon2_index][pokemon_frame_index[pokemon2_index]], tuple(i*2 for i in list(pokemons[pokemon2_index].size))), pokemon2_image_rect)
    else:
        pokemon1_image_rect = loaded_images[0][pokemon_frame_index[0]].get_rect(center=((screen.get_width() // 2 - 400, screen.get_height() // 2)))
        pokemon2_image_rect = loaded_images[1][pokemon_frame_index[1]].get_rect(center=((screen.get_width() // 2 - 200, screen.get_height() // 2)))
        pokemon3_image_rect = loaded_images[2][pokemon_frame_index[2]].get_rect(center=((screen.get_width() // 2, screen.get_height() // 2)))
        pokemon4_image_rect = loaded_images[3][pokemon_frame_index[3]].get_rect(center=((screen.get_width() // 2 + 200, screen.get_height() // 2)))
        pokemon5_image_rect = loaded_images[4][pokemon_frame_index[4]].get_rect(center=((screen.get_width() // 2 + 400, screen.get_height() // 2)))
        screen.blit(loaded_images[0][pokemon_frame_index[0]], pokemon1_image_rect)
        screen.blit(loaded_images[1][pokemon_frame_index[1]], pokemon2_image_rect)
        screen.blit(loaded_images[2][pokemon_frame_index[2]], pokemon3_image_rect)
        screen.blit(loaded_images[3][pokemon_frame_index[3]], pokemon4_image_rect)
        screen.blit(loaded_images[4][pokemon_frame_index[4]], pokemon5_image_rect)
    

    
    # update the screen
    pygame.display.flip()
    
    # makes sure that the index wont go beyond to the count of frames
    for i in pokemon_frame_index:
        pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(loaded_images[i])

    # fps
    clock.tick(40)

pygame.quit()

# Clean up extracted frames
for pokemon in pokemons:
    pokemon.animation_clean_up()
# try lang ni renzo kung okay na sa collaboration