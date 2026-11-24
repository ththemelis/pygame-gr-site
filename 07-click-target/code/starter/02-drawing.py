"""Στάδιο 2 — Σχεδίαση: ο στόχος και η γραμμή πληροφοριών.

Συμπλήρωσε τα επτά κενά (____). Όταν το πρόγραμμα τρέξει, βλέπεις έναν στόχο από τρεις κύκλους, μια
γραμμή κάτω από την περιοχή πληροφοριών και ένα κίτρινο περίγραμμα γύρω από το ορθογώνιο του στόχου.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
TARGET_SIZE = 80
SHOW_HITBOX = True

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάτα τον στόχο")

target = pygame.Rect(280, 200, TARGET_SIZE, TARGET_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    # TODO 1: οριζόντια γραμμή στο ύψος HUD_HEIGHT, από το x = 0 μέχρι το x = WIDTH
    pygame.draw.line(screen, GREY, (0, ____), (WIDTH, HUD_HEIGHT), 2)

    # Ο στόχος: τρεις ομόκεντροι κύκλοι. Ο μεγαλύτερος ζωγραφίζεται πρώτος.
    # TODO 2: η ακτίνα είναι το μισό του πλάτους του ορθογωνίου
    radius = target.____ // 2
    # TODO 3: ο εξωτερικός κύκλος είναι κόκκινος
    pygame.draw.circle(screen, ____, target.center, radius)
    # TODO 4: ο μεσαίος κύκλος είναι λευκός, με το ίδιο κέντρο και ακτίνα radius * 2 // 3
    ____
    # TODO 5: ο εσωτερικός κύκλος έχει ακτίνα το ένα τρίτο της ακτίνας
    pygame.draw.circle(screen, RED, target.____, radius // 3)

    # Το περίγραμμα του ορθογωνίου δείχνει την περιοχή που θα δέχεται κλικ
    # TODO 6: ζωγράφισέ το μόνο αν η σταθερά SHOW_HITBOX είναι αληθής
    if ____:
        # TODO 7: το τελευταίο όρισμα είναι το πάχος της γραμμής: 1 δίνει μόνο περίγραμμα
        pygame.draw.rect(screen, YELLOW, target, ____)

    pygame.display.flip()

pygame.quit()
