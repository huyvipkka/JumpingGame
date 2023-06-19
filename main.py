import pygame
from init_var import *
from ClassGame import *
from spriteSheet import SpriteSheet
import random

jumpy = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-150)
platform_gr = pygame.sprite.Group()
platform = Platform(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-50, 100, 0)
platform_gr.add(platform)

bird_sheet = SpriteSheet(bird_image)
enemy_gr = pygame.sprite.Group()
enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, bird_sheet, 1.5)
enemy_gr.add(enemy)
pygame.mixer.music.play(-1, 0)

hight_score = int(ReadFile("hight_score.txt"))
while game_running:
    clock.tick(FPS)
    if not game_over:
        # thêm thanh gỗ
        if len(platform_gr) < MAX_PLATFORM:
            p_w = random.randint(70, 100)
            p_x = random.randint(0, SCREEN_WIDTH-p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.choice([0, 1]) and score >= 500
            platform = Platform(p_x, p_y, p_w, p_type)
            platform_gr.add(platform)
        # thêm chim
        if len(enemy_gr) == 0 and score >= 1000:
            e_dis_y = enemy.rect.y - random.randint(enemy.rect.y, enemy.rect.y+500)
            enemy = Enemy(SCREEN_WIDTH, -10, bird_sheet, 1.5)
            enemy_gr.add(enemy)
        
        scroll = jumpy.move(platform_gr) # di chuyển nhân vật và cập nhật biến cuộn
        bg_scroll += scroll #cuộn bg theo biến cuộn 
        if bg_scroll >= SCREEN_HEIGHT: 
            bg_scroll = 0 
        score += scroll 
        platform_gr.update(scroll)
        enemy_gr.update(scroll)
        
        DrawBg(screen, bg_scroll)
        platform_gr.draw(screen)
        enemy_gr.draw(screen)
        jumpy.draw(screen)
        DrawPanel(screen, score, hight_score) 
        
        if jumpy.rect.top > SCREEN_HEIGHT: # rơi xuống dưới màn hình
            game_over = True
            death_sound.play()
        if pygame.sprite.spritecollide(jumpy, enemy_gr, False): # va chạm 2 ô vuông nhân vật và chim
            if pygame.sprite.spritecollide(jumpy, enemy_gr, False, pygame.sprite.collide_mask): # va chạm 2 ảnh nhân vật và chim
                game_over = True
                quack_sound.play()
    else: #game over
        if score > hight_score:
            WriteFile("hight_score.txt", str(score))
            hight_score = score
        if fade_counter < SCREEN_WIDTH: # vẽ 6 dải đen chạy từ 2 bên
            fade_counter += 8
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y*100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH-fade_counter, (y+1)*100, SCREEN_WIDTH, 100))
        if fade_counter >= SCREEN_WIDTH: # 6 dải đen chạy xong
            DrawText(screen,f"---------Game Over---------", font_big, WHITE, 10, 200)
            DrawText(screen,f"-Score: {score}", font_big, WHITE, 40, 250)
            DrawText(screen,f"-Hight Score: {hight_score}", font_big, WHITE, 40, 300)
            DrawText(screen,f"-PRESS SPACE TO PLAY AGAIN", font_big, WHITE, 40, 350)
        DrawPanel(screen, score, hight_score) 
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]: # reset các thông số
            game_over = False
            score = 0
            scroll = 0
            jumpy.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-150)
            platform_gr.empty()
            platform = Platform(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-50, 100, 0)
            platform_gr.add(platform)
            enemy_gr.empty()
            fade_counter = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    pygame.display.update()
pygame.quit()