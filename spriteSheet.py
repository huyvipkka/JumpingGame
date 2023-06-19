import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
        
    def get_image(self, frame, w, h, scale, color):
        image = pygame.Surface((w, h)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame*w), 0, w, h))
        image = pygame.transform.scale(image, (int(w*scale), int(h*scale)))
        image.set_colorkey(color)
        return image