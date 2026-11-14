"""Μ11 — Κύκλος 1. Τρία αστέρια που πέφτουν, με τον ίδιο κανόνα γραμμένο τρεις φορές, μία για κάθε αστέρι.

Δεν συμπληρώνεις τίποτα εδώ: τρέξε το πρόγραμμα, διάβασέ το ζώνη προς ζώνη και δοκίμασε τα πλήκτρα P (παύση) και N (ένα καρέ).
"""
import random

import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη, χρώματα και ταχύτητες =====
WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60            # πάνω από τη γραμμή αυτή είναι ο χώρος των κειμένων
SIZE = 60
SPEED = 5                  # pixel ανά καρέ για τον παίκτη
STAR_SIZE = 30
STAR_SPEED = 4             # pixel ανά καρέ για κάθε αστέρι

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
YELLOW = (250, 220, 90)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Μ11: πολλά αστέρια")
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
def place_star(star):
    """Βάζει το αστέρι σε τυχαία θέση, ακριβώς κάτω από τη γραμμή HUD_HEIGHT. Αλλάζει το ίδιο το Rect που της δίνεις."""
    star.x = random.randint(0, WIDTH - star.width)
    star.y = HUD_HEIGHT


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_watch(surface, font, lines):
    """Δείχνει κάτω αριστερά τις τιμές που παρακολουθούμε (λίστα από ζεύγη όνομα-τιμή) και πάνω δεξιά τα πλήκτρα του βοηθού."""
    hint = font.render("P: παύση    N: ένα καρέ", True, GREY)
    surface.blit(hint, (WIDTH - hint.get_width() - 10, 8))
    y = HEIGHT - 28 * len(lines) - 6
    for name, value in lines:
        image = font.render(f"{name} = {value}", True, WHITE)
        surface.blit(image, (10, y))
        y += 28


# ===== 3. ΔΕΔΟΜΕΝΑ: οι μεταβλητές που αλλάζουν όσο τρέχει το παιχνίδι =====
player = pygame.Rect(WIDTH // 2 - SIZE // 2, HEIGHT - SIZE, SIZE, SIZE)
star1 = pygame.Rect(100, HUD_HEIGHT, STAR_SIZE, STAR_SIZE)
star2 = pygame.Rect(200, 180, STAR_SIZE, STAR_SIZE)
star3 = pygame.Rect(500, 300, STAR_SIZE, STAR_SIZE)
score = 0
misses = 0
frame = 0
paused = False             # True: το πρόγραμμα ξεκινά σταματημένο και προχωρά με το N
step_once = False

running = True
while running:
    # ===== 4. Ο ΒΡΟΧΟΣ: ένα καρέ σε κάθε επανάληψη =====
    # ----- Α. ΣΥΜΒΑΝΤΑ: τι έκανε ο παίκτης -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_n:
                step_once = True
    keys = pygame.key.get_pressed()       # ποια πλήκτρα κρατιούνται πατημένα αυτή τη στιγμή

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if not paused or step_once:
        frame += 1
        if keys[pygame.K_LEFT]:
            player.x -= SPEED
        if keys[pygame.K_RIGHT]:
            player.x += SPEED
        if keys[pygame.K_UP]:
            player.y -= SPEED
        if keys[pygame.K_DOWN]:
            player.y += SPEED
        # όρια: αν ένα άκρο του παίκτη ξεπεράσει ένα όριο, τον βάζουμε ακριβώς πάνω στο όριο
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top < HUD_HEIGHT:
            player.top = HUD_HEIGHT
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        # το πρώτο αστέρι: πέφτει, ξαναρχίζει αν βγει από το παράθυρο ή αν το πιάσει ο παίκτης
        star1.y += STAR_SPEED
        if star1.top > HEIGHT:
            place_star(star1)
            misses += 1
        if player.colliderect(star1):
            place_star(star1)
            score += 1
        # το δεύτερο αστέρι: ο ίδιος κανόνας
        star2.y += STAR_SPEED
        if star2.top > HEIGHT:
            place_star(star2)
            misses += 1
        if player.colliderect(star2):
            place_star(star2)
            score += 1
        # το τρίτο αστέρι: ο ίδιος κανόνας
        star3.y += STAR_SPEED
        if star3.top > HEIGHT:
            place_star(star3)
            misses += 1
        if player.colliderect(star3):
            place_star(star3)
            score += 1
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Σκορ: {score}", WHITE, (20, 30))
    draw_text(screen, font, f"Χαμένα: {misses}", WHITE, (220, 30))
    pygame.draw.circle(screen, YELLOW, star1.center, STAR_SIZE // 2)
    pygame.draw.circle(screen, YELLOW, star2.center, STAR_SIZE // 2)
    pygame.draw.circle(screen, YELLOW, star3.center, STAR_SIZE // 2)
    pygame.draw.rect(screen, GREEN, player)
    draw_watch(screen, small_font, [("frame", frame), ("score", score), ("misses", misses), ("star1.y", star1.y), ("star2.y", star2.y), ("star3.y", star3.y)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
