"""Στάδιο 3 — Συμβάντα και κλικ: ο στόχος αλλάζει θέση.

Συμπλήρωσε τα οκτώ κενά (____). Όταν το πρόγραμμα τρέξει, κάθε επιτυχημένο κλικ μετακινεί τον στόχο
και γράφει το σκορ στο τερματικό. Κάθε κλικ εκτός στόχου μετρά ως αστοχία. Στα πέντε σκορ το
πρόγραμμα κλείνει. Τα κείμενα στο παράθυρο έρχονται στο Στάδιο 4.
"""
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
TARGET_SIZE = 80
GOAL = 5

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάτα τον στόχο")

target = pygame.Rect(280, 200, TARGET_SIZE, TARGET_SIZE)
score = 0
misses = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO 1: το συμβάν «πατήθηκε κουμπί του ποντικιού»
        elif event.type == pygame.____ and event.button == 1:
            # TODO 2: η μέθοδος του Rect που λέει αν ένα σημείο είναι μέσα σε αυτό
            if target.____(event.pos):
                # TODO 3: αύξησε το σκορ κατά 1
                score ____ 1
                print("Σκορ:", score)
                # TODO 4: το x πρέπει να είναι από 0 μέχρι WIDTH μείον το πλάτος του στόχου
                target.x = random.randint(0, WIDTH - target.____)
                # TODO 5: το y ξεκινά κάτω από την περιοχή πληροφοριών και καταλήγει HEIGHT μείον το ύψος του στόχου
                target.y = random.randint(____, HEIGHT - target.height)
            else:
                # TODO 6: μέτρησε μια αστοχία
                ____
                print("Αστοχίες:", misses)

    # TODO 7: όταν το σκορ φτάσει τον στόχο του παιχνιδιού
    if score ____ GOAL:
        print(f"Κέρδισες με {misses} αστοχίες.")
        # TODO 8: σταμάτα τον βρόχο του παιχνιδιού
        ____

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)

    radius = target.width // 2
    pygame.draw.circle(screen, RED, target.center, radius)
    pygame.draw.circle(screen, WHITE, target.center, radius * 2 // 3)
    pygame.draw.circle(screen, RED, target.center, radius // 3)

    pygame.display.flip()

pygame.quit()
