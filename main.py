import pygame
from pokemon import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Array to store pokemons
pokemons = [bulbasaur, charizard, blastoise, weepinbell, arcanine, psyduck, scyther, magmar, poliwrath, farfetchd, moltres, vaporeon]
player1_pokemons = []
player1_loaded_images = []
player1_pokemon_frame_index = []
player2_pokemons = []
player2_loaded_images = []
player2_pokemon_frame_index = []
original_pokemons = pokemons[:]

# Load Pokémon animation frames
loaded_images = []
for pokemon in pokemons:
    loaded_images.append([pygame.image.load(frame) for frame in pokemon.animation_frames()])

# Frame index to track animation progress
pokemon_frame_index = [0 for _ in range(len(pokemons))]

# Other variables
focus = 0
running = True
number_of_selected = 0
background_image = pygame.transform.scale(pygame.image.load("./assets/layout/pick-middle.png"), (800, 600))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if number_of_selected % 2 == 0:
                    # Save the selected Pokémon for player1
                    player1_pokemons.append(pokemons[focus])
                    player1_loaded_images.append(loaded_images[focus])
                    player1_pokemon_frame_index.append(0)
                else:
                    # Save the selected Pokemon for player2
                    player2_pokemons.append(pokemons[focus])
                    player2_loaded_images.append(loaded_images[focus])
                    player2_pokemon_frame_index.append(0)

                # Remove from the selection pool
                pokemons.pop(focus)
                loaded_images.pop(focus)
                pokemon_frame_index.pop(focus)
                
                number_of_selected += 1

            elif event.key == pygame.K_RIGHT:
                focus += 1
                focus %= len(pokemons)

            elif event.key == pygame.K_LEFT:
                focus -= 1
                focus %= len(pokemons)

    # Draw background
    screen.blit(background_image, (0, 0))

    # Display Pokémon selection
    prev_index = (focus - 1) % len(pokemons)
    next_index = (focus + 1) % len(pokemons)

    # Scale and position Pokémon images
    pokemon1_image_size = pygame.transform.scale(loaded_images[prev_index][pokemon_frame_index[prev_index]],
                                                    (int(loaded_images[prev_index][pokemon_frame_index[prev_index]].get_width() * 1.1),
                                                    int(loaded_images[prev_index][pokemon_frame_index[prev_index]].get_height() * 1.1)))
    pokemon2_image_size = pygame.transform.scale(loaded_images[focus][pokemon_frame_index[focus]],
                                                    (int(loaded_images[focus][pokemon_frame_index[focus]].get_width() * 1.8),
                                                    int(loaded_images[focus][pokemon_frame_index[focus]].get_height() * 1.8)))
    pokemon3_image_size = pygame.transform.scale(loaded_images[next_index][pokemon_frame_index[next_index]],
                                                    (int(loaded_images[next_index][pokemon_frame_index[next_index]].get_width() * 1.1),
                                                    int(loaded_images[next_index][pokemon_frame_index[next_index]].get_height() * 1.1)))

    # Get positions
    pokemon1_image_rect = pokemon1_image_size.get_rect(midbottom=(screen.get_width() // 2 - 275, screen.get_height() // 2 - 30))
    pokemon2_image_rect = pokemon2_image_size.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() // 2 + 20))
    pokemon3_image_rect = pokemon3_image_size.get_rect(midbottom=(screen.get_width() // 2 + 275, screen.get_height() // 2 - 30))

    # Blit images
    screen.blit(pokemon1_image_size, pokemon1_image_rect)
    screen.blit(pokemon2_image_size, pokemon2_image_rect)
    screen.blit(pokemon3_image_size, pokemon3_image_rect)

    # Update the screen
    pygame.display.flip()

    # Update animation frames
    for i in range(len(pokemon_frame_index)):
        pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(loaded_images[i])
    for i in range(len(player1_pokemon_frame_index)):
        player1_pokemon_frame_index[i] = (player1_pokemon_frame_index[i] + 1) % len(player1_loaded_images[i])

    # Cap the frame rate
    clock.tick(40)

pygame.quit()

# Clean up extracted frames
for pokemon in original_pokemons:
    pokemon.animation_clean_up()