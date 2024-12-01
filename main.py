import pygame
from pokemon import *
import random, time
from battleeffects import *
from utility import *

# Data Structures
from data_structures.linked_list import *
from data_structures.queue import *
from data_structures.stack import *
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
    map_types = ["Grass", "Fire", "Water"]
    starting_show_speed = 0.05
    selected_map = random.choice(map_names)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(starting_show_speed)
        
        random_map = random.choice(map_names) # Randomly select a map again        
        current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{random_map}.png"), (800,600))
        screen.blit(current_background, (0,0))
        show_text(random_map, 400, 50, screen)
        
        starting_show_speed *= 1.5
        if starting_show_speed >= 2:
            screen.blit(pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{selected_map}.png"), (800,600)), (0,0))
            current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battle_Scene/{selected_map}.png"), (800,600))
            time.sleep(1)
            return current_background, map_types[map_names.index(random_map)]
        
        
        # Update the screen
        pygame.display.flip()
        # fps
        clock.tick(60)
        
def fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battleeffects_frames, current_background, map_type) -> None:
    # Preparation for next screen to avoid multiple declaration

    # Queue for Executing Potion Healings and Poison Damages
    consumables_queue = Queue() 
    # Stack for Executing Buffs and Nerfs
    buffs_stack = Stack()
    match_number = 0
    another_round = False
    player1_ready = False
    player2_ready = False
    current_pokemon_index = (match_number) % 3
    player_1_pokemon = player1_pokemons.dequeue()
    player_2_pokemon = player2_pokemons.dequeue()

    if player_1_pokemon.type == map_type:
        buffs_stack.push(1) # Number means the player number
    if player_2_pokemon.type == map_type:
        buffs_stack.push(2) 
    x_pos = 0
    player1_pokemon_frame_index = [0 for _ in range(player1_pokemons.size())]
    player2_pokemon_frame_index = [0 for _ in range(player1_pokemons.size())]
    menu_options = ["Ready", "Potion", "Poison", "Run"]
    option_description = ["Get ready for\n battle", "Recover Health\n Points", "Inflict Damage\n to Enemy", "Conclude the\n battle"]
    # Set up index to be used for each frame
    index = 0
    player1_menu_option_index = 0
    player2_menu_option_index = 0
    player1_show_confirmation = False
    player1_confirmation_index = 0
    player2_show_confirmation = False
    player2_confirmation_index = 0
    confirmation_messages = ["Are you sure\nyou want to\nget ready?", "Using a potion will\nheal 20 health\npoints", "Using a poison will\ndeal 20 health\npoints to enemy", "Are you sure you\nwant to end now?"]

    player1_failmsg = False # For Fail in Run Option
    player2_failmsg = False

    player1_failpot = False # For Fail in Potion Option
    player2_failpot = False

    player1_failpoi = False # For Fail in Poison Option
    player2_failpoi = False 

    failmsg_timer = 3000 # 3 seconds in milliseconds
    player1timer = None # None state if timer is stopped
    player2timer = None

    player1_usedpotion = False
    player2_usedpotion = False

    player1_usedpoison = False
    player2_usedpoison = False

    fight_dia_timer = None
    fight_dia_duration = 8000
    collision = False
    tobe_printed_msg = ""
    msg_index = 0
    disable_player1_proj = False
    disable_player2_proj = False
    player1_damage_counter = 0
    player2_damage_counter = 0
    deduct_player1_hp = False
    deduct_player2_hp = False
    dmg_interval = 500
    player_1_dmg_time = 0
    player_2_dmg_time = 0
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
                    if not player1_show_confirmation:
                        player1_menu_option_index = (player1_menu_option_index - 2) % 4
                    else:
                        player1_confirmation_index = (player1_confirmation_index+1) % 2
                if event.key == pygame.K_s:
                    if not player1_show_confirmation:
                        player1_menu_option_index = (player1_menu_option_index + 2) % 4
                    else:
                        player1_confirmation_index = (player1_confirmation_index + 1) % 2
                if event.key == pygame.K_a:
                    if not player1_show_confirmation:
                        player1_menu_option_index = (player1_menu_option_index - 1) % 4
                    else:
                        player1_confirmation_index = (player1_confirmation_index + 1) % 2
                if event.key == pygame.K_d:
                    if not player1_show_confirmation:
                        player1_menu_option_index = (player1_menu_option_index + 1) % 4
                    else:
                        player1_confirmation_index = (player1_confirmation_index + 1) % 2

                if event.key == pygame.K_SPACE:
                    if player1_show_confirmation:
                        if player1_confirmation_index == 1 :
                            player1_show_confirmation = False 
                        elif player1_confirmation_index == 0:
                            if player1_menu_option_index == 0:
                                player1_ready = True
                            elif player1_menu_option_index == 1:
                                consumables_queue.enqueue("Player 1 Used Potion")
                                player1_show_confirmation = False
                                player1_usedpotion = True
                            elif player1_menu_option_index == 2:
                                consumables_queue.enqueue("Player 1 Used Poison")
                                player1_show_confirmation = False
                                player1_usedpoison = True
                            elif player1_menu_option_index == 3:
                                player1timer = pygame.time.get_ticks()
                                # Not yet implemented
                                all_pokemon_used = False
                                player1_failmsg = True
                                if not all_pokemon_used:
                                    player1_show_confirmation = False

                    else:
                        if player1_menu_option_index == 1 and player1_usedpotion:
                            player1_failpot = True
                            player1timer = pygame.time.get_ticks()
                        elif player1_menu_option_index == 2 and player1_usedpoison:
                            player1_failpoi = True
                            player1timer = pygame.time.get_ticks()

                        else:
                            player1_show_confirmation = True
                # Controls for Player 2
                if event.key == pygame.K_UP:
                    if not player2_show_confirmation:
                        player2_menu_option_index = (player2_menu_option_index - 2) % 4
                    else:
                        player2_confirmation_index = (player2_confirmation_index + 1) % 2
                    
                if event.key == pygame.K_DOWN:
                    if not player2_show_confirmation:
                        player2_menu_option_index = (player2_menu_option_index + 2) % 4
                    else:
                        player2_confirmation_index = (player2_confirmation_index + 1) % 2
                if event.key == pygame.K_LEFT:
                    if not player2_show_confirmation:
                        player2_menu_option_index = (player2_menu_option_index - 1) % 4
                    else:
                        player2_confirmation_index = (player2_confirmation_index + 1) % 2
                if event.key == pygame.K_RIGHT:
                    if not player2_show_confirmation:
                        player2_menu_option_index = (player2_menu_option_index + 1) % 4
                    else:
                        player2_confirmation_index = (player2_confirmation_index + 1) % 2
                if event.key == pygame.K_RETURN:
                    if player2_show_confirmation:
                        if player2_confirmation_index == 1 :
                            player2_show_confirmation = False 
                        elif player2_confirmation_index == 0:
                            if player2_menu_option_index == 0:
                                player2_ready = True 
                            elif player2_menu_option_index == 1:
                                consumables_queue.enqueue("Player 2 Used Potion")
                                player2_show_confirmation = False
                                player2_usedpotion = True
                            elif player2_menu_option_index == 2:
                                consumables_queue.enqueue("Player 2 Used Poison")
                                player2_show_confirmation = False
                                player2_usedpoison = True
                            elif player2_menu_option_index == 3:
                                # Not yet implemented
                                all_pokemon_used = False
                                player2timer = pygame.time.get_ticks()
                                player2_failmsg = True
                                if not all_pokemon_used:
                                    player2_show_confirmation = False
                                    
                    else:
                        if player2_menu_option_index == 1 and player2_usedpotion:
                            player2_failpot = True
                            player2timer = pygame.time.get_ticks()
                        elif player2_menu_option_index == 2 and player2_usedpoison:
                            player2_failpoi = True
                            player2timer = pygame.time.get_ticks()
                        else:
                            player2_show_confirmation = True
        if another_round:
            match_number += 1
            another_round = False
        
        current_pokemon_index = (match_number) % 3

        # Display chosen background
        screen.blit(current_background, (0,0))
        ready = False

        # To show what the current match number is
        show_text(f"Match {match_number+1}", screen.get_width() // 2, 57, screen, 40, color = "#4ddf6f")

        # To show the name of pokemon in the current match
        show_text(player_1_pokemon.name, 55, 34, screen, 20, "midleft", color = "#4ddf6f")
        show_text(player_2_pokemon.name, 600, 34, screen, 20, "midleft", color = "#4ddf6f")

        # Just for trying purposes
        # player_1_pokemon.remaining_health -= 1
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
        show_text(f"{player_1_pokemon.remaining_health}/{player_1_pokemon.health}", 140, 69, screen, 20, "midleft", color = "#4ddf6f")
        show_text(f"{player_2_pokemon.remaining_health}/{player_2_pokemon.health}", 690, 69, screen, 20, "midleft", color = "#4ddf6f")
        
        # Loading of Arrow Image
        player1_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20))
        player2_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20)) 

        # Display when player 1 is ready
        if player1_ready:
            show_text("READY", 110, 520, screen, 35, color= "#4ddf6f")
            show_text("READY", 260, 520, screen, 35, color= "#4ddf6f")
        # Menu when confirming an action for player 1
        elif player1_show_confirmation:
            player1_text = confirmation_messages[player1_menu_option_index].split("\n") 
            player1_text_xpos, player1_text_ypos = 95, 510
            for line in player1_text:
                show_text(line, player1_text_xpos, player1_text_ypos, screen, 20, "center", color = "#4ddf6f")
                player1_text_ypos += 20
            if player1_confirmation_index == 0:
                show_text("Yes", 210, 510, screen, 20, "midleft",highlight= True, color = "#4ddf6f")
                player1_arrow_img_rect = player1_arrow_img.get_rect(midleft = (190, 510))
                screen.blit(player1_arrow_img, player1_arrow_img_rect)
            else:
                show_text("Yes", 210, 510, screen, 20, "midleft", color = "#4ddf6f")
            if player1_confirmation_index == 1:
                show_text("No", 280, 510, screen, 20, "midleft",highlight= True, color = "#4ddf6f")
                player1_arrow_img_rect = player1_arrow_img.get_rect(midleft = (260, 510))
                screen.blit(player1_arrow_img, player1_arrow_img_rect)
            else:
                show_text("No", 280, 510, screen, 20, "midleft",color = "#4ddf6f")

         # For showing player 1 menu
        else:
            for i in range(len(menu_options)):
                y = 515
                if i > 1:
                    y = 550
                
                # Option Description for Player 1
                if player1_failmsg:
                    if player1timer and pygame.time.get_ticks() - player1timer  < failmsg_timer:
                        player1_text = "You cannot run\nyet.".split("\n")
                    else:
                        player1_text = option_description[player1_menu_option_index].split("\n")
                        player1_failmsg = False
                elif player1_failpot:
                    if player1timer and pygame.time.get_ticks() - player1timer  < failmsg_timer:
                        player1_text = "You already used\nyour potion.".split("\n")
                    else:
                        player1_text = option_description[player1_menu_option_index].split("\n")
                        player1_failpot = False
                elif player1_failpoi:
                    if player1timer and pygame.time.get_ticks() - player1timer  < failmsg_timer:
                        player1_text = "You already used\nyour poison.".split("\n")
                    else:
                        player1_text = option_description[player1_menu_option_index].split("\n")
                        player1_failpoi = False
                else:
                    player1_text = option_description[player1_menu_option_index].split("\n")
                player1_text_xpos, player1_text_ypos = 96, 520
                for line in player1_text:
                    show_text(line, player1_text_xpos, player1_text_ypos, screen, 20, "center", color = "#4ddf6f")
                    player1_text_ypos += 20
                
                if player1_menu_option_index == i:
                    show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft", True, color = "#4ddf6f")
                    arrow_img_rect = player1_arrow_img.get_rect(midleft = (190 + ((i+2)%2)*80, y))
                    screen.blit(player1_arrow_img, arrow_img_rect)
                else:
                    show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft", color = "#4ddf6f")

        if player2_ready:
            show_text("READY", 530, 530, screen, 35, color= "#4ddf6f")
            show_text("READY", 700, 530, screen, 35, color= "#4ddf6f")
        # Menu when confirming an action for player 2
        elif player2_show_confirmation:
            player2_text = confirmation_messages[player2_menu_option_index].split("\n")
            player2_text_xpos, player2_text_ypos = 518, 510
            for line in player2_text:
                show_text(line, player2_text_xpos, player2_text_ypos, screen, 20, "center", color = "#4ddf6f")
                player2_text_ypos += 20
            if player2_confirmation_index == 0:
                show_text("Yes", 630, 510, screen, 20, "midleft",highlight= True, color = "#4ddf6f")
                player2_arrow_img_rect = player2_arrow_img.get_rect(midleft = (610, 510))
                screen.blit(player2_arrow_img, player2_arrow_img_rect)
            else:
                show_text("Yes", 630, 510, screen, 20, "midleft", color = "#4ddf6f")
            if player2_confirmation_index == 1:
                show_text("No", 700, 510, screen, 20, "midleft",highlight= True, color = "#4ddf6f")
                player2_arrow_img_rect = player2_arrow_img.get_rect(midleft = (780, 510))
                screen.blit(player2_arrow_img, player2_arrow_img_rect)
            else:
                show_text("No", 700, 510, screen, 20, "midleft",color = "#4ddf6f")
        else:
            # For showing player 2 menu
            for i in range(len(menu_options)):
                y = 515
                if i > 1:
                    y = 550

                # Option Description for Player 2
                if player2_failmsg:
                    if player2timer and pygame.time.get_ticks() - player2timer  < failmsg_timer:
                        player2_text = "You cannot run\nyet.".split("\n")
                    else:
                        player2_text = option_description[player1_menu_option_index].split("\n")
                        player2_failmsg = False
                elif player2_failpot:
                    if player2timer and pygame.time.get_ticks() - player2timer  < failmsg_timer:
                        player2_text = "You already used\nyour potion.".split("\n")
                    else:
                        player2_text = option_description[player2_menu_option_index].split("\n")
                        player2_failpot = False
                elif player2_failpoi:
                    if player2timer and pygame.time.get_ticks() - player2timer  < failmsg_timer:
                        player2_text = "You already used\nyour poison.".split("\n")
                    else:
                        player2_text = option_description[player2_menu_option_index].split("\n")
                        player2_failpoi = False
                else:
                    player2_text = option_description[player2_menu_option_index].split("\n")
                player2_text_xpos, player2_text_ypos = 515, 520
                for line in player2_text:
                    show_text(line, player2_text_xpos, player2_text_ypos, screen, 20, "center", color = "#4ddf6f")
                    player2_text_ypos += 20
                if player2_menu_option_index == i:
                    show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft", True, color = "#4ddf6f")
                    arrow_img_rect = player2_arrow_img.get_rect(midleft = (610 + ((i+2)%2)*80, y))
                    screen.blit(player2_arrow_img, arrow_img_rect)
                else:
                    show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft", color = "#4ddf6f")

        ready = player1_ready and player2_ready # to check if both player are ready

        if ready:
            if fight_dia_timer and pygame.time.get_ticks() - fight_dia_timer < fight_dia_duration:
                x_pos += 0
                if pygame.time.get_ticks() - fight_dia_timer < 5000:
                    show_text(str(random.randint(1, 150)),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    show_text(str(random.randint(1, 150)),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                else:
                    if msg_index < len(comparison_msg):
                        tobe_printed_msg += comparison_msg[msg_index]
                        msg_index = (msg_index + 1) if msg_index < len(comparison_msg) else len(comparison_msg)
                    show_text(tobe_printed_msg, screen.get_width()//2 , 470, screen, 20, origin= "center")
                    show_text(str(player_1_pokemon.power),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    show_text(str(player_2_pokemon.power),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                    
                    
            else:
                if collision:
                    x_pos += 3
                    if player_1_pokemon.power > player_2_pokemon.power:
                        disable_player2_proj = True
                    else:
                        disable_player1_proj = True
                    fight_dia_timer = None
                # Increment x to make each image closer to middle ( 400 )
                x_pos += 2
                
            # Get current frames, resize and rotate them 
            player_1_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_1_battle_effect_image[player_1_battle_effect_index], -90), tuple([measure * 0.5 for measure in player_1_battle_effect_image[player_1_battle_effect_index].get_size()]))
            player_2_battle_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_2_battle_effect_image[player_2_battle_effect_index], 90), tuple([measure * 0.5 for measure in player_2_battle_effect_image[player_2_battle_effect_index].get_size()]))
            
        
            # Draw them each
            if not disable_player1_proj:
                player_1_battle_effect_current_img_rect = player_1_battle_effect_current_img.get_rect(center = ((screen.get_width() // 2 - 200 ) + x_pos, screen.get_height() // 2 + 110 ))
                screen.blit(player_1_battle_effect_current_img, player_1_battle_effect_current_img_rect)
            if not disable_player2_proj:
                player_2_battle_effect_current_img_rect = player_2_battle_effect_current_img.get_rect(center = ((screen.get_width() // 2 + 200) - x_pos, screen.get_height() // 2 + 110))
                screen.blit(player_2_battle_effect_current_img, player_2_battle_effect_current_img_rect)
            # Update each index for the battle effect frame
            player_1_battle_effect_index = (player_1_battle_effect_index + 1) % len(player_1_battle_effect_image)
            player_2_battle_effect_index = (player_2_battle_effect_index + 1) % len(player_2_battle_effect_image)
            if player_1_battle_effect_current_img_rect.colliderect(player_2_battle_effect_current_img_rect):
                comparison_msg = (f"{player_1_pokemon.name if player_1_pokemon.power > player_2_pokemon.power else player_2_pokemon.name} overwhelmes {player_2_pokemon.name if player_2_pokemon.power < player_1_pokemon.power else player_1_pokemon.name}")
                if not collision:
                    fight_dia_timer = pygame.time.get_ticks()
                    collision = True
            
            if player_1_battle_effect_current_img_rect.colliderect(player_2_pokemon_rect):
                if not deduct_player2_hp:
                    deduct_player2_hp = True
                    disable_player1_proj = True
            elif player_2_battle_effect_current_img_rect.colliderect(player_1_pokemon_rect):
                if not deduct_player1_hp:
                    deduct_player1_hp = True
                    disable_player2_proj = True

            if deduct_player2_hp:
                if pygame.time.get_ticks() - player_2_dmg_time >= dmg_interval and player1_damage_counter < 10 :
                    player1_damage_counter +=1
                    player_2_pokemon.remaining_health -= 1
                if player1_damage_counter >= 10:
                    player1_damage_counter = 10
                    deduct_player2_hp = False
            elif deduct_player1_hp:
                if pygame.time.get_ticks() - player_1_dmg_time >= dmg_interval and player2_damage_counter < 10:
                    player2_damage_counter += 1
                    player_1_pokemon.remaining_health -= 1
                if player2_damage_counter >= 10:
                    player2_damage_counter = 10
                    deduct_player1_hp = False

            

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
    current_background, map_type = map_randomizer()
    fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battle_effects_loaded_images, current_background, map_type)    
    
main()