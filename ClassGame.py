import pygame
import init_var as ini
import random

class Player():
    def __init__(self, x, y):
        self.image = ini.jumpy_image
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vy = 0
        self.flip = False
        
    def move(self, platform_gr):
        dx = 0
        dy = 0
        scroll = 0
        key = pygame.key.get_pressed()
        # Qua trái phải
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
        self.vy += ini.GRAVITY    
        dy += self.vy
        # Không vượt quá screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > ini.SCREEN_WIDTH:
            dx = ini.SCREEN_WIDTH - self.rect.right     
        #rơi xuống platfrom (nhảy)
        for platform in platform_gr:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vy > 0:
                        ini.jump_sound.play()
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vy = -20   
        if self.rect.top <= ini.SCROLL_THRESH: # nhảy qua phần cuộn
            if self.vy < 0: #đang nhảy
                scroll = -dy #biến cuộn = phàn nhảy lên qua phần cuộn
        self.rect.x += dx
        self.rect.y += dy + scroll
        self.mask = pygame.mask.from_surface(self.image)
        return scroll
        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x-12, self.rect.y-5))
        
class Platform(pygame.sprite.Sprite):
    def __init__(self, x : int, y : int, width : int, moving : int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ini.platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
    
    def update(self, scroll):
        if self.move:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        if self.move_counter >= 200 or self.rect.left < 0 or self.rect.right > ini.SCREEN_WIDTH: 
            self.direction *= -1
            self.move_counter = 0
        
        self.rect.y += scroll
        if self.rect.top > ini.SCREEN_HEIGHT:
            self.kill()
 
class Enemy(pygame.sprite.Sprite):
    animation_steps = 9
    def __init__(self, scr_w, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False
        for i in range(Enemy.animation_steps):
            image = sprite_sheet.get_image(i, 32, 32, scale, ini.BLACK)
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey(ini.BLACK)
            self.animation_list.append(image)
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, 2)
        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = scr_w
        self.rect.y = y
           
    def update(self, scroll):
        animatiton_colldown = 50
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animatiton_colldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= Enemy.animation_steps:
            self.frame_index = 0
            
        self.rect.x += self.direction * self.speed
        self.rect.y += scroll
        if self.rect.right < 0 or self.rect.left > ini.SCREEN_WIDTH:
            self.kill()
        
        if self.rect.top > ini.SCREEN_HEIGHT:
            self.kill()
 
