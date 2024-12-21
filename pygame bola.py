import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
white = (255, 255, 255)
red = (255, 0, 0)

# Koordinat awal bola
ball_x = screen_width // 2
ball_y = screen_height // 2

# Ukuran bola
ball_radius = 20

# Kecepatan bola
ball_speed = 5

# Membuat clock untuk kontrol FPS
clock = pygame.time.Clock()

# Fungsi untuk membatasi bola agar tetap di layar
def keep_ball_in_screen(x, y, radius):
    if x - radius < 0:
        x = radius
    if x + radius > screen_width:
        x = screen_width - radius
    if y - radius < 0:
        y = radius
    if y + radius > screen_height:
        y = screen_height - radius
    return x, y

# Loop utama
while True:
    # Menghandle event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mengambil semua tombol yang ditekan
    keys = pygame.key.get_pressed()

    # Untuk kontrol bola dengan Shift + Panah
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        if keys[pygame.K_LEFT]:
            ball_x -= ball_speed
        if keys[pygame.K_RIGHT]:
            ball_x += ball_speed
        if keys[pygame.K_UP]:
            ball_y -= ball_speed
        if keys[pygame.K_DOWN]:
            ball_y += ball_speed

    # Bola agar tetap dalam layar
    ball_x, ball_y = keep_ball_in_screen(ball_x, ball_y, ball_radius)

    # Untuk BG dan bola
    screen.fill(white)
    pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)

    # Layar
    pygame.display.flip()

    # Untuk kontrol kecepatan frame
    clock.tick(60)