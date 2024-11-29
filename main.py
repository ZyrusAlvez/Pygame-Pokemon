import pygame
from pokemon import *
import random, time
from battleeffects import *
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

# Array to store map information
map_names = ["Viridale Plains", "Pyrolith Crater", "Azure Shoals"]

# Array to store projectile objects
battle_effects = [fireball, waterball, grassball]
# Load Pokémon animation frames
loaded_images = []
for pokemon in pokemons:
    loaded_images.append([pygame.image.load(frame) for frame in pokemon.animation_frames()])
# Load Battleeffects animation frames
battleeffects_frames = []
for effect in battle_effects:
    battleeffects_frames.append([pygame.image.load(frame) for frame in effect.animation_frames()])
# Frame index to track animation progress
pokemon_frame_index = [0 for _ in range(len(pokemons))]

# Other variables
focus = 0
running = True
number_of_selected = 0
background_image = pygame.transform.scale(pygame.image.load("./assets/layout/pick-middle.png"), (800, 600))

fighting_scene = False
choosing_pokemon_scene = True
map_selection = False

#For declaration of pokemon font
pokemon_font = pygame.font.Font("./assets/font/Pokemon-Em.ttf", 60)
def show_text(text, x_position, y_position):
    rendered_text = pokemon_font.render(text, False, "White")
    rendered_text_rect = rendered_text.get_rect(center = (x_position, y_position))
    pygame.draw.rect(screen, "#A8E6A3", rendered_text_rect)
    pygame.draw.rect(screen, "#A8E6A3", rendered_text_rect, 6, 2)
    screen.blit(rendered_text, rendered_text_rect)

background_image = pygame.transform.scale(pygame.image.load("./assets/layout/pick-middle.png"), (800, 600))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if choosing_pokemon_scene:
            if event.type == pygame.KEYDOWN:
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
    if choosing_pokemon_scene:
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



        # Update animation frames
        for i in range(len(pokemon_frame_index)):
            pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(loaded_images[i])
        for i in range(len(player1_pokemon_frame_index)):
            player1_pokemon_frame_index[i] = (player1_pokemon_frame_index[i] + 1) % len(player1_loaded_images[i])

        
        if len(player2_pokemons) == 3:
            choosing_pokemon_scene = False
            map_selection = True
            # Variables to be used for map randomizer / Next screen ( To avoid multiple declaration )
            map_index = random.randint(0, len(map_names)-1) # Random starting map
            starting_show_speed = 0.05
            is_map_final = False
        # Update the screen
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(40)

    if map_selection:
        current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{map_index}.png"), (800,600))
        current_name = map_names[map_index]
        screen.blit(current_background, (0,0))
        show_text(map_names[map_index], 400, 50)
        # Update the screen
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(60)
        
        if not is_map_final:
            starting_show_speed *= 1.1
            map_index = (map_index + 1) % len(map_names)
            time.sleep(starting_show_speed)
            if starting_show_speed >= 1.2:
                is_map_final = True
                map_selection = False
                fighting_scene = True
                # Preparation for next screen to avoid multiple declaration
                match_number = 0
                another_round = False
                attacking = False
                current_pokemon_index = (match_number) % 3
                player_1_pokemon = player1_pokemons[current_pokemon_index]
                player_2_pokemon = player2_pokemons[current_pokemon_index]
                x_pos = 0
                # Set up index to be used for each frame
                index = 0

                # Load up projectiles to be used by both pokemons
                for num in range(len(battle_effects)):
                    if battle_effects[num].element == player_1_pokemon.element:
                        player_1_battle_effect_image = battleeffects_frames[num]
                        player_1_battle_effect_index = 0
                    if battle_effects[num].element == player_2_pokemon.element:
                        player_2_battle_effect_image = battleeffects_frames[num]
                        player_2_battle_effect_index = 0
        

        

    if fighting_scene:
        if another_round:
            match_number += 1
            another_round = False
        
        current_pokemon_index = (match_number) % 3
        # Display chosen background
        screen.blit(current_background, (0,0))
        attacking = True
        if attacking:
       
            # Get current frames, resize and rotate them 
            player_1_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_1_battle_effect_image[player_1_battle_effect_index], -90), tuple([measure * 0.3 for measure in player_1_battle_effect_image[index].get_size()]))
            player_2_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_2_battle_effect_image[player_2_battle_effect_index], 90), tuple([measure * 0.3 for measure in player_2_battle_effect_image[index].get_size()]))
            # Position each
            player_1_battle_effect_current_img_rect = player_1_battle_effect_current_img.get_rect(midbottom = ((screen.get_width() // 2 - 200 ) + x_pos, screen.get_height() // 2 + 150 ))
            player_2_battle_effect_current_img_rect = player_2_battle_effect_current_img.get_rect(midbottom = ((screen.get_width() // 2 + 200) - x_pos, screen.get_height() // 2 + 150))

            # Increment x to make each image closer to middle ( 400 )
            x_pos += 1
            if player_1_battle_effect_current_img_rect.colliderect(player_2_battle_effect_current_img_rect):
                show_text(f"{player_1_pokemon.name if player_1_pokemon.power > player_2_pokemon.power else player_2_pokemon.name} overwhelmes {player_2_pokemon.name if player_2_pokemon.power > player_1_pokemon.power else player_1_pokemon.name}", screen.get_width() // 2, screen.get_height() + 500)
            
            # Draw them each
            screen.blit(player_1_battle_effect_current_img, player_1_battle_effect_current_img_rect)
            screen.blit(player_2_battle_effect_current_img, player_2_battle_effect_current_img_rect)
            # Update each index for the battle effect frame
            player_1_battle_effect_index = (player_1_battle_effect_index + 1) % len(player_1_battle_effect_image)
            player_2_battle_effect_index = (player_2_battle_effect_index + 1) % len(player_2_battle_effect_image)

        # Get current frame and resize it proportionally
        player_1_pokemon_image = pygame.transform.flip(pygame.transform.scale(player1_loaded_images[current_pokemon_index][player1_pokemon_frame_index[current_pokemon_index]], tuple([measure*1.5 for measure in player_1_pokemon.size])), True, False)
        player_2_pokemon_image = pygame.transform.scale(player2_loaded_images[current_pokemon_index][player2_pokemon_frame_index[current_pokemon_index]], tuple([measure*1.5 for measure in player_2_pokemon.size]))

        # Position them in the screen properly and on the same footing to show difference in size
        player_1_pokemon_rect = player_1_pokemon_image.get_rect(midbottom = (screen.get_width() // 4, screen.get_height() // 2 + 150))
        player_2_pokemon_rect = player_2_pokemon_image.get_rect(midbottom = (screen.get_width() // 2 + 200, screen.get_height() // 2 + 150))

        # Put them on the screen
        screen.blit(player_1_pokemon_image, player_1_pokemon_rect)
        screen.blit(player_2_pokemon_image, player_2_pokemon_rect)

        # Update frame index
        player1_pokemon_frame_index[current_pokemon_index] = (player1_pokemon_frame_index[current_pokemon_index] + 1) % len(player1_loaded_images[current_pokemon_index])
        player2_pokemon_frame_index[current_pokemon_index] = (player2_pokemon_frame_index[current_pokemon_index] + 1) % len(player2_loaded_images[current_pokemon_index])

        pygame.display.flip()
        clock.tick(40)
# Clean up extracted frames
for pokemon in original_pokemons:
    pokemon.animation_clean_up()
pygame.quit()


