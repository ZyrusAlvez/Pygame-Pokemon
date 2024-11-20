import pygame
import os
from pokemon import charizard


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1100, 600))
clock = pygame.time.Clock()

# Load frames
loaded_frames = [pygame.image.load(frame) for frame in charizard.animation_frames()]

running = True
frame_index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # background
    screen.fill((255, 255, 255))
    
    # location 
    screen.blit(loaded_frames[frame_index], (550, 300))
    
    # update the screen
    pygame.display.flip()

    frame_index = (frame_index + 1) % len(loaded_frames)
    
    # fps
    clock.tick(40)

pygame.quit()

# Clean up extracted frames
charizard.animation_clean_up()
