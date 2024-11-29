import pygame

def scale(loaded_image, multiply = 1):
    return pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * multiply), int(loaded_image.get_height() * multiply)))

def show_text(text, x_position, y_position, screen, font_size = 60, position = "center", highlight = False):
    pokemon_font = pygame.font.Font("./assets/font/Pokemon-Em.ttf", font_size)
    rendered_text = pokemon_font.render(text, False, "#4ddf6f")
    if position == "center":
        rendered_text_rect = rendered_text.get_rect(center = (x_position, y_position))
    elif position == "midleft":
        rendered_text_rect = rendered_text.get_rect(midleft = (x_position, y_position))
    elif position == "topleft":
        rendered_text_rect = rendered_text.get_rect(topleft = (x_position, y_position))
    if highlight:
        pygame.draw.rect(screen, "#fc0404", (rendered_text_rect.x - 5, rendered_text_rect.y - 5, rendered_text_rect.width + 10, rendered_text_rect.height + 10), 3)

    screen.blit(rendered_text, rendered_text_rect)
