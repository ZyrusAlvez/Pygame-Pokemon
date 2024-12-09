import pygame
from pokemon import *
import random, time
from battleeffects import *
from utility import *

# Data Structures
from data_structures.linked_list import *
from data_structures.queue import *
from data_structures.stack import *
from data_structures.binary_tree import *

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
pygame.mixer.init()

# Global initialization
pokemons = [bulbasaur, charizard, blastoise, weepinbell, arcanine, psyduck, scyther, magmar, piplup, farfetchd, moltres, vaporeon]
original_pokemons = pokemons[:]
battle_effects = [fireball, waterball, grassball, pokeball, fainted, heal_player]
impact_effects = [firefx, waterfx, grassfx]
potion_poison_effects = [potion, poison]
transitions = [opening, closing]
# Global Variable
player1_usedpotion = False
player2_usedpotion = False
player1_usedpoison = False
player2_usedpoison = False
player1_default_pokemom_names = []
player2_default_pokemom_names = []

# this requires a lot of time to load
def load_images() -> list:
    loading_complete = False

    def load_images_task():
        nonlocal loading_complete
        global pokemon_loaded_images, battle_effects_loaded_images, impact_effects_loaded_images, potion_poison_effects_loaded_images, transitions_loaded_images
        
        def load_pokemon_frames(pokemon):
            return [pygame.image.load(frame) for frame in pokemon.animation_frames()]

        def load_effect_frames(effect):
            return [pygame.image.load(frame) for frame in effect.animation_frames()]
        
        def load_impact_frames(impact):
            return [pygame.image.load(frame) for frame in impact.animation_frames()]

        def load_potion_poison_frames(potion_poison):
            return [pygame.image.load(frame) for frame in potion_poison.animation_frames()]
        
        def load_transition_frames(transitions):
            return [pygame.image.load(frame) for frame in transitions.animation_frames()]

        # Use ThreadPoolExecutor to load frames in parallel
        with ThreadPoolExecutor() as executor:
            pokemon_loaded_images = list(executor.map(load_pokemon_frames, pokemons))
            battle_effects_loaded_images = list(executor.map(load_effect_frames, battle_effects))
            impact_effects_loaded_images = list(executor.map(load_impact_frames, impact_effects))
            potion_poison_effects_loaded_images = list(executor.map(load_potion_poison_frames, potion_poison_effects))
            transitions_loaded_images = list(executor.map(load_transition_frames, transitions))
        loading_complete = True

    # Start loading images in a thread
    loading_thread = threading.Thread(target=load_images_task)
    loading_thread.start()

    pygame.mixer.music.load("assets/audio/pokemon-loadingscreen.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    image = pygame.image.load("assets/Loading-Screen/Loading-Screen(v1)(630).png")
    
    loading_text = "Loading"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Render loading  screen
        screen.blit(image, (0,-25))
        show_text(loading_text, 300, 480, screen, origin="topleft")
        loading_text += "."
        if loading_text == "Loading.....":
            loading_text = "Loading"
        
        pygame.display.update()
        clock.tick(3)
        
        if loading_complete:
            pygame.mixer.music.stop()
            return pokemon_loaded_images, battle_effects_loaded_images, impact_effects_loaded_images, potion_poison_effects_loaded_images, transitions_loaded_images

def menu() -> None:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/pokemon-menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    background = pygame.image.load("assets/Menu-GUI/Menu.png")
    
    btn_play = scale(pygame.image.load("assets/Menu-GUI/PLAY-BUTTON.png"), 0.7)
    btn_play_rect = btn_play.get_rect(center=(600, 150))
    
    btn_exit = scale(pygame.image.load("assets/Menu-GUI/EXIT-BUTTON.png"), 0.7)
    btn_exit_rect = btn_exit.get_rect(center=(600, 350))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or pygame.K_SPACE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if click is inside the button
                if btn_play_rect.collidepoint(event.pos):  
                    return
                if btn_exit_rect.collidepoint(event.pos):
                    quit()  
            
        screen.blit(background, (0,0))
        screen.blit(btn_play, btn_play_rect)
        screen.blit(btn_exit, btn_exit_rect)
        
        pygame.display.update()
        clock.tick(40)
         
def pokemon_selection_scene(pokemon_loaded_images: list, battle_effect_loaded_images: list) -> list:
    # Initialize  music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/pokemon-selection.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    sound_arrow =  pygame.mixer.Sound("assets/audio/button-click.mp3")
    sound_arrow.set_volume(0.8)
    sound_select = pygame.mixer.Sound("assets/audio/select-audio.wav")
    sound_select.set_volume(0.8)

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
        selected_pokemon = pokemons[focus]

        if number_of_selected % 2 == 0:
            # Save the selected Pokémon for player1
            player1_loaded_images.append(pokemon_loaded_images[focus])
            
            # add the pokemon to the linked list
            player1_linkedlist.atend(selected_pokemon)
        else:
            # Save the selected Pokemon for player
            player2_loaded_images.append(pokemon_loaded_images[focus])
            
            # add the pokemon to the linked list
            player2_linkedlist.atend(selected_pokemon)
        
        selected_pokemon.play_audio()
        
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
                pygame.mixer.music.stop()
                for pokemon in original_pokemons:
                    pokemon.animation_clean_up()
                for battle_effect in battle_effects:
                    battle_effect.clear_residue()
                pygame.quit()
                exit()  
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                   sound_select.play()
                   updated_number_of_selected, updated_focus = select_pokemon(number_of_selected, focus)
                   focus = updated_focus
                   number_of_selected = updated_number_of_selected
                if event.key == pygame.K_RIGHT:
                    sound_arrow.play()
                    focus = (focus + 1) % len(pokemons)
                if event.key == pygame.K_LEFT:
                    sound_arrow.play()
                    focus = (focus - 1) % len(pokemons)
            pokemons[focus].play_audio()
            
            # Check if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if click is inside the button
                if arrow_left_rect.collidepoint(event.pos):  
                   sound_arrow.play()
                   focus = (focus - 1) % len(pokemons)
                   arrow_left_state_counter = 5
                if arrow_right_rect.collidepoint(event.pos):  
                   sound_arrow.play()
                   focus = (focus + 1) % len(pokemons)
                   arrow_right_state_counter = 5
                if select_button_rect.collidepoint(event.pos):  
                   sound_select.play()
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
        arrow_right_rect = arrow_right.get_rect(center=(570, 415))
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
        show_text(pokemons[focus].name, 265, 485, screen, 30, "topleft", color="Black", bold=True)
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
            pygame.mixer.music.stop()
            
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
        
def map_randomizer(transition_frames) -> object:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/map-pick.mp3")
    pygame.mixer.music.play(-1)

    # Variables to be used for map randomizer / Next screen ( To avoid multiple declaration )
    map_names = ["Viridale Forest", "Dragon Dungeon", "Bamboo Bridge"]
    map_types = ["Grass", "Fire", "Water"]
    starting_show_speed = 0.05
    selected_map = random.choice(map_names)
    
    randomization_time = pygame.time.get_ticks()
    transition_time = None
    randomize_map = True
    transition_anim_timer = None
    transition_frame_index = 0
    new_map_names = map_names
    black_surface = pygame.Surface(screen.get_size())
    black_surface.fill((0,0,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.mixer.music.stop()
                pygame.quit()
                exit()
        # equivalent of time.sleep(starting_show_speed)
        if pygame.time.get_ticks() - randomization_time <= starting_show_speed * 1000:
            pass
        else:
            if randomize_map:
                random_map = random.choice(new_map_names) # Randomly select a map again  
                new_map_names = [name for name in map_names if name != random_map]      
                current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{random_map}.png"), (800,600))
                screen.blit(current_background, (0,0))
                show_text(random_map, 400, 50, screen)
                starting_show_speed *= 1.23
                print(starting_show_speed)
                randomize_map = False
            if starting_show_speed >= 1:
                screen.blit(pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{selected_map}.png"), (800,600)), (0,0))
                show_text(selected_map, 400, 50, screen)
                current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battle_Scene/{selected_map}.png"), (800,600))
                if transition_time == None:
                    transition_time = pygame.time.get_ticks()
                # Equivalent of time.sleep(1)
                if pygame.time.get_ticks() - transition_time <= 1000:
                    pass
                else:
                    pygame.mixer.music.stop()
                    if transition_anim_timer == None:
                        transition_anim_timer = pygame.time.get_ticks()
                    if pygame.time.get_ticks() - transition_anim_timer <= 3000:
                        transition_current_img = pygame.transform.scale(transitions_loaded_images[1][transition_frame_index], (800,600))
                        transition_current_img_rect = transition_current_img.get_rect(topleft = (0,0))
                        if transition_frame_index < len(transitions_loaded_images[1])-3:
                            screen.blit(transition_current_img, transition_current_img_rect)
                            transition_frame_index += 1
                        else:
                            screen.blit(black_surface, (0,0))
                    else:
                        screen.blit(black_surface, (0,0))
                        return current_background, map_types[map_names.index(selected_map)]
            else:
                randomize_map = True
                randomization_time = pygame.time.get_ticks()
                

        
            # quit()
             
        # current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{map_names[i % 3]}.png"), (800,600))
        # screen.blit(current_background, (0,0))
        # show_text(map_names[i % 3], 400, 50, screen)

        
        # Update the screen
        pygame.display.flip()
        clock.tick(10)
            
    # screen.blit(pygame.transform.scale(pygame.image.load(f"./assets/Battleground/{selected_map}.png"), (800,600)), (0,0))
    # show_text(selected_map, 400, 50, screen, shadow_color="Black")
    # current_background = pygame.transform.scale(pygame.image.load(f"./assets/Battle_Scene/{selected_map}.png"), (800,600))
    # pygame.display.flip()   
    # time.sleep(1)
    
    # return current_background, map_types[map_names.index(selected_map)]
        
def fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battleeffects_frames, impacteffect_frames,potionpoison_frames,transition_frames, current_background, map_type, match_number, root_node) -> None:
    # Queue for Executing Potion Healings and Poison Damages
    consumables_queue = Queue() 
    # Stack for Executing Buffs and Nerfs
    buffs_stack = Stack()
    another_round = False
    player1_ready = False
    player2_ready = False
    print(len(battleeffects_frames))
    global player1_default_pokemon_names
    global player2_default_pokemon_names
    if match_number == 0:
        player1_default_pokemon_names = [i.name for i in player1_pokemons.queue]
        player2_default_pokemon_names = [i.name for i in player2_pokemons.queue]
    
    player_1_pokemon = player1_pokemons.dequeue()
    player_2_pokemon = player2_pokemons.dequeue()

    if player_1_pokemon.type == map_type:
        buffs_stack.push(1) # Number means the player number
    if player_2_pokemon.type == map_type:
        buffs_stack.push(2)
        
    x_pos = 0
    player1_pokemon_frame_index = [0 for _ in range(3)]
    player2_pokemon_frame_index = [0 for _ in range(3)]
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

    global player1_usedpotion
    global player2_usedpotion
    global player1_usedpoison
    global player2_usedpoison
    global impact_effects
    global potion_poison_effects

    p1_current_pokemon_index = player1_default_pokemon_names.index(player_1_pokemon.name)
    p2_current_pokemon_index = player2_default_pokemon_names.index(player_2_pokemon.name)
    
    fight_dia_timer = None
    fight_dia_duration = 10000
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

    player1_buff = False
    player2_buff = False

    player1_power_buff_counter = 0
    player2_power_buff_counter = 0

    post_battle = False
    post_battle_timer = False
    dequeue_timer = False
    action_done = True
    queue_duration = 0
    fatigue_timer = False
    player1_fatigue_counter = 0
    player2_fatigue_counter = 0
    player1_heal_time = False
    player2_heal_time = False
    heal_player1_hp = False
    heal_player2_hp = False
    player1_heal_counter = 0
    player2_heal_counter = 0
    fatigue = False
    next_round = False
    next_round_timer = False
    node_addition = False
    
    player_1_pokemon_posx = 0
    player_2_pokemon_posx = 800

    comparison_dia_timer = False
    comparison_msg = ""

    player1_atk_effect_timer = False
    player2_atk_effect_timer = False

    player1_proj_hit = False
    player2_proj_hit = False
    show_player1_impact = True
    show_player2_impact = True
    transition_timer = pygame.time.get_ticks()
    transition_frame_index = 0

    player1_faint_timer = None
    player1_faint_index = 0
    player2_faint_timer = None
    player2_faint_index = 0

    deduct_player2hp_time = None
    deduct_player1hp_time = None
    # Load up projectiles to be used by both pokemons
    for num in range(len(battle_effects)):
        if battle_effects[num].type == player_1_pokemon.type:
            player_1_battle_effect_image = battleeffects_frames[num]
            player_1_battle_effect_index = 0
            player_1_impact_effect_image = impacteffect_frames[num]
            player_1_impact_effect_index = 0
            player_1_impact_effect = impact_effects[num]
        if battle_effects[num].type == player_2_pokemon.type:
            player_2_battle_effect_image = battleeffects_frames[num]
            player_2_battle_effect_index = 0
            player_2_impact_effect_image = impacteffect_frames[num]
            player_2_impact_effect_index = 0
            player_2_impact_effect = impact_effects[num]
    
    potion_frames = potionpoison_frames[0]
    poison_frames = potionpoison_frames[1]
                
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

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
            another_round = False

        # Display chosen background
        screen.blit(current_background, (0,0))
        ready = False

        # To show what the current match number is
        show_text(f"Match {match_number+1}", screen.get_width() // 2, 61, screen, 40, color = "Black", bold=True)

        # To show the name of pokemon in the current match
        show_text(player_1_pokemon.name, 50, 34, screen, 20, "midleft", color = "Black", bold=True)
        show_text(player_2_pokemon.name, 595, 34, screen, 20, "midleft", color = "Black", bold=True)
        
        # show pokemon type-icon
        screen.blit(scale(pygame.image.load(f"./assets/type-icons/{player_1_pokemon.type}.png"), 0.4), (46, 50))
        screen.blit(scale(pygame.image.load(f"./assets/type-icons/{player_2_pokemon.type}.png"), 0.4), (591, 50))

        # To show the Health Points Bar of the Pokemons
        hp_bar = scale(pygame.image.load("./assets/Battle_Scene/hp_bar.png"), .5)
        # For player 1
        player1_grn_pcnt = (player_1_pokemon.remaining_health/player_1_pokemon.health)*92
        pygame.draw.rect(screen, "#d8483a", (113, 65, 92, 6), border_radius= 3)
        pygame.draw.rect(screen, "#7df39d", (113, 65, player1_grn_pcnt, 6), border_radius= 3)

        # For player 2
        player2_grn_pcnt = (player_2_pokemon.remaining_health/player_2_pokemon.health)*92
        pygame.draw.rect(screen, "#d8483a", (657, 65, 92, 6), border_radius= 3)
        pygame.draw.rect(screen, "#7df39d", (657, 65, player2_grn_pcnt, 6), border_radius= 3)

        player1_hp_bar_rect = hp_bar.get_rect(topleft = (76, 59))
        player2_hp_bar_rect = hp_bar.get_rect(topleft = (620, 59))

        screen.blit(hp_bar, player1_hp_bar_rect)
        screen.blit(hp_bar, player2_hp_bar_rect)

        # To show the Health Points of the Pokemons (Text)
        show_text(f"{player_1_pokemon.remaining_health}/{player_1_pokemon.health}", 217, 49, screen, 20, "midright", color = "Black", shadow=False)
        show_text(f"{player_2_pokemon.remaining_health}/{player_2_pokemon.health}", 760, 49, screen, 20, "midright", color = "Black", shadow=False)
        
        # Loading of Arrow Image
        player1_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20))
        player2_arrow_img = pygame.transform.scale(pygame.image.load("./assets/buttons/R.png"), (20,20)) 

        # Display when player 1 is ready
        if player1_ready:
            show_text("READY", 110, 530, screen, 35, color= "White")

        # Menu when confirming an action for player 1
        elif player1_show_confirmation:
            player1_text = confirmation_messages[player1_menu_option_index].split("\n") 
            player1_text_xpos, player1_text_ypos = 95, 510
            for line in player1_text:
                show_text(line, player1_text_xpos, player1_text_ypos, screen, 20, "center", color = "White")
                player1_text_ypos += 20
            if player1_confirmation_index == 0:
                show_text("Yes", 210, 510, screen, 20, "midleft",highlight= True, color = "Black")
                player1_arrow_img_rect = player1_arrow_img.get_rect(midleft = (190, 510))
                screen.blit(player1_arrow_img, player1_arrow_img_rect)
            else:
                show_text("Yes", 210, 510, screen, 20, "midleft", color = "Black")
            if player1_confirmation_index == 1:
                show_text("No", 280, 510, screen, 20, "midleft",highlight= True, color = "Black")
                player1_arrow_img_rect = player1_arrow_img.get_rect(midleft = (260, 510))
                screen.blit(player1_arrow_img, player1_arrow_img_rect)
            else:
                show_text("No", 280, 510, screen, 20, "midleft",color = "Black")

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
                player1_text_xpos, player1_text_ypos = 100, 520
                for line in player1_text:
                    show_text(line, player1_text_xpos, player1_text_ypos, screen, 20, "center", color="White", bold=True)
                    player1_text_ypos += 20
                
                if player1_menu_option_index == i:
                    show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft", True, color = "Black")
                    arrow_img_rect = player1_arrow_img.get_rect(midleft = (190 + ((i+2)%2)*80, y))
                    screen.blit(player1_arrow_img, arrow_img_rect)
                else:
                    show_text(menu_options[i], 210 + ((i+2)%2)*80, y, screen, 20, "midleft", color = "Black")

        if player2_ready:
            show_text("READY", 530, 530, screen, 35, color= "White")
        # Menu when confirming an action for player 2
        elif player2_show_confirmation:
            player2_text = confirmation_messages[player2_menu_option_index].split("\n")
            player2_text_xpos, player2_text_ypos = 518, 510
            for line in player2_text:
                show_text(line, player2_text_xpos, player2_text_ypos, screen, 20, "center", color = "White")
                player2_text_ypos += 20
            if player2_confirmation_index == 0:
                show_text("Yes", 630, 510, screen, 20, "midleft",highlight= True, color = "Black")
                player2_arrow_img_rect = player2_arrow_img.get_rect(midleft = (610, 510))
                screen.blit(player2_arrow_img, player2_arrow_img_rect)
            else:
                show_text("Yes", 630, 510, screen, 20, "midleft", color = "Black")
            if player2_confirmation_index == 1:
                show_text("No", 700, 510, screen, 20, "midleft",highlight= True, color = "Black")
                player2_arrow_img_rect = player2_arrow_img.get_rect(midleft = (780, 510))
                screen.blit(player2_arrow_img, player2_arrow_img_rect)
            else:
                show_text("No", 700, 510, screen, 20, "midleft",color = "Black")
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
                player2_text_xpos, player2_text_ypos = 520, 520
                for line in player2_text:
                    show_text(line, player2_text_xpos, player2_text_ypos, screen, 20, "center", color ="White", bold=True)
                    player2_text_ypos += 20
                if player2_menu_option_index == i:
                    show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft", True, color = "Black")
                    arrow_img_rect = player2_arrow_img.get_rect(midleft = (610 + ((i+2)%2)*80, y))
                    screen.blit(player2_arrow_img, arrow_img_rect)
                else:
                    show_text(menu_options[i], 630 + ((i+2)%2)*80, y, screen, 20, "midleft", color = "Black")

              

        # Get current frame and resize it proportionally
        player_1_pokemon_image = pygame.transform.flip(pygame.transform.scale(player1_loaded_images[p1_current_pokemon_index][player1_pokemon_frame_index[p1_current_pokemon_index]], tuple([measure*1.5 for measure in player_1_pokemon.size])), True, False)
        player_2_pokemon_image = pygame.transform.scale(player2_loaded_images[p2_current_pokemon_index][player2_pokemon_frame_index[p2_current_pokemon_index]], tuple([measure*1.5 for measure in player_2_pokemon.size]))

        # Position them in the screen properly and on the same footing to show difference in size
        while player_1_pokemon_posx < 200 and player_2_pokemon_posx > 600:
            player_1_pokemon_posx += 20
            player_2_pokemon_posx -= 20
            break
        player_1_pokemon_rect = player_1_pokemon_image.get_rect(midbottom = (player_1_pokemon_posx, screen.get_height() // 2 + 150))
        player_2_pokemon_rect = player_2_pokemon_image.get_rect(midbottom = (player_2_pokemon_posx, screen.get_height() // 2 + 150))

        # Put them on the screen
        screen.blit(player_1_pokemon_image, player_1_pokemon_rect)
        screen.blit(player_2_pokemon_image, player_2_pokemon_rect)

        # Update frame index
        player1_pokemon_frame_index[p1_current_pokemon_index] = (player1_pokemon_frame_index[p1_current_pokemon_index] + 1) % len(player1_loaded_images[p1_current_pokemon_index])
        player2_pokemon_frame_index[p2_current_pokemon_index] = (player2_pokemon_frame_index[p2_current_pokemon_index] + 1) % len(player2_loaded_images[p2_current_pokemon_index])

        ready = player1_ready and player2_ready # to check if both player are ready

        if ready:
            if not buffs_stack.empty():
                fight_dia_duration = 12000
                for _ in range(len(buffs_stack.stack)):
                        player_buff = buffs_stack.pop()
                        if player_buff == 1:
                            player1_buff = True
                        if player_buff == 2:
                            player2_buff = True
            if fight_dia_timer and pygame.time.get_ticks() - fight_dia_timer < fight_dia_duration:
                x_pos += 0
                if pygame.time.get_ticks() - fight_dia_timer < 5000:
                    show_text(str(random.randint(1, 150)),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    show_text(str(random.randint(1, 150)),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")

                elif (player1_buff or player2_buff) and (pygame.time.get_ticks() - fight_dia_timer > 5000 and pygame.time.get_ticks() - fight_dia_timer <= 8000):
                    if player1_buff:
                        player1_buff_msg = f"{player_1_pokemon.name} receives\nboost from the battlefield".split("\n")
                        player1_buff_ypos = 306
                        for line in player1_buff_msg:
                            show_text(line, 115, player1_buff_ypos, screen, 20) 
                            player1_buff_ypos += 20
                        show_text(f"+{int(player_1_pokemon.health * 0.2)}", 260, 336, screen, 30)
                    if player2_buff:
                        player2_buff_msg = f"{player_2_pokemon.name}receives\nboost from the battlefield".split("\n")
                        player2_buff_ypos = 306
                        for line in player2_buff_msg:
                            show_text(line, 600, player2_buff_ypos, screen, 20)
                            player2_buff_ypos += 20
                        show_text(f"+{int(player_2_pokemon.health * 0.2)}", 470, 336, screen, 30)

                    # To show the numbers
                    show_text(str(player_1_pokemon.temporary_power),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    show_text(str(player_2_pokemon.temporary_power),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                elif (player1_buff or player2_buff) and (pygame.time.get_ticks() - fight_dia_timer > 8000 and pygame.time.get_ticks() - fight_dia_timer <= 10000):
                    if player1_buff:
                        if player1_power_buff_counter < int(player_1_pokemon.health * 0.2):
                            player_1_pokemon.temporary_power += 1
                            player1_power_buff_counter += 1
                        else:
                            player1_power_buff_counter = int(player_1_pokemon.health * 0.2)
                            
                        show_text(str(player_1_pokemon.temporary_power),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    else:
                        show_text(str(player_1_pokemon.temporary_power),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    if player2_buff:
                        if player2_power_buff_counter < int(player_2_pokemon.health * 0.2):
                            player_2_pokemon.temporary_power += 1
                            player2_power_buff_counter += 1
                        else:
                            player2_power_buff_counter = int(player_2_pokemon.health * 0.2)
                        show_text(str(player_2_pokemon.temporary_power),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                    else:
                        show_text(str(player_2_pokemon.temporary_power),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                else:
                    if comparison_dia_timer == False:
                        comparison_dia_timer = pygame.time.get_ticks()
                    if comparison_msg == "":
                        if player_1_pokemon.temporary_power == player_2_pokemon.temporary_power:
                            comparison_msg = "Both pokemons stand at equal power"
                        else:
                            comparison_msg = (f"{player_1_pokemon.name if player_1_pokemon.temporary_power > player_2_pokemon.temporary_power else player_2_pokemon.name} dominates {player_2_pokemon.name if player_2_pokemon.temporary_power < player_1_pokemon.temporary_power else player_1_pokemon.name}")
                    if pygame.time.get_ticks() - comparison_dia_timer <= 2000:
                        if msg_index < len(comparison_msg):
                            tobe_printed_msg += comparison_msg[msg_index]
                            msg_index = (msg_index + 1) if msg_index < len(comparison_msg) else len(comparison_msg)
                        show_text(tobe_printed_msg, screen.get_width()//2 , 470, screen, 20, origin= "center")

                    # To show the numbers
                    show_text(str(player_1_pokemon.temporary_power),349, 336, screen, 30, color= "Red" if player_1_pokemon.type == "Fire" else "Blue" if player_1_pokemon.type == "Water" else "Green")
                    show_text(str(player_2_pokemon.temporary_power),429, 336, screen, 30, color= "Red" if player_2_pokemon.type == "Fire" else "Blue" if player_2_pokemon.type == "Water" else "Green")
                    
                
            else:
                if collision:
                    x_pos += 3
                    if player_1_pokemon.temporary_power > player_2_pokemon.temporary_power:
                        disable_player2_proj = True
                    elif player_1_pokemon.temporary_power < player_2_pokemon.temporary_power:
                        disable_player1_proj = True
                    else:
                        disable_player1_proj = True
                        disable_player2_proj = True
                        # Edit back to fatigue = True if tie causes bug
                        post_battle = True
                    fight_dia_timer = None
                # Increment x to make each image closer to middle ( 400 )
                x_pos += 2
            
            if post_battle:
                # Simulation for the Respective Order of Potion/Poison Uses
                if post_battle_timer == False:
                    post_battle_timer = pygame.time.get_ticks()
                if not queue_duration:
                    queue_duration = consumables_queue.size() * 6000
                    post_player1_battle_damage_counter = 0
                    post_player2_battle_healing_counter = 0
                    post_player2_battle_damage_counter = 0
                    post_player1_battle_healing_counter = 0
                    
                if pygame.time.get_ticks() - post_battle_timer >= 0 and pygame.time.get_ticks() - post_battle_timer < 2000:
                    pass
                elif pygame.time.get_ticks() - post_battle_timer < queue_duration:
                    post_bat_msg_ypos = 306
                    if action_done:
                        action = consumables_queue.dequeue()
                        action_done = False
                        dequeue_timer = pygame.time.get_ticks()
                        post_battle_message = ""
                        if action == None:
                            action = ""
                        if "Potion" in action:
                            queue_effect_frames = potion_frames
                            potion_poison_effects[0].play_audio()
                        elif "Poison" in action:
                            queue_effect_frames = poison_frames
                            potion_poison_effects[1].play_audio()
                        queue_effect_frames_index = 0
                        if action == "":
                            show_effect = False
                        else:
                            show_effect = True

                    if pygame.time.get_ticks() - dequeue_timer < 5000:
                        if action == "Player 1 Used Potion":
                            post_battle_message = f"{player_1_pokemon.name} has\nused Potion.".split("\n")
                            post_bat_msg_xpos = player_1_pokemon_posx
                            show_text(f"+20", post_bat_msg_xpos, 80, screen, 20)
                            if post_player1_battle_healing_counter < 20:
                                post_player1_battle_healing_counter += 1
                                player_1_pokemon.remaining_health += 1 if player_1_pokemon.remaining_health != player_1_pokemon.health else 0
                            if post_player1_battle_healing_counter >= 20:
                                post_player1_battle_healing_counter = 20
                        elif action == "Player 1 Used Poison":
                            post_battle_message = f"{player_1_pokemon.name} has\ninflicted Poison.".split("\n")
                            post_bat_msg_xpos = player_2_pokemon_posx
                            show_text(f"-20", post_bat_msg_xpos, 80, screen, 20)
                            if post_player2_battle_damage_counter < 20:
                                post_player2_battle_damage_counter += 1
                                player_2_pokemon.remaining_health -= 1 if player_2_pokemon.remaining_health != 0 else 0
                            if post_player2_battle_damage_counter >= 20:
                                post_player2_battle_damage_counter = 20
                        elif action == "Player 2 Used Potion":
                            post_battle_message = f"{player_2_pokemon.name} has\nused Potion.".split("\n")
                            post_bat_msg_xpos = player_2_pokemon_posx
                            show_text(f"+20", post_bat_msg_xpos, 80, screen, 20)
                            if post_player2_battle_healing_counter < 20:
                                post_player2_battle_healing_counter += 1 
                                player_2_pokemon.remaining_health += 1 if player_2_pokemon.remaining_health != player_2_pokemon.health else 0
                            if post_player2_battle_healing_counter >= 20:
                                post_player2_battle_healing_counter = 20
                        elif action == "Player 2 Used Poison":
                            post_battle_message = f"{player_2_pokemon.name} has\ninflicted Poison.".split("\n")
                            post_bat_msg_xpos = player_1_pokemon_posx
                            show_text(f"-20", post_bat_msg_xpos, 80, screen, 20)
                            if post_player1_battle_damage_counter < 20:
                                post_player1_battle_damage_counter += 1
                                player_1_pokemon.remaining_health -= 1 if player_1_pokemon.remaining_health != 0 else 0
                            if post_player1_battle_damage_counter >= 20:
                                post_player1_battle_damage_counter = 20
                        # Showing of Effect
                        # Compute for Ratio ( Bigger Animation Frame for Bigger Pokemons )
                        # 0.7 is best for standard sized pokemons
                        if post_bat_msg_xpos == player_1_pokemon_posx:
                            if player_1_pokemon_image.get_width() < 160:
                                pokemon_ratio = 0.7
                            else:
                                pokemon_ratio = 1
                        elif post_bat_msg_xpos == player_2_pokemon_posx:
                            if player_1_pokemon_image.get_width() < 160:
                                pokemon_ratio = 0.7
                            else:
                                pokemon_ratio = 1
                           
                        effect_current_img = pygame.transform.scale(queue_effect_frames[queue_effect_frames_index], tuple([measure * pokemon_ratio for measure in queue_effect_frames[queue_effect_frames_index].get_size()]))
                        effect_current_img_rect = effect_current_img.get_rect(center = (post_bat_msg_xpos, post_bat_msg_ypos + 100))
                        if show_effect == True:
                            screen.blit(effect_current_img, effect_current_img_rect)
                        queue_effect_frames_index += 1 if queue_effect_frames_index < len(queue_effect_frames) - 1 else 0
                        if queue_effect_frames_index == len(queue_effect_frames) - 1:
                            show_effect = False
                        for line in post_battle_message:
                            show_text(line, post_bat_msg_xpos, post_bat_msg_ypos, screen, 20)
                            post_bat_msg_ypos += 20
                        
                    else:
                        action_done = True
                else:
                    fatigue = True
                    action_done = False
                    post_battle = False     
                    
            if fatigue:   
                fatigue_msg_ypos = screen.get_width() // 2
                if fatigue_timer == False:
                    fatigue_timer = pygame.time.get_ticks()
                if pygame.time.get_ticks() - fatigue_timer < 4000:
                    fatigue_msg = "Due to fatigue, both pokemon\nwill lose 5 health points".split("\n")
                    for line in fatigue_msg:
                        show_text(line, screen.get_width()//2, fatigue_msg_ypos, screen, 30)
                        fatigue_msg_ypos += 30
                elif pygame.time.get_ticks() - fatigue_timer >= 4000 and pygame.time.get_ticks() - fatigue_timer <= 5000:
                    if player1_fatigue_counter < 5:
                        player1_fatigue_counter += 1
                        player_1_pokemon.remaining_health -= 1 if player_1_pokemon.remaining_health != 0 else 0
                    if player1_fatigue_counter >= 5:
                        player1_fatigue_counter = 5
                    if player2_fatigue_counter < 5:
                        player2_fatigue_counter += 1
                        player_2_pokemon.remaining_health -= 1 if player_2_pokemon.remaining_health != 0 else 0
                    if player2_fatigue_counter >= 5:
                        player2_fatigue_counter = 5
                else:
                    if player_1_pokemon.remaining_health == 0 or player_2_pokemon.remaining_health == 0:
                        if player_1_pokemon.remaining_health == 0:
                            if player1_faint_timer == None:
                                player1_faint_timer = pygame.time.get_ticks()
                                player1_faint_animation_interval = pygame.time.get_ticks()
                            if pygame.time.get_ticks() - player1_faint_timer <= 5000:
                                if pygame.time.get_ticks() - player1_faint_animation_interval > 500:
                                    player1_faint_index = (player1_faint_index + 1) % len(battle_effects_loaded_images[4])
                                    player1_faint_animation_interval = pygame.time.get_ticks()
                                player1_faint_current_img = pygame.transform.scale(battle_effects_loaded_images[4][player1_faint_index], tuple([measure * 0.18 for measure in battle_effects_loaded_images[4][player1_faint_index].get_size()]))
                                player1_faint_current_img_rect = player1_faint_current_img.get_rect(center = (player_1_pokemon_posx, 300))
                                screen.blit(player1_faint_current_img, player1_faint_current_img_rect)
                                player1_faint_msg = f"{player_1_pokemon.name} fainted due to exhaustion.\n{player_1_pokemon.name} will be removed from future\nmatch-ups".split("\n")
                                player1_faint_msg_ypos = 150
                                for line in player1_faint_msg:
                                    show_text(line, player_1_pokemon_posx, player1_faint_msg_ypos, screen, 20)
                                    player1_faint_msg_ypos += 20
                            else:
                                next_round = True
                        if player_2_pokemon.remaining_health == 0:
                            if player2_faint_timer == None:
                                player2_faint_timer = pygame.time.get_ticks()
                                player2_faint_animation_interval = pygame.time.get_ticks()
                            if pygame.time.get_ticks() - player2_faint_timer <= 5000:
                                if pygame.time.get_ticks() - player2_faint_animation_interval > 500:
                                    player2_faint_index = (player2_faint_index + 1) % len(battle_effects_loaded_images[4])
                                    player2_faint_animation_interval = pygame.time.get_ticks()
                                player2_faint_current_img = pygame.transform.scale(battle_effects_loaded_images[4][player1_faint_index], tuple([measure * 0.18 for measure in battle_effects_loaded_images[4][player1_faint_index].get_size()]))
                                player2_faint_current_img_rect = player2_faint_current_img.get_rect(center = (player_2_pokemon_posx, 300))
                                screen.blit(player2_faint_current_img, player2_faint_current_img_rect)
                                player2_faint_msg = f"{player_2_pokemon.name} fainted due to exhaustion.\n{player_2_pokemon.name} will be removed from future\nmatch-ups".split("\n")
                                player2_faint_msg_ypos = 150
                                for line in player2_faint_msg:
                                    show_text(line, player_2_pokemon_posx, player2_faint_msg_ypos, screen, 20)
                                    player2_faint_msg_ypos += 20
                            else:
                                next_round = True

                    else:
                        next_round = True
            if next_round:
                if node_addition == False:
                    if match_number == 0:
                        if player_1_pokemon.temporary_power > player_2_pokemon.temporary_power:
                            root_node = Node("Player 1")
                        elif player_1_pokemon.temporary_power < player_2_pokemon.temporary_power:
                            root_node = Node("Player 2")
                        else:
                            root_node = Node("Tie")
                    else:
                        if player_1_pokemon.temporary_power > player_2_pokemon.temporary_power:
                            add_node(root_node, "Player 1", "left")
                        elif player_1_pokemon.temporary_power < player_2_pokemon.temporary_power:
                            add_node(root_node, "Player 2", "right")
                        else:
                            add_node(root_node, "Tie", "left")
                    node_addition = True
                if next_round_timer == False:
                    next_round_timer = pygame.time.get_ticks()
                if pygame.time.get_ticks() - next_round_timer > 3000:
                    next_round = False
                    player_1_pokemon.temporary_power = player_1_pokemon.power
                    player_2_pokemon.temporary_power = player_2_pokemon.power
                    return match_number+1, (player_1_pokemon, player_2_pokemon), root_node
                                       
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
                if not collision:
                    fight_dia_timer = pygame.time.get_ticks()
                    collision = True
            
            # If projectiles pokemon
            # If Player1 projectile hits Player 2
            if player_1_battle_effect_current_img_rect.colliderect(player_2_pokemon_rect):
                if not player1_proj_hit:
                    player1_proj_hit = True
                disable_player1_proj = True
                
            # If player2 projectile hits Player 1
            elif player_2_battle_effect_current_img_rect.colliderect(player_1_pokemon_rect):
                if not player2_proj_hit:
                    player2_proj_hit = True
                    disable_player2_proj = True

            if player2_proj_hit:
                if player2_atk_effect_timer == False:
                    player2_atk_effect_timer = pygame.time.get_ticks()
                    player_2_impact_effect.play_audio()
                if pygame.time.get_ticks() - player2_atk_effect_timer <= 2000:
                    player_2_impact_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_2_impact_effect_image[player_2_impact_effect_index], 90), player_2_impact_effect_image[player_2_impact_effect_index].get_size())
                    player_2_impact_effect_rect = player_2_impact_effect_current_img.get_rect(center = (player_1_pokemon_posx - 50, screen.get_height() // 2 + 150))
                    if show_player2_impact:
                        screen.blit(player_2_impact_effect_current_img, player_2_impact_effect_rect)
                    player_2_impact_effect_index += 1 if player_2_impact_effect_index < len(player_2_impact_effect_image)-1 else 0
                    if player_2_impact_effect_index == len(player_2_impact_effect_image)-1:
                        show_player2_impact = False
                    show_text(f"-15", player_1_pokemon_posx, 80, screen, 20)
                    heal_msg = f"{player_1_pokemon.name} will receive 15 points\n of damage".split("\n")
                    heal_msg_ypos = 180
                    for line in heal_msg:
                        show_text(line, screen.get_width() //2, heal_msg_ypos, screen, 20 )
                        heal_msg_ypos += 20
                else:
                    if not deduct_player1_hp:
                        deduct_player1_hp = True
                
                    
            if player1_proj_hit:
                if player1_atk_effect_timer == False:
                    player1_atk_effect_timer = pygame.time.get_ticks()
                    player_1_impact_effect.play_audio()
                if pygame.time.get_ticks() - player1_atk_effect_timer <= 2000:
                    player_1_impact_effect_current_img = pygame.transform.scale(pygame.transform.rotate(player_1_impact_effect_image[player_1_impact_effect_index], 90), player_1_impact_effect_image[player_1_impact_effect_index].get_size())
                    player_1_impact_effect_rect = player_1_impact_effect_current_img.get_rect(center = (player_2_pokemon_posx + 50, screen.get_height() // 2 + 150))
                    if show_player1_impact:
                        screen.blit(player_1_impact_effect_current_img, player_1_impact_effect_rect)
                    player_1_impact_effect_index += 1 if player_1_impact_effect_index < len(player_1_impact_effect_image)-1 else 0
                    if player_1_impact_effect_index == len(player_1_impact_effect_image)-1:
                        show_player1_impact = False
                    show_text(f"-15", player_2_pokemon_posx, 80, screen, 20)
                    heal_msg = f"{player_2_pokemon.name} will receive 15 points\n of damage".split("\n")
                    heal_msg_ypos = 180
                    for line in heal_msg:
                        show_text(line, screen.get_width() //2, heal_msg_ypos, screen, 20 )
                        heal_msg_ypos += 20

                else:
                    if not deduct_player2_hp:
                        deduct_player2_hp = True
                

            if deduct_player2_hp:
                if deduct_player2hp_time == None:
                    deduct_player2hp_time = pygame.time.get_ticks()
                if pygame.time.get_ticks() - deduct_player2hp_time <= 2000:
                    if pygame.time.get_ticks() - player_2_dmg_time >= dmg_interval and player1_damage_counter < 15 :
                        player1_damage_counter +=1
                        player_2_pokemon.remaining_health -= 1 if player_2_pokemon.remaining_health > 0 else 0
                    if player1_damage_counter >= 15:
                        player1_damage_counter = 15
                        deduct_player2_hp = False
                        heal_player1_hp = True
                    
                
            elif deduct_player1_hp:
                if pygame.time.get_ticks() - player_1_dmg_time >= dmg_interval and player2_damage_counter < 15:
                    player2_damage_counter += 1
                    player_1_pokemon.remaining_health -= 1 if player_1_pokemon.remaining_health > 0 else 0
                if player2_damage_counter >= 15:
                    player2_damage_counter = 15
                    deduct_player1_hp = False
                    heal_player2_hp = True

            if heal_player1_hp:
                if player1_heal_time == False:
                    player1_heal_time = pygame.time.get_ticks()
                    player1_heal_frame_index = 0
                    potion_poison_effects[0].play_audio()
                if pygame.time.get_ticks() - player1_heal_time <= 2000 :
                    player1_heal_current_img = pygame.transform.scale(battle_effects_loaded_images[5][player1_heal_frame_index], tuple([measure * 0.7 for measure in battle_effects_loaded_images[5][player1_heal_frame_index].get_size()]))
                    player1_heal_current_img_rect = player1_heal_current_img.get_rect(midbottom = (player_1_pokemon_posx, screen.get_height() // 2 + 150))
                    if player1_heal_frame_index < len(battle_effects_loaded_images[5])-1:
                        screen.blit(player1_heal_current_img, player1_heal_current_img_rect)
                        player1_heal_frame_index += 1
                    show_text(f"Adding 10 hp to {player_1_pokemon.name}", screen.get_width() // 2, screen.get_height() // 2, screen, 30 )
                elif pygame.time.get_ticks() - player1_heal_time <= 4000 and pygame.time.get_ticks() - player1_heal_time > 2000:
                    if player1_heal_counter < 10:
                        player1_heal_counter += 1
                        player_1_pokemon.remaining_health += 1 if  player_1_pokemon.remaining_health !=  player_1_pokemon.health else 0
                        
                    if player1_heal_counter >= 10:
                        player1_heal_counter = 10
                        heal_player1_hp = False
                    
                    
                else:
                    post_battle = True
                
            if heal_player2_hp:
                if player2_heal_time == False:
                    player2_heal_time = pygame.time.get_ticks()
                    player2_heal_frame_index = 0
                    potion_poison_effects[0].play_audio()
                if pygame.time.get_ticks() - player2_heal_time <= 2000:
                    player2_heal_current_img = pygame.transform.scale(battle_effects_loaded_images[5][player2_heal_frame_index], tuple([measure * 0.7 for measure in battle_effects_loaded_images[5][player2_heal_frame_index].get_size()]))
                    player2_heal_current_img_rect = player2_heal_current_img.get_rect(midbottom = (player_2_pokemon_posx, screen.get_height() // 2 + 150))
                    if player2_heal_frame_index < len(battle_effects_loaded_images[5])-1:
                        screen.blit(player2_heal_current_img, player2_heal_current_img_rect)
                        player2_heal_frame_index += 1
                    show_text(f"Adding 10 hp to {player_2_pokemon.name}", screen.get_width() // 2, screen.get_height() // 2, screen, 30 )
                elif pygame.time.get_ticks() - player2_heal_time <= 4000 and pygame.time.get_ticks() - player2_heal_time > 2000 :
                    if player2_heal_counter < 10:
                        player2_heal_counter += 1
                        player_2_pokemon.remaining_health += 1 if  player_2_pokemon.remaining_health !=  player_2_pokemon.health else 0
                    if player2_heal_counter >= 10:
                        player2_heal_counter = 10
                        heal_player1_hp = False
                    
                else:
                    post_battle = True
        
        # Showing of Transition for the first 2 seconds
        if pygame.time.get_ticks() - transition_timer <= 2000:
            screen.fill((0,0,0))
        if pygame.time.get_ticks() - transition_timer <= 4000 and pygame.time.get_ticks() - transition_timer > 2000:
            transition_current_img = pygame.transform.scale(transitions_loaded_images[0][transition_frame_index],(800,600))
            transition_current_img_rect = transition_current_img.get_rect(topleft = (0,0))
            if transition_frame_index < len(transitions_loaded_images[0])-1:
                screen.blit(transition_current_img, transition_current_img_rect)
                transition_frame_index += 1

      
        # Used for knowing specific locations in the screen
        # mouse_pos = pygame.mouse.get_pos()
        # print(f"Position: {mouse_pos}")

        pygame.display.flip()
        clock.tick(40)

# utility scene        
def quit():
    if original_pokemons:
        for pokemon in original_pokemons:
            pokemon.animation_clean_up()
    if battle_effects:
        for battle_effect in battle_effects:
            battle_effect.clear_residue()
    pygame.quit()
    exit()
    
def main():
    match_number = 0
    fight = True
    root_node = None
    
    pokemon_loaded_images, battle_effects_loaded_images, impact_effects_loaded_images, potion_poison_effects_loaded_images, transitions_loaded_images = load_images()
    menu()
    player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images = pokemon_selection_scene(pokemon_loaded_images, battle_effects_loaded_images)
    
    while fight:
        current_background, map_type = map_randomizer(transitions_loaded_images)
        new_match_number, dequeued_pokemon, new_root_node = fight_scene(player1_pokemons, player1_loaded_images, player2_pokemons, player2_loaded_images, battle_effects_loaded_images, impact_effects_loaded_images,potion_poison_effects_loaded_images, transitions_loaded_images, current_background, map_type, match_number, root_node)    

        match_number = new_match_number
        root_node = new_root_node
        
        print(root_node.traversePreOrder())
        
        if dequeued_pokemon[0].remaining_health > 0:
            player1_pokemons.enqueue(dequeued_pokemon[0])
        if dequeued_pokemon[1].remaining_health > 0:
            player2_pokemons.enqueue(dequeued_pokemon[1])
            
        if player1_pokemons.size() <= 0 or player2_pokemons.size() <= 0:
            fight = False

main()