import pygame

def scale(loaded_image, multiply = 1):
    return pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * multiply), int(loaded_image.get_height() * multiply)))


def show_text(text, x_position, y_position, screen, origin="center", size=60, color="White"):
    pokemon_font = pygame.font.Font("./assets/font/Pokemon-Em.ttf", size)
    rendered_text = pokemon_font.render(text, False, color)
    if origin == "center":
        rendered_text_rect = rendered_text.get_rect(center = (x_position, y_position))
    elif origin == "topleft":
        rendered_text_rect = rendered_text.get_rect(topleft = (x_position, y_position))
    # pygame.draw.rect(screen, "#A8E6A3", rendered_text_rect)
    # pygame.draw.rect(screen, "#A8E6A3", rendered_text_rect, 6, 2)
    screen.blit(rendered_text, rendered_text_rect)