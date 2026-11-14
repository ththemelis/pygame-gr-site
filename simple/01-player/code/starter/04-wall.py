"""Μ9, Στάδιο 4 — ο παίκτης σταματά μπροστά στον τοίχο.

Συμπλήρωσε τα τρία κενά (____).
"""
import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη, χρώματα και ταχύτητες =====
WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60            # πάνω από τη γραμμή αυτή θα μπουν αργότερα τα κείμενα του παιχνιδιού
SIZE = 60
SPEED = 5                  # pixel ανά καρέ
FAST_SPEED = 10            # pixel ανά καρέ, όσο κρατάς το SHIFT

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
RED = (220, 60, 60)
ORANGE = (240, 160, 60)
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
wall = pygame.Rect(430, 100, 40, 260)
speed = SPEED              # η ταχύτητα αυτού του καρέ: με το SHIFT γίνεται FAST_SPEED
touching = False           # True όταν ο παίκτης και ο τοίχος επικαλύπτονται
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
            speed = FAST_SPEED
        if keys[pygame.K_LEFT]:
            player.x -= speed
            if player.colliderect(wall):
                # TODO 1: αν ο παίκτης χτύπησε τον τοίχο, ακυρώνουμε την κίνηση: προσθέτουμε πίσω όσο αφαιρέσαμε
                player.x += ____
        if keys[pygame.K_RIGHT]:
            player.x += speed
            # TODO 2: ρωτάμε αν ο παίκτης και ο τοίχος επικαλύπτονται
            if player.____(wall):
                player.x -= speed
        if keys[pygame.K_UP]:
            player.y -= speed
            if player.colliderect(wall):
                # TODO 3: το πάνω βέλος μίκρυνε το y· για να το ακυρώσουμε, το μεγαλώνουμε
                player.y ____ speed
        if keys[pygame.K_DOWN]:
            player.y += speed
            if player.colliderect(wall):
                player.y -= speed
        # όρια: αν ένα άκρο του παίκτη ξεπεράσει ένα όριο, τον βάζουμε ακριβώς πάνω στο όριο
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top < HUD_HEIGHT:
            player.top = HUD_HEIGHT
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        touching = player.colliderect(wall)
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    pygame.draw.rect(screen, ORANGE, wall)
    if touching:
        color = RED
    else:
        color = GREEN
    pygame.draw.rect(screen, color, player)
    draw_watch(screen, small_font, [("frame", frame), ("player", player), ("player.right", player.right), ("wall.left", wall.left), ("touching", touching)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
