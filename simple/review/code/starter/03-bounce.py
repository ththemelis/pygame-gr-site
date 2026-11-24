"""Επαναληπτικό, Στάδιο 3 — το τετράγωνο αναπηδά και πάνω-κάτω.

Συμπλήρωσε τα τρία κενά (____). Το τετράγωνο κινείται και προς τα κάτω ή πάνω και πρέπει να αναπηδά στο πάνω και στο κάτω όριο.
"""
import random

import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη και χρώματα =====
WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
SIZE = 60

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Επαναληπτικό: αναπήδηση")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
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
box = pygame.Rect(570, 210, SIZE, SIZE)
speed_x = 5                # pixel ανά καρέ προς τα δεξιά (αρνητικό: προς τα αριστερά)
speed_y = 3                # pixel ανά καρέ προς τα κάτω (αρνητικό: προς τα πάνω)
score = 0
misses = 0
last_click = None
hit = False
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            last_click = event.pos
            hit = box.collidepoint(event.pos)
            if hit:
                score += 1
                box.y = random.randint(HUD_HEIGHT, HEIGHT - SIZE)
            else:
                misses += 1

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if not paused or step_once:
        frame += 1
        box.x += speed_x
        # TODO 1: κατακόρυφη κίνηση: το y αλλάζει κατά speed_y, όπως το x αλλάζει κατά speed_x
        box.y += ____
        if box.left < 0:
            box.left = 0
            speed_x = -speed_x
        elif box.right > WIDTH:
            box.right = WIDTH
            speed_x = -speed_x
        if box.top < HUD_HEIGHT:
            box.top = HUD_HEIGHT
            speed_y = -speed_y
        # TODO 2: όταν το ΚΑΤΩ άκρο του τετραγώνου ξεπεράσει το κάτω άκρο του παραθύρου (HEIGHT)
        elif box.bottom ____ HEIGHT:
            box.bottom = HEIGHT
            # TODO 3: η κατακόρυφη κατεύθυνση αντιστρέφεται, όπως η οριζόντια στις άλλες γραμμές
            speed_y = ____
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Σκορ: {score}", WHITE, (20, 20))
    draw_text(screen, font, f"Αστοχίες: {misses}", WHITE, (220, 20))
    pygame.draw.rect(screen, RED, box)
    draw_watch(screen, small_font, [("frame", frame), ("box", box), ("speed_x", speed_x), ("speed_y", speed_y), ("hit", hit)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
