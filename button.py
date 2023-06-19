import pygame

class Button:
    def __init__(self, text, font, color, color_hover, rect):
        self.text = text
        self.font = font
        self.size = pygame.font.Font.size(self.font, text)
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.color = color
        self.color_hover = color_hover
        
    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        color = self.color
        if self.rect.collidepoint(pos[0], pos[1]):
            color = self.color_hover   
        pygame.draw.rect(screen, color, self.rect, 2)
        x = self.rect.centerx - self.size[0]//2
        y = self.rect.centery - self.size[1]//2
        screen.blit(self.font.render(self.text, True, color), (x, y))
    
    def check(self, *keys_pressed):
        key = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        for k in keys_pressed:
            if key[getattr(pygame, k)]:
                return True
        if self.rect.collidepoint(pos[0], pos[1]):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False
        