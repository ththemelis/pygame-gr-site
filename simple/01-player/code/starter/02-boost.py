"""Μ9, Στάδιο 2 — με το SHIFT ο παίκτης τρέχει.

Συμπλήρωσε τα τρία κενά (____).
"""
import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη, χρώματα και ταχύτητες =====
WIDTH = 640
HEIGHT = 480
SIZE = 60
SPEED = 5                  # pixel ανά καρέ
FAST_SPEED = 10            # pixel ανά καρέ, όσο κρατάς το SHIFT

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Μ9: ο παίκτης")
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
player = pygame.Rect(WIDTH // 2 - SIZE // 2, HEIGHT // 2 - SIZE // 2, SIZE, SIZE)
speed = SPEED              # η ταχύτητα αυτού του καρέ: με το SHIFT γίνεται FAST_SPEED
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
        speed = SPEED
        if keys[pygame.K_LSHIFT]:
            # TODO 1: με το SHIFT η ταχύτητα γίνεται FAST_SPEED
            speed = ____
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            # TODO 2: το δεξί βέλος χρησιμοποιεί την ταχύτητα αυτού του καρέ, αυτή που αλλάζει με το SHIFT
            player.x += ____
        if keys[pygame.K_UP]:
            # TODO 3: προς τα πάνω το y μικραίνει
            player.y ____ speed
        if keys[pygame.K_DOWN]:
            player.y += speed
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, GREEN, player)
    draw_watch(screen, small_font, [("frame", frame), ("SHIFT", keys[pygame.K_LSHIFT]), ("speed", speed), ("player", player)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
