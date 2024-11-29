import pygame
from pokemon import *
import random, time
from battleeffects import *
from utility import *

# for asynchronous operation (loading screen)
import threading
# this solves the slowness of threading
from concurrent.futures import ThreadPoolExecutor

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Global initialization
pokemons = [bulbasaur, charizard, blastoise, weepinbell, arcanine, psyduck, scyther, magmar, poliwrath, farfetchd, moltres, vaporeon]
original_pokemons = pokemons[:]
battle_effects = [fireball, waterball, grassball]
type_icons = [pygame.image.load("assets/type-icons/Fire.png"), pygame.image.load("assets/type-icons/Grass.png"), pygame.image.load("assets/type-icons/Water.png")]

# this requires a lot of time to load
def load_images() -> list:
    loading_complete = False

    def load_images_task():
        nonlocal loading_complete
        global pokemon_loaded_images, battle_effects_loaded_images
        
        def load_pokemon_frames(pokemon):
            return [pygame.image.load(frame) for frame in pokemon.animation_frames()]

        def load_effect_frames(effect):
            return [pygame.image.load(frame) for frame in effect.animation_frames()]

        # Use ThreadPoolExecutor to load frames in parallel
        with ThreadPoolExecutor() as executor:
            pokemon_loaded_images = list(executor.map(load_pokemon_frames, pokemons))
            battle_effects_loaded_images = list(executor.map(load_effect_frames, battle_effects))

        loading_complete = True

    # Start loading images in a thread
    loading_thread = threading.Thread(target=load_images_task)
    loading_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()

        # Render loading  screen
        screen.blit(pygame.image.load("assets/Battleground/0.png"), (0,0))
        show_text("Team Rocket", 400, 300, screen)

        pygame.display.update()
        
        if loading_complete:
            return pokemon_loaded_images, battle_effects_loaded_images


