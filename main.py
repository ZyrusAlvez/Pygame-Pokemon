import pygame
import os
from pokemon import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# Desired size (e.g., 1.5 times the original size)
scale_factor1 = 1.5
scale_factor2 = 1.2
scale_factor3 = 1

# Array to store pokemons
pokemons = [butterfree, charizard, dugtrio, golbat, kadabra, meowth, nidoking, pidgeot, pikachu, venonat, venusaur, wartortle]
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
    
update = False
focus = 2
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                player1_pokemons.append(pokemons[1])
                
                         
    # background
    screen.fill((255, 255, 255))
    
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
charizard.animation_clean_up()
# try lang ni renzo kung okay na sa collaboration