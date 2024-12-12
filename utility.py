import pygame # type: ignore

def scale(loaded_image, multiply = 1):
    return pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * multiply), int(loaded_image.get_height() * multiply)))

def show_text(text, x_position, y_position, screen, font_size=60, origin="center", highlight=False, color="White", bold=False, shadow=True, shadow_offset=(4, 4), shadow_color="Black"):
    if color == "White":
        shadow_color = "Black"
    if color == "Black":
        shadow_color = "Gray"
    
    if bold or highlight:
        pokemon_font = pygame.font.Font("./assets/font/Pokemon-DP-Bold.ttf", font_size)
    else:
        pokemon_font = pygame.font.Font("./assets/font/Pokemon-Em.ttf", font_size)

    # Render main text
    rendered_text = pokemon_font.render(text, False, color)

    # Render shadow text if enabled
    if shadow:
        shadow_text = pokemon_font.render(text, False, shadow_color)
        if origin == "center":
            shadow_rect = shadow_text.get_rect(center=(x_position + shadow_offset[0], y_position + shadow_offset[1]))
        elif origin == "midleft":
            shadow_rect = shadow_text.get_rect(midleft=(x_position + shadow_offset[0], y_position + shadow_offset[1]))
        elif origin == "midright":
            shadow_rect = shadow_text.get_rect(midright=(x_position + shadow_offset[0], y_position + shadow_offset[1]))
        elif origin == "topleft":
            shadow_rect = shadow_text.get_rect(topleft=(x_position + shadow_offset[0], y_position + shadow_offset[1]))
        screen.blit(shadow_text, shadow_rect)


    # Calculate main text position
    if origin == "center":
        rendered_text_rect = rendered_text.get_rect(center=(x_position, y_position))
    elif origin == "midleft":
        rendered_text_rect = rendered_text.get_rect(midleft=(x_position, y_position))
    elif origin == "midright":
        rendered_text_rect = rendered_text.get_rect(midright=(x_position, y_position))
    elif origin == "topleft":
        rendered_text_rect = rendered_text.get_rect(topleft=(x_position, y_position))


    # Blit main text
    screen.blit(rendered_text, rendered_text_rect)

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

class Button:
    def __init__(self, x, y , width , height, text, font, color, hover_color, text_color, action):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text 
        self.font = pygame.font.Font(font, 20) 
        self.color = color 
        self.hover_color = hover_color 
        self.text_color = text_color
        self.action = action
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen,self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
            return True    