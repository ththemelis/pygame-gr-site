"""Στάδιο 4 — Το ολοκληρωμένο παιχνίδι «Πάτα τον στόχο».

Συμπλήρωσε τα οκτώ κενά (____). Το παιχνίδι δείχνει το σκορ και τις αστοχίες στο παράθυρο. Με πέντε
επιτυχίες εμφανίζεται μήνυμα νίκης, και ένα κλικ ξεκινά νέο παιχνίδι.
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
GREEN = (90, 220, 150)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάτα τον στόχο")
# TODO 1: δημιούργησε γραμματοσειρά μεγέθους 36 (το None σημαίνει «η προεπιλεγμένη»)
font = pygame.font.____(None, 36)
# TODO 2: το ρολόι του παιχνιδιού (η κλάση Clock του module time)
clock = pygame.time.____()


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    # TODO 3: η μέθοδος της γραμματοσειράς που φτιάχνει μια Surface με το κείμενο
    image = font.____(text, True, color)
    # TODO 4: αντίγραψε την εικόνα του κειμένου πάνω στην επιφάνεια, στη θέση position
    surface.____(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    # TODO 5: το get_rect δέχεται όρισμα με όνομα: ποια ιδιότητα του ορθογωνίου θα μπει στο center;
    surface.blit(image, image.get_rect(____=center))


def draw_target(surface, target):
    """Ζωγραφίζει τον στόχο: τρεις ομόκεντροι κύκλοι."""
    radius = target.width // 2
    pygame.draw.circle(surface, RED, target.center, radius)
    pygame.draw.circle(surface, WHITE, target.center, radius * 2 // 3)
    pygame.draw.circle(surface, RED, target.center, radius // 3)


target = pygame.Rect(280, 200, TARGET_SIZE, TARGET_SIZE)
score = 0
misses = 0
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # TODO 6: όταν το παιχνίδι έχει τελειώσει, ένα κλικ το ξεκινά από την αρχή
            if ____:
                score = 0
                misses = 0
                game_over = False
            elif target.collidepoint(event.pos):
                score += 1
                if score == GOAL:
                    game_over = True
                else:
                    target.x = random.randint(0, WIDTH - target.width)
                    target.y = random.randint(HUD_HEIGHT, HEIGHT - target.height)
            else:
                misses += 1

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Σκορ: {score} / {GOAL}", WHITE, (20, 20))
    # TODO 7: το κείμενο «Αστοχίες: …» στη θέση (WIDTH - 180, 20), όπως το σκορ
    ____

    if game_over:
        draw_centered_text(screen, font, "Κέρδισες.", GREEN, (WIDTH // 2, HEIGHT // 2 - 20))
        draw_centered_text(screen, font, "Κάνε κλικ για νέο παιχνίδι.", WHITE, (WIDTH // 2, HEIGHT // 2 + 20))
    else:
        draw_target(screen, target)

    pygame.display.flip()
    # TODO 8: περίμενε όσο χρειάζεται ώστε ο βρόχος να τρέχει το πολύ 60 φορές το δευτερόλεπτο
    clock.____(60)

pygame.quit()
