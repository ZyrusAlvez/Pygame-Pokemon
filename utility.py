import pygame

def scale(loaded_image, multiply = 1):
    return pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * multiply), int(loaded_image.get_height() * multiply)))

def show_text(text, x_position, y_position, screen, font_size = 60, origin = "center", highlight = False, color = "White", bold=False):
    if bold:
        pokemon_font = pygame.font.Font("./assets/font/Pokemon-DP-Bold.ttf", font_size)
    else:
        pokemon_font = pygame.font.Font("./assets/font/Pokemon-Em.ttf", font_size)
    rendered_text = pokemon_font.render(text, False, color)
    if origin == "center":
        rendered_text_rect = rendered_text.get_rect(center = (x_position, y_position))
    elif origin == "midleft":
        rendered_text_rect = rendered_text.get_rect(midleft = (x_position, y_position))
    elif origin == "topleft":
        rendered_text_rect = rendered_text.get_rect(topleft = (x_position, y_position))
    if highlight:
        pygame.draw.rect(screen, "#fc0404", (rendered_text_rect.x - 5, rendered_text_rect.y - 5, rendered_text_rect.width + 10, rendered_text_rect.height + 10), 3)

    screen.blit(rendered_text, rendered_text_rect)\
        

def apply_brightness(image, brightness_factor=0.4):
    """
    Uniformly reduces the brightness of an image, including transparent areas.

    Args:
        image (pygame.Surface): The image to adjust.
        brightness_factor (float): Brightness factor (0 to 1).
                                   0 = completely dark, 1 = original brightness.

    Returns:
        pygame.Surface: A new surface with adjusted brightness.
    """
    # Ensure brightness_factor is clamped between 0 and 1
    brightness_factor = max(0, min(brightness_factor, 1))

    # Create a copy of the original image
    adjusted_image = image.copy()

    # Lock the surface for pixel access
    adjusted_image.lock()
    
    # Iterate over every pixel and adjust brightness
    width, height = adjusted_image.get_size()
    for x in range(width):
        for y in range(height):
            # Get pixel color (R, G, B, A)
            r, g, b, a = adjusted_image.get_at((x, y))
            # Scale the RGB values by the brightness factor
            r = int(r * brightness_factor)
            g = int(g * brightness_factor)
            b = int(b * brightness_factor)
            # Set the pixel with new RGB but keep original alpha
            adjusted_image.set_at((x, y), (r, g, b, a))
    
    # Unlock the surface after pixel operations
    adjusted_image.unlock()
    
    return adjusted_image