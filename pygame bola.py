import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Kelas untuk pemain
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Kelas untuk musuh
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)

# Kelas untuk sistem skor
class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def increase(self):
        self.score += 1

    def draw(self, screen):
        score_surface = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_surface, (10, 10))

# Grup sprite
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = Score()

# Background color
background_color = BLACK

# Loop utama
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perbarui semua sprite
    all_sprites.update()

    # Periksa tabrakan
    if pygame.sprite.spritecollideany(player, enemies):
        running = False  # Game over jika pemain bertabrakan dengan musuh

    # Perbarui skor
    score.increase()

    # Gambar latar belakang
    screen.fill(background_color)

    # Gambar semua sprite
    all_sprites.draw(screen)

    # Gambar skor
    score.draw(screen)

    # Perbarui layar
    pygame.display.flip()

    # Atur FPS
    clock.tick(60)

pygame.quit()
