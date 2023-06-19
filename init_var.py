import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128,128,128)
PURPLE = (128,0,128)
TEAL = (0,128,128)
NAVY = (0,0,128)
MAROON = (128,0,0)
AQUA = (0,255,255)

pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+30))
pygame.display.set_caption("Jumping Game")

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 1
MAX_PLATFORM = 10
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0

game_running = True
game_over = False
score = 0
fade_counter = 0 

bg_image = pygame.image.load("assets/bg.png").convert_alpha()
jumpy_image = pygame.transform.scale(pygame.image.load("assets/jump.png").convert_alpha(), (45, 45))
platform_image = pygame.image.load("assets/wood.png").convert_alpha()
bird_image = pygame.image.load("assets/bird.png").convert_alpha()

font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 24)


pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
jump_sound = pygame.mixer.Sound("assets/jump.mp3")
death_sound = pygame.mixer.Sound("assets/death.mp3")
quack_sound = pygame.mixer.Sound("assets/quac.mp3")