def pokemon_selection_scene(pokemon_loaded_images: list) -> list:
    # Initialization
    player1_pokemons = []
    player1_loaded_images = []
    player2_pokemons = []
    player2_loaded_images = []
    
    # Frame index to track animation progress
    pokemon_frame_index = [0 for _ in range(len(pokemons))]
    
    focus = 0
    number_of_selected = 0
    background_image = pygame.transform.scale(pygame.image.load("./assets/layout/pick-middle.png"), (800, 600))
    
    arrow_left_state_counter = 0
    arrow_right_state_counter = 0
    select_button_state_counter = 0
    
    def select_pokemon(number_of_selected, focus):
        if number_of_selected % 2 == 0:
            # Save the selected Pokémon for player1
            player1_pokemons.append(pokemons[focus])
            player1_loaded_images.append(pokemon_loaded_images[focus])
        else:
            # Save the selected Pokemon for player2
            player2_pokemons.append(pokemons[focus])
            player2_loaded_images.append(pokemon_loaded_images[focus])
            
        # Remove from the selection pool
        pokemons.pop(focus)
        pokemon_loaded_images.pop(focus)
        pokemon_frame_index.pop(focus)
        focus -= 1
        number_of_selected += 1
        return number_of_selected, focus
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                   updated_number_of_selected, updated_focus = select_pokemon(number_of_selected, focus)
                   focus = updated_focus
                   number_of_selected = updated_number_of_selected
                if event.key == pygame.K_RIGHT:
                    focus = (focus + 1) % len(pokemons)
                if event.key == pygame.K_LEFT:
                    focus = (focus - 1) % len(pokemons)
            
            # Check if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if click is inside the button
                if arrow_left_rect.collidepoint(event.pos):  
                   focus = (focus - 1) % len(pokemons)
                   arrow_left_state_counter = 5
                if arrow_right_rect.collidepoint(event.pos):  
                   focus = (focus + 1) % len(pokemons)
                   arrow_right_state_counter = 5
                if select_button_rect.collidepoint(event.pos):  
                   updated_number_of_selected, updated_focus = select_pokemon(number_of_selected, focus)
                   focus = updated_focus
                   number_of_selected = updated_number_of_selected
                   select_button_state_counter = 5
                   

        # Update nearby pokemon index (carousel purposes)
        prev_index = (focus - 1) % len(pokemons)
        next_index = (focus + 1) % len(pokemons)
        
        # Draw background
        screen.blit(background_image, (0, 0))

        # Scale Pokemon images
        pokemon1_image = scale(pokemon_loaded_images[prev_index][pokemon_frame_index[prev_index]], 1.1)
        pokemon2_image = scale(pokemon_loaded_images[focus][pokemon_frame_index[focus]], 1.9)
        pokemon3_image = scale(pokemon_loaded_images[next_index][pokemon_frame_index[next_index]], 1.1)

        # Get positions
        pokemon1_image_rect = pokemon1_image.get_rect(midbottom=(screen.get_width() // 2 - 275, screen.get_height() // 2 - 30))
        pokemon2_image_rect = pokemon2_image.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        pokemon3_image_rect = pokemon3_image.get_rect(midbottom=(screen.get_width() // 2 + 275, screen.get_height() // 2 - 30))

        # show images
        screen.blit(pokemon1_image, pokemon1_image_rect)
        screen.blit(pokemon2_image, pokemon2_image_rect)
        screen.blit(pokemon3_image, pokemon3_image_rect)
        
        # buttons
        if arrow_left_state_counter:
            arrow_left = scale(pygame.image.load("assets/buttons/arrow-left-clicked.png"), 0.17)
            arrow_left_state_counter -= 1
        else:
            arrow_left = scale(pygame.image.load("assets/buttons/arrow-left.png"), 0.17)
        arrow_left_rect = arrow_left.get_rect(center=(230, 415))
        screen.blit(arrow_left, arrow_left_rect)
        
        if arrow_right_state_counter:
            arrow_right = scale(pygame.image.load("assets/buttons/arrow-right-clicked.png"), 0.17)
            arrow_right_state_counter -= 1
        else:
            arrow_right = scale(pygame.image.load("assets/buttons/arrow-right.png"), 0.17)
        arrow_right_rect = arrow_right.get_rect(center=(580, 415))
        screen.blit(arrow_right, arrow_right_rect)
        
        if select_button_state_counter:
            select_button = scale(pygame.image.load("assets/buttons/select-button-clicked.png"), 0.3)
            select_button_state_counter -= 1
        else:
            select_button = scale(pygame.image.load("assets/buttons/select-button.png"), 0.3)
        select_button_rect = select_button.get_rect(center=(400, 415))
        screen.blit(select_button, select_button_rect)
        
        # show pokemon info
        screen.blit(scale(pygame.image.load(pokemons[focus].icon), 0.5), (225, 480))
        show_text(pokemons[focus].name, 265, 485, screen, "topleft", 30, "Black")
        screen.blit(scale(pygame.image.load(f"assets/type-icons/{pokemons[focus].type}.png"), 0.5), (550, 480))
        show_text(f"Power  : {pokemons[focus].power}", 236, 530, screen, "topleft", 25, "Black")
        show_text(f"Health : {pokemons[focus].health}", 235, 565, screen, "topleft", 25, "Black")

        # Update animation frames
        for i in range(len(pokemon_frame_index)):
            pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(pokemon_loaded_images[i])
            
        # Conditional Rendering for icons
        if len(player1_pokemons) >= 1:
            screen.blit(scale(pygame.image.load(player1_pokemons[0].icon), 0.5), (15, 50))
        if len(player2_pokemons) >= 1:
            screen.blit(scale(pygame.image.load(player2_pokemons[0].icon), 0.5), (630, 50))
        if len(player1_pokemons) >= 2:
            screen.blit(scale(pygame.image.load(player1_pokemons[1].icon), 0.5), (65, 50))
        if len(player2_pokemons) >= 2:
            screen.blit(scale(pygame.image.load(player2_pokemons[1].icon), 0.5), (680, 50))
        if len(player1_pokemons) >= 3:
            screen.blit(scale(pygame.image.load(player1_pokemons[2].icon), 0.5), (115, 50))
        if len(player2_pokemons) >= 3:
            screen.blit(scale(pygame.image.load(player2_pokemons[2].icon), 0.5), (730, 50))
            
        pygame.display.flip()
        clock.tick(40)
        
        if number_of_selected == 6:
            return player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images
        
def map_randomizer() -> object:
    # Variables to be used for map randomizer / Next screen ( To avoid multiple declaration )
    map_names = ["Viridale Forest", "Dragon Dungeon", "Bamboo Bridge"]
    map_index = random.randint(0, len(map_names)-1) # Random starting map
    starting_show_speed = 0.05
    is_map_final = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()
                
        current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{map_index}.png"), (800,600))
        screen.blit(current_background, (0,0))
        show_text(map_names[map_index], 400, 50, screen)
        
        if not is_map_final:
            starting_show_speed *= 1.1
            map_index = (map_index + 1) % len(map_names)
            time.sleep(starting_show_speed)
            if starting_show_speed >= 1.2:
                return current_background
        
        # Update the screen
        pygame.display.flip()
        # fps
        clock.tick(60)
        
def fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battleeffects_frames, current_background) -> None:
    # Preparation for next screen to avoid multiple declaration
    match_number = 0
    another_round = False
    attacking = False
    current_pokemon_index = (match_number) % 3
    player_1_pokemon = player1_pokemons[current_pokemon_index]
    player_2_pokemon = player2_pokemons[current_pokemon_index]
    x_pos = 0
    player1_pokemon_frame_index = [0 for _ in range(len(player1_pokemons))]
    player2_pokemon_frame_index = [0 for _ in range(len(player2_pokemons))]
    
    # Set up index to be used for each frame
    index = 0

    # Load up projectiles to be used by both pokemons
    for num in range(len(battle_effects)):
        if battle_effects[num].type == player_1_pokemon.type:
            player_1_battle_effect_image = battleeffects_frames[num]
            player_1_battle_effect_index = 0
        elif battle_effects[num].type == player_2_pokemon.type:
            player_2_battle_effect_image = battleeffects_frames[num]
            player_2_battle_effect_index = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()
                
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
                show_text(f"{player_1_pokemon.name if player_1_pokemon.power > player_2_pokemon.power else player_2_pokemon.name} overwhelmes {player_2_pokemon.name if player_2_pokemon.power > player_1_pokemon.power else player_1_pokemon.name}", screen.get_width() // 2, screen.get_height() + 500, screen)
            
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

def main():
    pokemon_loaded_images, battle_effects_loaded_images = load_images()
    player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images = pokemon_selection_scene(pokemon_loaded_images)
    current_background = map_randomizer()
    fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battle_effects_loaded_images, current_background)    
    

main()