"""Στάδιο 1 — Δύο ρακέτες που κινούνται με τα πλήκτρα (pygame.key.get_pressed).

Συμπλήρωσε τα πέντε κενά (____). Ο αριστερός παίκτης κινεί τη ρακέτα του με τα W και S, ο δεξιός με τα βέλη πάνω και
κάτω. Η κίνηση συνεχίζεται όσο κρατάς το πλήκτρο πατημένο.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 80
PADDLE_SPEED = 360         # pixel το δευτερόλεπτο
MARGIN = 24                # απόσταση της ρακέτας από την άκρη του παραθύρου
MAX_DT = 0.05

BACKGROUND = (25, 35, 60)
GREY = (120, 130, 150)
BLUE = (110, 170, 255)
ORANGE = (255, 170, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Βήμα 1, έξω από τον βρόχο: η θέση κάθε ρακέτας (το y είναι η πάνω πλευρά της)
left_x = MARGIN
right_x = WIDTH - MARGIN - PADDLE_WIDTH
left_y = HUD_HEIGHT + (HEIGHT - HUD_HEIGHT - PADDLE_HEIGHT) / 2
right_y = left_y

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Βήμα 2, μέσα στον βρόχο: ποια πλήκτρα κρατιούνται πατημένα ΤΩΡΑ;
    # TODO 1: η συνάρτηση που επιστρέφει την κατάσταση όλων των πλήκτρων αυτή τη στιγμή
    keys = pygame.key.____()
    # TODO 2: το πλήκτρο W
    if keys[pygame.____]:
        # TODO 3: προς τα πάνω σημαίνει μικρότερο y
        left_y ____ PADDLE_SPEED * dt
    # TODO 4: το πλήκτρο S
    if keys[pygame.____]:
        left_y += PADDLE_SPEED * dt
    if keys[pygame.K_UP]:
        right_y -= PADDLE_SPEED * dt
    if keys[pygame.K_DOWN]:
        right_y += PADDLE_SPEED * dt
    # TODO 5: το y μένει ανάμεσα στο HUD_HEIGHT και στο HEIGHT - PADDLE_HEIGHT (πρότυπο του Μαθήματος 4)
    left_y = ____(HUD_HEIGHT, min(left_y, HEIGHT - PADDLE_HEIGHT))
    right_y = max(HUD_HEIGHT, min(right_y, HEIGHT - PADDLE_HEIGHT))

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    pygame.draw.rect(screen, BLUE, (left_x, round(left_y), PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, ORANGE, (right_x, round(right_y), PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.display.flip()

pygame.quit()
