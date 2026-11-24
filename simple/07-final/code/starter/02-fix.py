"""Μ15, Στάδιο 2 — το παιχνίδι χωρίς τα τρία λάθη: ο πόντος προστίθεται, το αστέρι-ασπίδα πέφτει και το παιχνίδι τελειώνει όταν οι ζωές γίνουν 0.

Συμπλήρωσε τα τρία κενά (____).
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
ROCK_SIZE = 30
ROCK_SPEED = 4             # pixel ανά καρέ για κάθε βράχο
LIVES = 3                  # οι ζωές με τις οποίες ξεκινά ο παίκτης
START_ROCKS = 3            # όσοι βράχοι έχει η λίστα στην αρχή
NEW_ROCK_EVERY = 4         # κάθε τόσους πόντους προστίθεται νέος βράχος
MAX_ROCKS = 6              # οι περισσότεροι βράχοι που μπορεί να έχει η λίστα
SHIELD_FRAMES = 60         # για πόσα καρέ προστατεύει η ασπίδα μετά από ένα χτύπημα
ICON_X = 300               # πού ξεκινά το πρώτο εικονίδιο ζωής
ICON_STEP = 30             # πόσο απέχει κάθε εικονίδιο από το προηγούμενο
BONUS_POINTS = 3           # οι πόντοι που δίνει το αστέρι-μπόνους όταν το πιάνεις
DODGE_GOAL = 5             # κάθε τόσους βράχους που ξεφεύγεις παίρνεις μπόνους
DODGE_POINTS = 5           # οι πόντοι του μπόνους

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
BLUE = (90, 160, 255)
YELLOW = (250, 220, 90)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Μ15: ολοκλήρωση και φεστιβάλ")
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 64)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
def place_rock(rock):
    """Βάζει τον βράχο σε τυχαία θέση, ακριβώς κάτω από τη γραμμή HUD_HEIGHT. Αλλάζει το ίδιο το Rect που της δίνεις."""
    rock.x = random.randint(0, WIDTH - rock.width)
    rock.y = HUD_HEIGHT


def make_player():
    """Φτιάχνει το ορθογώνιο του παίκτη, κάτω στη μέση του παραθύρου."""
    return pygame.Rect(WIDTH // 2 - SIZE // 2, HEIGHT - SIZE, SIZE, SIZE)


def make_rocks():
    """Φτιάχνει τη λίστα με τους τρεις βράχους της αρχής."""
    return [
        pygame.Rect(300, HUD_HEIGHT, ROCK_SIZE, ROCK_SIZE),
        pygame.Rect(310, 160, ROCK_SIZE, ROCK_SIZE),
        pygame.Rect(500, 300, ROCK_SIZE, ROCK_SIZE),
    ]


def make_bonus():
    """Φτιάχνει το ορθογώνιο του αστεριού-μπόνους."""
    return pygame.Rect(320, 300, ROCK_SIZE, ROCK_SIZE)


def make_shield_star():
    """Φτιάχνει το ορθογώνιο του αστεριού-ασπίδας."""
    return pygame.Rect(270, 250, ROCK_SIZE, ROCK_SIZE)


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


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
player = make_player()
rocks = make_rocks()
bonus = make_bonus()
shield_star = make_shield_star()
wanted_rocks = START_ROCKS # πόσους βράχους θέλουμε σε αυτό το καρέ: εξαρτάται από το σκορ
score = 0
lives = LIVES
shield = 0                 # η ασπίδα: όσο είναι μεγαλύτερη από 0, δεν χάνεις ζωή
hits = 0                   # πόσες φορές άγγιξε βράχος τον παίκτη σε αυτό το παιχνίδι, ακόμη και όταν η ασπίδα προστάτευε
dodged = 0                 # πόσοι βράχοι πέρασαν από την τελευταία φορά που πήρες μπόνους
best = 0                   # το ρεκόρ: το μεγαλύτερο σκορ που έγινε από τότε που άνοιξε το πρόγραμμα
new_record = False         # True: το παιχνίδι που τελείωσε ξεπέρασε το ρεκόρ και δείχνει «Νέο ρεκόρ»
state = "menu"             # η κατάσταση του παιχνιδιού: "menu", "playing" ή "game over"
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
            elif state == "menu" and event.key == pygame.K_SPACE:
                state = "playing"
            elif state == "game over" and event.key == pygame.K_SPACE:
                # νέο παιχνίδι: όλα τα δεδομένα ξαναγυρίζουν στην αρχική τους τιμή και ξαναφαίνεται το μενού
                player = make_player()
                rocks = make_rocks()
                bonus = make_bonus()
                shield_star = make_shield_star()
                wanted_rocks = START_ROCKS
                score = 0
                lives = LIVES
                shield = 0
                hits = 0
                dodged = 0
                new_record = False
                state = "menu"
    keys = pygame.key.get_pressed()       # ποια πλήκτρα κρατιούνται πατημένα αυτή τη στιγμή

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if (not paused or step_once) and state == "playing":
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
        # η ασπίδα μετρά αντίστροφα: σε κάθε καρέ μειώνεται κατά 1, μέχρι να φτάσει το 0
        if shield > 0:
            shield -= 1
        # ο ίδιος κανόνας για κάθε βράχο της λίστας: πέφτει, και μετά ρωτάμε αν πέρασε από το παράθυρο και αν άγγιξε τον παίκτη
        for rock in rocks:
            rock.y += ROCK_SPEED
            if rock.top > HEIGHT:
                place_rock(rock)
                # TODO 1: ο πόντος προστίθεται στο σκορ που υπάρχει ήδη (ποιος τελεστής;)
                score ____ 1
                dodged += 1
                if dodged == DODGE_GOAL:
                    score += DODGE_POINTS
                    dodged = 0
            if player.colliderect(rock):
                place_rock(rock)
                hits += 1
                if shield == 0:
                    lives -= 1
                    shield = SHIELD_FRAMES
        # το αστέρι-μπόνους πέφτει όπως οι βράχοι· αν το πιάσεις, παίρνεις πόντους
        bonus.y += ROCK_SPEED
        if bonus.top > HEIGHT:
            place_rock(bonus)
        if player.colliderect(bonus):
            place_rock(bonus)
            score += BONUS_POINTS
            lives += 1
            lives = min(lives, LIVES)
        # το αστέρι-ασπίδα πέφτει όπως το αστέρι-μπόνους· αν το πιάσεις, παίρνεις ασπίδα
        # TODO 2: το αστέρι πέφτει, δηλαδή αλλάζει η κατακόρυφη θέση του (ποιο όνομα, x ή y;)
        shield_star.____ += ROCK_SPEED
        if shield_star.top > HEIGHT:
            place_rock(shield_star)
        if player.colliderect(shield_star):
            place_rock(shield_star)
            shield = SHIELD_FRAMES
        # όσοι βράχοι θέλουμε εξαρτώνται από το σκορ· αν η λίστα έχει λιγότερους, προσθέτουμε νέο βράχο
        wanted_rocks = START_ROCKS + score // NEW_ROCK_EVERY
        wanted_rocks = min(wanted_rocks, MAX_ROCKS)
        if len(rocks) < wanted_rocks:
            new_rock = pygame.Rect(0, HUD_HEIGHT, ROCK_SIZE, ROCK_SIZE)
            place_rock(new_rock)
            rocks.append(new_rock)
        # όταν οι ζωές τελειώσουν, το παιχνίδι τελειώνει και ίσως έχουμε νέο ρεκόρ
        # TODO 3: το παιχνίδι τελειώνει όταν οι ζωές γίνουν 0 ή λιγότερες (ποιο σύμβολο σύγκρισης;)
        if lives ____ 0:
            if score > best:
                best = score
                new_record = True
            state = "game over"
    step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    if state == "menu":
        draw_centered_text(screen, title_font, "Αποφυγή βράχων", YELLOW, (WIDTH // 2, 150))
        draw_centered_text(screen, font, "Πάτα SPACE για να παίξεις", WHITE, (WIDTH // 2, 240))
        draw_centered_text(screen, font, f"Ρεκόρ: {best}", WHITE, (WIDTH // 2, 300))
    else:
        pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
        draw_text(screen, font, f"Σκορ: {score}", WHITE, (20, 30))
        draw_text(screen, font, "Ζωές:", WHITE, (220, 30))
        for icon in range(lives):
            pygame.draw.rect(screen, GREEN, (ICON_X + ICON_STEP * icon, 32, 20, 20))
        draw_text(screen, font, f"Βράχοι: {len(rocks)}", WHITE, (420, 30))
        draw_text(screen, font, f"Χτυπήματα: {hits}", WHITE, (20, 6))
        draw_text(screen, font, f"Ξέφυγες: {dodged}", WHITE, (220, 6))
        for rock in rocks:
            pygame.draw.rect(screen, RED, rock)
        pygame.draw.circle(screen, YELLOW, bonus.center, ROCK_SIZE // 2)
        pygame.draw.circle(screen, BLUE, shield_star.center, ROCK_SIZE // 2)
        ship = [(player.centerx, player.top), (player.left, player.bottom), (player.right, player.bottom)]
        if shield > 0:
            pygame.draw.polygon(screen, BLUE, ship)
        else:
            pygame.draw.polygon(screen, GREEN, ship)
        if state == "game over":
            if new_record:
                draw_centered_text(screen, font, "Νέο ρεκόρ", GREEN, (WIDTH // 2, HEIGHT // 2 - 80))
            draw_centered_text(screen, font, "Τέλος παιχνιδιού", WHITE, (WIDTH // 2, HEIGHT // 2 - 40))
            draw_centered_text(screen, font, f"Τελικό σκορ: {score}", YELLOW, (WIDTH // 2, HEIGHT // 2))
            draw_centered_text(screen, font, f"Ρεκόρ: {best}", WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
            draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι", WHITE, (WIDTH // 2, HEIGHT // 2 + 80))
    draw_watch(screen, small_font, [("frame", frame), ("state", state), ("score", score), ("lives", lives), ("shield_star.y", shield_star.y)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
