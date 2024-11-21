import pygame
import os
from pokemon import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1100, 600))
clock = pygame.time.Clock()


# Desired size (e.g., 1.5 times the original size)
scale_factor1 = 1.5
scale_factor2 = 1.2
scale_factor3 = 1

# Array to store pokemons
pokemons = [butterfree, charizard, dugtrio, golbat, kadabra, meowth, nidoking, pidgeot, pikachu, venonat, venusaur, wartortle]

# store the images in a dictionary
loaded_images = {}
for i, pokemon in enumerate(pokemons, 1):
    loaded_images[i] = [pygame.image.load(frame) for frame in pokemon.animation_frames()]

# makes sure that the index wont go beyond to the count of frames   
pokemon_frame_index = {}
for i, pokemon in enumerate(pokemons, 1):
    pokemon_frame_index[i] = 0
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # background
    screen.fill((255, 255, 255))
    
    # Get the image's rectangle (bounding box) and place it on the screen using its center
    pokemon1_image_rect = loaded_images[1][pokemon_frame_index[1]].get_rect(center=((screen.get_width() // 2, screen.get_height() // 2)))
    pokemon2_image_rect = loaded_images[2][pokemon_frame_index[2]].get_rect(center=((screen.get_width() // 2 + 200, screen.get_height() // 2)))
    pokemon3_image_rect = loaded_images[3][pokemon_frame_index[3]].get_rect(center=((screen.get_width() // 2 - 200, screen.get_height() // 2)))
    pokemon4_image_rect = loaded_images[4][pokemon_frame_index[4]].get_rect(center=((screen.get_width() // 2 + 400, screen.get_height() // 2)))
    pokemon5_image_rect = loaded_images[5][pokemon_frame_index[5]].get_rect(center=((screen.get_width() // 2 - 400, screen.get_height() // 2)))
    
    # showed pokemon
    screen.blit(loaded_images[1][pokemon_frame_index[1]], pokemon1_image_rect)
    screen.blit(loaded_images[2][pokemon_frame_index[2]], pokemon2_image_rect)
    screen.blit(loaded_images[3][pokemon_frame_index[3]], pokemon3_image_rect)
    screen.blit(loaded_images[4][pokemon_frame_index[4]], pokemon4_image_rect)
    screen.blit(loaded_images[5][pokemon_frame_index[5]], pokemon5_image_rect)
    
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