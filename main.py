import pygame
from pokemon import *
import random, time
from battleeffects import *
from utility import *

# Data Structures
from data_structures.linked_list import *
from data_structures.queue import *

# for asynchronous operation (loading screen)
import threading
# this solves the slowness of threading
from concurrent.futures import ThreadPoolExecutor


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Team Rocket's Pokemon Game")
pygame.display.set_icon(scale(pygame.image.load("assets/Team-Rocket-Logo/Rocket-Logo.png"), 2))

# Global initialization
pokemons = [bulbasaur, charizard, blastoise, weepinbell, arcanine, psyduck, scyther, magmar, poliwrath, farfetchd, moltres, vaporeon]
original_pokemons = pokemons[:]
battle_effects = [fireball, waterball, grassball, pokeball]

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
    image = pygame.image.load("assets/Loading-Screen/Loading-Screen(v1)(630).png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Render loading  screen
        screen.blit(image, (0,-25))
        
        pygame.display.update()
        
        if loading_complete:
            return pokemon_loaded_images, battle_effects_loaded_images

def pokemon_selection_scene(pokemon_loaded_images: list, battle_effect_loaded_images: list) -> list:
    # Creates the linked list
    player1_linkedlist = LinkedList()
    player2_linkedlist = LinkedList()
    
    # Frame index to track animation progress
    pokemon_frame_index = [0 for _ in range(len(pokemons))]
    
    # Initialization
    focus = 0
    number_of_selected = 0
    background_image_p1 = pygame.transform.scale(pygame.image.load("assets/layout/pick-p1-highlight.png"), (800, 600))
    background_image_p2 = pygame.transform.scale(pygame.image.load("assets/layout/pick-p2-highlight.png"), (800, 600))
    arrow_left_state_counter = 0
    arrow_right_state_counter = 0
    select_button_state_counter = 0
    player1_loaded_images = []
    player2_loaded_images = [] 
    
    pokeball_effect_frame_index = 0
    
    
    def select_pokemon(number_of_selected, focus):
        if number_of_selected % 2 == 0:
            # Save the selected Pokémon for player1
            player1_loaded_images.append(pokemon_loaded_images[focus])
            
            # add the pokemon to the linked list
            player1_linkedlist.atend(pokemons[focus])
        else:
            # Save the selected Pokemon for player
            player2_loaded_images.append(pokemon_loaded_images[focus])
            
            # add the pokemon to the linked list
            player2_linkedlist.atend(pokemons[focus])
            
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
        pokeball_image = scale(battle_effect_loaded_images[3][pokeball_effect_frame_index], 0.15)
        if number_of_selected % 2 == 0:
            screen.blit(background_image_p1, (0, 0))
            pokeball_image_rect = pokeball_image.get_rect(topleft=(100, -15))
        else:
            screen.blit(background_image_p2, (0, 0))
            pokeball_image_rect = pokeball_image.get_rect(topleft=(570, -15))
        screen.blit(pokeball_image, pokeball_image_rect)
        pokeball_effect_frame_index = (pokeball_effect_frame_index + 1) % len(battle_effect_loaded_images[3])

        # Scale Pokemon images
        pokemon1_image = scale(apply_brightness(pokemon_loaded_images[prev_index][pokemon_frame_index[prev_index]]), 1.1)
        pokemon2_image = scale(pokemon_loaded_images[focus][pokemon_frame_index[focus]], 1.9)
        pokemon3_image = scale(apply_brightness(pokemon_loaded_images[next_index][pokemon_frame_index[next_index]]), 1.1)

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
        show_text(pokemons[focus].name, 265, 485, screen, 30, "topleft", color="Black")
        screen.blit(scale(pygame.image.load(f"assets/type-icons/{pokemons[focus].type}.png"), 0.5), (550, 480))
        show_text(f"Power  : {pokemons[focus].power}", 236, 530, screen, 25, "topleft", color="Black")
        show_text(f"Health : {pokemons[focus].health}", 235, 565, screen, 25, "topleft", color="Black")
        if pokemons[focus].type == "Water":
            screen.blit(pygame.image.load("assets/Bar/Bar-Mid.png"), (370, 535))
            screen.blit(pygame.image.load("assets/Bar/Bar-Mid.png"), (370, 570))
        elif pokemons[focus].type == "Fire":
            screen.blit(pygame.image.load("assets/Bar/Bar-Long.png"), (370, 535))
            screen.blit(pygame.image.load("assets/Bar/Bar-Short.png"), (370, 570))
        elif pokemons[focus].type == "Grass":
            screen.blit(pygame.image.load("assets/Bar/Bar-Short.png"), (370, 535))
            screen.blit(pygame.image.load("assets/Bar/Bar-Long.png"), (370, 570))
            
        # Update animation frames
        for i in range(len(pokemon_frame_index)):
            pokemon_frame_index[i] = (pokemon_frame_index[i] + 1) % len(pokemon_loaded_images[i])
            
        # Conditional Rendering for icons using linked list operations
        if player1_linkedlist.count() >= 1:
            screen.blit(scale(pygame.image.load(player1_linkedlist.get_data_at(1).icon), 0.5), (20, 55))
        if player2_linkedlist.count() >= 1:
            screen.blit(scale(pygame.image.load(player2_linkedlist.get_data_at(1).icon), 0.5), (650, 55))
        if player1_linkedlist.count() >= 2:
            screen.blit(scale(pygame.image.load(player1_linkedlist.get_data_at(2).icon), 0.5), (70, 55))
        if player2_linkedlist.count() >= 2:
            screen.blit(scale(pygame.image.load(player2_linkedlist.get_data_at(2).icon), 0.5), (700, 55))
        if player1_linkedlist.count() >= 3:
            screen.blit(scale(pygame.image.load(player1_linkedlist.get_data_at(3).icon), 0.5), (120, 55))
        if player2_linkedlist.count() >= 3:
            screen.blit(scale(pygame.image.load(player2_linkedlist.get_data_at(3).icon), 0.5), (750, 55))
            
        pygame.display.flip()
        clock.tick(40)
        
        if number_of_selected == 6:
            
            # Creates the Queue
            player1_pokemons_queue = Queue()
            player2_pokemons_queue = Queue()
            
            # Convert the linked list data to a Queue
            for data in player1_linkedlist.show_data():
                player1_pokemons_queue.enqueue(data)
            for data in player2_linkedlist.show_data():
                player2_pokemons_queue.enqueue(data)
            
            # pass the queue for the next scene    
            return player1_pokemons_queue, player1_loaded_images, player2_pokemons_queue, player2_loaded_images
        
def map_randomizer() -> object:
    # Variables to be used for map randomizer / Next screen ( To avoid multiple declaration )
    map_names = ["Viridale Forest", "Dragon Dungeon", "Bamboo Bridge"]
    map_index = random.choice(map_names) # Random starting map
    starting_show_speed = 0.05
    is_map_final = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{map_index}.png"), (800,600))
        screen.blit(current_background, (0,0))
        show_text(map_index, 400, 50, screen)
        
        if not is_map_final:
            unselected_maps = [name for name in map_names if name != map_index]
            starting_show_speed *= 1.5
            map_index = random.choice(unselected_maps) # Randomly select a map again
            time.sleep(starting_show_speed)
            if starting_show_speed >= 1.2:
                current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battle_Scene/{map_index}.png"), (800,600))
                return current_background
        
        # Update the screen
        pygame.display.flip()
        # fps
        clock.tick(60)
        
def fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battleeffects_frames, current_background) -> None:
    # Preparation for next screen to avoid multiple declaration
    match_number = 0
    another_round = False
    ready = False
    current_pokemon_index = (match_number) % 3
    player_1_pokemon = player1_pokemons[current_pokemon_index]
    player_2_pokemon = player2_pokemons[current_pokemon_index]
    x_pos = 0
    player1_pokemon_frame_index = [0 for _ in range(len(player1_pokemons))]
    player2_pokemon_frame_index = [0 for _ in range(len(player2_pokemons))]
    menu_options = ["Ready", "Potion", "Poison", "Run"]
    option_description = ["Get ready for\n battle", "Recover Health\n Points", "Inflict Damage\n to Enemy", "Conclude the\n battle"]
    # Set up index to be used for each frame
    index = 0
    player1_menu_option_index = 0
    player2_menu_option_index = 0

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
            if event.type == pygame.KEYDOWN:
                # Controls for Player 1
                if event.key == pygame.K_w:
                    player1_menu_option_index = (player1_menu_option_index - 2) % 4
                if event.key == pygame.K_s:
                    player1_menu_option_index = (player1_menu_option_index + 2) % 4
                if event.key == pygame.K_a:
                    player1_menu_option_index = (player1_menu_option_index - 1) % 4
                if event.key == pygame.K_d:
                    player1_menu_option_index = (player1_menu_option_index + 1) % 4
                if event.key == pygame.K_SPACE:
                    pass
                # Controls for Player 2
                if event.key == pygame.K_UP:
                    player2_menu_option_index = (player2_menu_option_index - 2) % 4
                if event.key == pygame.K_DOWN:
                    player2_menu_option_index = (player2_menu_option_index + 2) % 4
                if event.key == pygame.K_LEFT:
                    player2_menu_option_index = (player2_menu_option_index - 1) % 4
                if event.key == pygame.K_RIGHT:
                    player2_menu_option_index = (player2_menu_option_index + 1) % 4
        if another_round:
            match_number += 1
            another_round = False
        
        current_pokemon_index = (match_number) % 3

        # Display chosen background
        screen.blit(current_background, (0,0))
        ready = False

        # To show what the current match number is
        show_text(f"Match {match_number+1}", screen.get_width() // 2, 57, screen, 40)

        # To show the name of pokemon in the current match
        show_text(player_1_pokemon.name, 55, 34, screen, 20, "midleft")
        show_text(player_2_pokemon.name, 600, 34, screen, 20, "midleft")

        # Just for trying purposes
        player_1_pokemon.remaining_health = player_1_pokemon.health - 40
        # To show the Health Points Bar of the Pokemons
        hp_bar = scale(pygame.image.load("./assets/Battle_Scene/hp_bar.png"), .5)
        # For player 1
        player1_grn_pcnt = (player_1_pokemon.remaining_health/player_1_pokemon.health)*92
        pygame.draw.rect(screen, "#d8483a", (117, 53, 92, 6), border_radius= 3)
        pygame.draw.rect(screen, "#7df39d", (117, 53, player1_grn_pcnt, 6), border_radius= 3)

        
        
        # For player 2
        player2_grn_pcnt = (player_2_pokemon.remaining_health/player_2_pokemon.health)*92
        pygame.draw.rect(screen, "#d8483a", (657, 53, 92, 6), border_radius= 3)
        pygame.draw.rect(screen, "#7df39d", (657, 53, player2_grn_pcnt, 6), border_radius= 3)
        
        player1_hp_bar_rect = hp_bar.get_rect(topleft = (80, 47))
        player2_hp_bar_rect = hp_bar.get_rect(topleft = (620, 47))

        screen.blit(hp_bar, player1_hp_bar_rect)
        screen.blit(hp_bar, player2_hp_bar_rect)

        # To show the Health Points of the Pokemons (Text)
        show_text(f"{player_1_pokemon.remaining_health}/{player_1_pokemon.health}", 140, 69, screen, 20, "midleft")
        show_text(f"{player_2_pokemon.remaining_health}/{player_2_pokemon.health}", 690, 69, screen, 20, "midleft")
        
        # For showing player 1 and player 2 menu
        for i in range(len(menu_options)):
            y = 515
            if i > 1:
                y = 550
            
            player1_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20))
            player2_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20))
            
            player1_text = option_description[player1_menu_option_index].split("\n")
            player1_text_xpos, player1_text_ypos = 95, 520
            for line in player1_text:
                show_text(line, player1_text_xpos, player1_text_ypos, screen, 20, "center")
                player1_text_ypos += 20
            # show_text(option_description[player1_menu_option_index], 30, 500, screen, 20, "topleft")

            player2_text = option_description[player2_menu_option_index].split("\n")
            player2_text_xpos, player2_text_ypos = 515, 520
            for line in player2_text:
                show_text(line, player2_text_xpos, player2_text_ypos, screen, 20, "center")
                player2_text_ypos += 20
            if player1_menu_option_index == i:
                show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft", True)
                arrow_img_rect = player1_arrow_img.get_rect(midleft = (190 + ((i+2)%2)*80, y))
                screen.blit(player1_arrow_img, arrow_img_rect)
            else:
                show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft")
            if player2_menu_option_index == i:
                show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft", True)
                arrow_img_rect = player2_arrow_img.get_rect(midleft = (610 + ((i+2)%2)*80, y))
                screen.blit(player2_arrow_img, arrow_img_rect)
            else:
                show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft")
        if ready:
            # Get current frames, resize and rotate them 
            player_1_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_1_battle_effect_image[player_1_battle_effect_index], -90), tuple([measure * 0.3 for measure in player_1_battle_effect_image[index].get_size()]))
            player_2_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_2_battle_effect_image[player_2_battle_effect_index], 90), tuple([measure * 0.3 for measure in player_2_battle_effect_image[index].get_size()]))
            # Position each
            player_1_battle_effect_current_img_rect = player_1_battle_effect_current_img.get_rect(midbottom = ((screen.get_width() // 2 - 200 ) + x_pos, screen.get_height() // 2 + 110 ))
            player_2_battle_effect_current_img_rect = player_2_battle_effect_current_img.get_rect(midbottom = ((screen.get_width() // 2 + 200) - x_pos, screen.get_height() // 2 + 110))

            # Increment x to make each image closer to middle ( 400 )
            x_pos += 1
            if player_1_battle_effect_current_img_rect.colliderect(player_2_battle_effect_current_img_rect):
                show_text(f"{player_1_pokemon.name if player_1_pokemon.power > player_2_pokemon.power else player_2_pokemon.name} overwhelmes {player_2_pokemon.name if player_2_pokemon.power > player_1_pokemon.power else player_1_pokemon.name}", screen.get_width() // 2, 400, screen)
                print("Collision")
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

        # Used for knowing specific locations in the screen
        # mouse_pos = pygame.mouse.get_pos()
        # print(f"Position: {mouse_pos}")
        pygame.display.flip()
        clock.tick(40)

def main():
    pokemon_loaded_images, battle_effects_loaded_images = load_images()
    player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images = pokemon_selection_scene(pokemon_loaded_images, battle_effects_loaded_images)
    current_background = map_randomizer()
    fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battle_effects_loaded_images, current_background)    
    
main()