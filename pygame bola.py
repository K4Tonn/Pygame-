import pygame
import os
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Pygame")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fungsi untuk memuat gambar
def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

# Fungsi untuk memuat suara
def load_sound(name):
    fullname = os.path.join('assets', name)
    sound = pygame.mixer.Sound(fullname)
    return sound

# Kelas untuk latar belakang bergerak dengan parallax effect
class ParallaxBackground:
    def __init__(self, image_path, speed):
        self.bg_image = load_image(image_path)
        self.rect1 = self.bg_image.get_rect()
        self.rect2 = self.bg_image.get_rect()
        self.rect2.left = self.rect1.right
        self.speed = speed

    def update(self):
        self.rect1.left -= self.speed
        self.rect2.left -= self.speed
        if self.rect1.right <= 0:
            self.rect1.left = self.rect2.right
        if self.rect2.right <= 0:
            self.rect2.left = self.rect1.right

    def draw(self, screen):
        screen.blit(self.bg_image, self.rect1)
        screen.blit(self.bg_image, self.rect2)

# Kelas untuk pemain dengan animasi menggunakan sprite sheet
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = load_image('player_spritesheet.png', -1)
        self.images = self.load_images_from_spritesheet(self.sprite_sheet, 4, 4)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.move_sound = load_sound('move.wav')

    def load_images_from_spritesheet(self, sheet, rows, cols):
        images = []
        sheet_rect = sheet.get_rect()
        width = sheet_rect.width // cols
        height = sheet_rect.height // rows
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * width, row * height, width, height)
                image = sheet.subsurface(rect)
                images.append(image)
        return images

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.play_move_sound()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.play_move_sound()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.play_move_sound()
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.play_move_sound()

        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def play_move_sound(self):
        if not pygame.mixer.get_busy():
            self.move_sound.play()

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

# Latar belakang bergerak dengan parallax effect
background_layers = [
    ParallaxBackground('background_layer1.png', 1),
    ParallaxBackground('background_layer2.png', 2),
    ParallaxBackground('background_layer3.png', 3),
]

# Musik latar
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

# Loop utama
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perbarui semua sprite dan latar belakang
    all_sprites.update()
    for layer in background_layers:
        layer.update()

    # Periksa tabrakan
    if pygame.sprite.spritecollideany(player, enemies):
        running = False  # Game over jika pemain bertabrakan dengan musuh

    # Perbarui skor
    score.increase()

    # Gambar latar belakang dengan parallax effect
    for layer in background_layers:
        layer.draw(screen)

    # Gambar semua sprite
    all_sprites.draw(screen)

    # Gambar skor
    score.draw(screen)

    # Perbarui layar
    pygame.display.flip()

    # Atur FPS
    clock.tick(60)

pygame.quit()
