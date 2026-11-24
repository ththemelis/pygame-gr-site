"""Επαναληπτικό, Στάδιο 1 — το τετράγωνο ξαναμπαίνει από αριστερά.

Συμπλήρωσε τα τρία κενά (____). Όταν το τετράγωνο βγει από το δεξί μέρος του παραθύρου, πρέπει να εμφανιστεί ξανά από αριστερά.
"""
import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη, χρώματα και ταχύτητες =====
WIDTH = 640
HEIGHT = 480
SIZE = 60
SPEED = 5                  # pixel ανά καρέ

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Επαναληπτικό: ο βρόχος του παιχνιδιού")
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
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
box = pygame.Rect(0, HEIGHT // 2 - SIZE // 2, SIZE, SIZE)
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

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if not paused or step_once:
        frame += 1
        # TODO 1: το τετράγωνο κινείται προς τα δεξιά κατά τόσα pixel όσα η ταχύτητα SPEED
        box.x += ____
        # TODO 2: όταν το ΑΡΙΣΤΕΡΟ άκρο του τετραγώνου ξεπεράσει το δεξί άκρο του παραθύρου (WIDTH)
        if box.left ____ WIDTH:
            # TODO 3: το ΔΕΞΙ άκρο του τετραγώνου πηγαίνει στο αριστερό άκρο του παραθύρου, που είναι η θέση 0
            box.right = ____
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, RED, box)
    draw_watch(screen, small_font, [("frame", frame), ("box.x", box.x), ("SPEED", SPEED)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
