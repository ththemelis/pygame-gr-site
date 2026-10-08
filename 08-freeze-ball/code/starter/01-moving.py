"""Στάδιο 1 — Κίνηση: θέση και ταχύτητα ανά καρέ.

Συμπλήρωσε τα τέσσερα κενά (____). Η μπάλα μετακινείται προς τα δεξιά και, όταν βγει ολόκληρη από το
παράθυρο, ξαναμπαίνει από τα αριστερά.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
RADIUS = 22

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάγωσε την μπάλα")
clock = pygame.time.Clock()

# Βήμα 1, έξω από τον βρόχο: η αρχική θέση και η ταχύτητα της μπάλας
ball_x = RADIUS
ball_y = HEIGHT // 2
speed = 5                  # pixel ανά καρέ

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Βήμα 2, μέσα στον βρόχο: πρώτα η μετακίνηση, μετά η σχεδίαση
    # TODO 1: σε κάθε καρέ, η θέση αυξάνεται κατά την ταχύτητα
    ball_x ____ speed
    # TODO 2: όταν το κέντρο της μπάλας περάσει τη δεξιά άκρη κατά μία ακτίνα, η μπάλα έχει βγει ολόκληρη
    if ball_x ____ WIDTH + RADIUS:
        # TODO 3: ξαναμπαίνει από αριστερά, ακριβώς έξω από το παράθυρο
        ball_x = ____

    screen.fill(BACKGROUND)
    # TODO 4: ζωγράφισε τον κύκλο με κέντρο το σημείο (ball_x, ball_y)
    pygame.draw.circle(screen, RED, ____, RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
