"""Στάδιο 2 — Όρια, αναπήδηση και χρόνος ανά καρέ (dt).

Συμπλήρωσε τα πέντε κενά (____). Η μπάλα κινείται με ταχύτητα 300 pixel το δευτερόλεπτο, αναπηδά στις δύο
πλευρές του παραθύρου και ο ρυθμός καρέ (FPS) φαίνεται πάνω αριστερά.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
RADIUS = 22
MAX_DT = 0.05              # το πολύ 0,05 δευτερόλεπτα ανά καρέ

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
WHITE = (245, 245, 245)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάγωσε την μπάλα")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

ball_x = RADIUS
ball_y = HEIGHT // 2
speed = 300                # pixel ανά ΔΕΥΤΕΡΟΛΕΠΤΟ

running = True
while running:
    # Πόσα δευτερόλεπτα πέρασαν από το προηγούμενο καρέ (η tick επιστρέφει χιλιοστά του δευτερολέπτου)
    # TODO 1: τα χιλιοστά γίνονται δευτερόλεπτα με διαίρεση με το 1000
    dt = clock.tick(60) / ____
    # TODO 2: κράτα το dt το πολύ ίσο με MAX_DT, ώστε μια καθυστέρηση να μη «πετάξει» την μπάλα
    dt = ____(dt, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO 3: η μετακίνηση είναι ταχύτητα επί χρόνο
    ball_x += speed * ____
    # TODO 4: όταν η μπάλα περάσει την αριστερή πλευρά (η θέση είναι μικρότερη από την ακτίνα)
    if ball_x ____ RADIUS:
        ball_x = RADIUS
        speed = -speed
    elif ball_x > WIDTH - RADIUS:
        ball_x = WIDTH - RADIUS
        # TODO 5: αντέστρεψε την ταχύτητα, όπως στην αριστερή πλευρά
        ____

    screen.fill(BACKGROUND)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), RADIUS)
    fps_image = font.render(f"FPS: {clock.get_fps():.0f}", True, WHITE)
    screen.blit(fps_image, (20, 20))
    pygame.display.flip()

pygame.quit()
