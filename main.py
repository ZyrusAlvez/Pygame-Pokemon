import pygame
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
pokemons = [bulbasaur,charizard,blastoise,weepinbell,arcanine,psyduck,scyther,magmar,poliwrath,farfetchd,moltres,vaporeon]
player1_pokemons = []
player2_pokemons = []

# store the images in a list
loaded_images = []
for pokemon in pokemons:
    loaded_images.append([pygame.image.load(frame) for frame in pokemon.animation_frames()])

# makes sure that the index wont go beyond to the count of frames   
pokemon_frame_index = [0 for _ in range(len(pokemons))]
    
update = False
focus = 0
running = True

background_image = pygame.transform.scale(pygame.image.load("./assets/layout/picking-middle.png"), (800, 600))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                player1_pokemons.append(pokemons[focus])
                pokemons.pop(focus)
                loaded_images.pop(focus)
                pokemon_frame_index.pop(focus)
            if event.key == pygame.K_RIGHT:
                focus += 1
                focus %= len(pokemons) - 1
            if event.key == pygame.K_LEFT:
                focus -= 1
                focus %= len(pokemons) - 1
                
                         
    # background
    screen.blit(background_image, (0, 0))

    # image size
    pokemon1_image_size = pygame.transform.scale(loaded_images[focus - 1][pokemon_frame_index[focus - 1]], (int(loaded_images[focus - 1][pokemon_frame_index[focus - 1]].get_width() * 1.1),int(loaded_images[focus - 1][pokemon_frame_index[focus - 1]].get_height() * 1.1)))
    pokemon2_image_size = pygame.transform.scale(loaded_images[focus][pokemon_frame_index[focus]], (int(loaded_images[focus][pokemon_frame_index[focus]].get_width() * 2),int(loaded_images[focus][pokemon_frame_index[focus]].get_height() * 1.8)))
    pokemon3_image_size = pygame.transform.scale(loaded_images[focus + 1][pokemon_frame_index[focus + 1]], (int(loaded_images[focus + 1][pokemon_frame_index[focus + 1]].get_width() * 1.1),int(loaded_images[focus + 1][pokemon_frame_index[focus + 1]].get_height() * 1.1)))
    
    # get image's dimension and location of placement
    pokemon1_image_rect = pokemon1_image_size.get_rect(midbottom=((screen.get_width() // 2 - 275, screen.get_height() // 2 - 30)))
    pokemon2_image_rect = pokemon2_image_size.get_rect(midbottom=((screen.get_width() // 2, screen.get_height() // 2 + 20)))
    pokemon3_image_rect = pokemon3_image_size.get_rect(midbottom=((screen.get_width() // 2 + 275, screen.get_height() // 2 - 30)))
    
    # place the image into the screen
    screen.blit(pokemon1_image_size, pokemon1_image_rect)
    screen.blit(pokemon2_image_size, pokemon2_image_rect)
    screen.blit(pokemon3_image_size, pokemon3_image_rect)

    
    # update the screen
    pygame.display.flip()
    
    # makes sure that the index wont go beyond to the count of frames
    for i in range(len(pokemon_frame_index)):
        pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(loaded_images[i])

    # fps
    clock.tick(40)

pygame.quit()

# Clean up extracted frames
for pokemon in pokemons:
    pokemon.animation_clean_up()