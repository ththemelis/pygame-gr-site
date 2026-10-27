"""Πρότυπο παιχνιδιού (Μάθημα 14). Τρέχει όπως είναι: μενού, παιχνίδι, τέλος, και ξανά από την αρχή.

Το παιχνίδι του προτύπου είναι προσωρινό: ένα τετράγωνο που κινείται με τα βέλη (ή τα W, A, S, D) και ένας χρόνος που
τελειώνει μετά από 5 δευτερόλεπτα. Αντικαταστήστε το με τον δικό σας κανόνα. Όσα αλλάζετε έχουν το σχόλιο ΑΛΛΑΞΤΕ ή
ΣΒΗΣΤΕ ΤΟ. Οι καταστάσεις και οι μικρές συναρτήσεις χωρίς pygame βρίσκονται στο logic.py."""
import pygame

from logic import GAME_OVER, MENU, PLAYING, move, new_game, next_state

pygame.init()

# ---- 1. Ρυθμίσεις: όλες οι σταθερές του παιχνιδιού

TITLE = "Το παιχνίδι μας"          # ΑΛΛΑΞΤΕ: ο τίτλος του παραθύρου και του μενού
WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 50                    # το ύψος της ζώνης με τις ενδείξεις, πάνω πάνω
FPS = 60
MAX_DT = 0.05                      # ένα καρέ που άργησε δεν κάνει τα αντικείμενα να πηδούν (όπως στα Μ11 και Μ12)
PLAYER_SIZE = 40
PLAYER_SPEED = 240                 # σε pixel το δευτερόλεπτο
DEMO_SECONDS = 5                   # ΣΒΗΣΤΕ ΤΟ: ο προσωρινός κανόνας του προτύπου (το παιχνίδι τελειώνει μετά από 5 δευτερόλεπτα)

BACKGROUND = (25, 35, 60)
HUD_COLOR = (12, 18, 36)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)
GREY = (120, 130, 150)
RED = (220, 60, 60)
PLAYER_COLOR = (90, 220, 150)

PLAY_AREA = pygame.Rect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT)    # η περιοχή όπου παίζεται το παιχνίδι
PANEL = pygame.Rect(120, 140, 400, 220)                               # το πλαίσιο του τέλους του παιχνιδιού
START_X = (WIDTH - PLAYER_SIZE) / 2                                   # ο παίκτης ξεκινά στο κέντρο της περιοχής
START_Y = HUD_HEIGHT + (HEIGHT - HUD_HEIGHT - PLAYER_SIZE) / 2

# ---- 2. Τα πλήκτρα κάθε κατάστασης: (κατάσταση, πλήκτρο) -> ενέργεια. Οι ενέργειες μπαίνουν στον πίνακα μεταβάσεων του logic.py

KEY_ACTIONS = {
    (MENU, pygame.K_SPACE): "play",
    (MENU, pygame.K_ESCAPE): "quit",
    (PLAYING, pygame.K_ESCAPE): "menu",
    (GAME_OVER, pygame.K_SPACE): "play",
    (GAME_OVER, pygame.K_ESCAPE): "menu",
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()


# ---- 3. Είσοδος και κανόνες

def handle_events(state):
    """Διαβάζει τα συμβάντα του καρέ και επιστρέφει τη λίστα των ενεργειών που ζητήθηκαν, με τη σειρά τους."""
    actions = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append("quit")
        elif event.type == pygame.KEYDOWN:
            action = KEY_ACTIONS.get((state, event.key))
            if action is not None:
                actions.append(action)
        # ΠΡΟΣΘΕΣΤΕ ΕΔΩ ό,τι άλλο ακούει το παιχνίδι σας: κλικ του ποντικιού (Μ12), χρονιστές με USEREVENT (Μ10)
    return actions


def read_direction():
    """Η κατεύθυνση που ζητά ο παίκτης με τα πλήκτρα που κρατιούνται: ένα ζευγάρι (dx, dy) με τιμές -1, 0 ή 1."""
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += 1
    return dx, dy


def update_game(game, dt):
    """Ένα καρέ του παιχνιδιού. ΕΔΩ ΜΠΑΙΝΕΙ Ο ΚΑΝΟΝΑΣ ΣΑΣ.

    Αλλάζει τα δεδομένα του game και επιστρέφει μια ενέργεια για τον πίνακα μεταβάσεων (π.χ. «lose» όταν χάνει ο παίκτης),
    ή None αν το παιχνίδι συνεχίζεται."""
    dx, dy = read_direction()
    game["x"] = move(game["x"], dx, PLAYER_SPEED, dt, PLAY_AREA.left, PLAY_AREA.right - PLAYER_SIZE)
    game["y"] = move(game["y"], dy, PLAYER_SPEED, dt, PLAY_AREA.top, PLAY_AREA.bottom - PLAYER_SIZE)
    game["time"] += dt
    game["score"] = int(game["time"])
    if game["time"] >= DEMO_SECONDS:        # ΣΒΗΣΤΕ ΤΟ: ο προσωρινός κανόνας
        return "lose"
    return None


# ---- 4. Σχεδίαση

def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def draw_player(surface, game):
    """Ζωγραφίζει τον παίκτη στη θέση του (οι συντεταγμένες στρογγυλεύονται σε ακέραιους pixel)."""
    rect = pygame.Rect(round(game["x"]), round(game["y"]), PLAYER_SIZE, PLAYER_SIZE)
    pygame.draw.rect(surface, PLAYER_COLOR, rect)


def draw_hud(surface, font, game):
    """Ζωγραφίζει τη ζώνη των ενδείξεων."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    draw_text(surface, font, f"Πόντοι: {game['score']}", YELLOW, (20, 14))
    draw_text(surface, font, "Βέλη ή WASD", GREY, (WIDTH - 180, 14))


def draw_menu(surface):
    """Ζωγραφίζει το μενού."""
    draw_centered_text(surface, title_font, TITLE, YELLOW, (WIDTH // 2, 170))
    draw_centered_text(surface, font, "SPACE: παίξε · ESC: έξοδος", GREY, (WIDTH // 2, 300))


def draw_game_over(surface, game):
    """Ζωγραφίζει το πλαίσιο του τέλους του παιχνιδιού."""
    pygame.draw.rect(surface, HUD_COLOR, PANEL)
    pygame.draw.rect(surface, GREY, PANEL, 2)
    draw_centered_text(surface, font, "Τέλος παιχνιδιού", RED, (WIDTH // 2, 195))
    draw_centered_text(surface, font, f"Πόντοι: {game['score']}", WHITE, (WIDTH // 2, 245))
    draw_centered_text(surface, font, "SPACE: ξανά · ESC: μενού", GREY, (WIDTH // 2, 320))


# ---- 5. Ο βρόχος του παιχνιδιού

game = new_game(START_X, START_Y)
state = MENU

running = True
while running:
    dt = min(clock.tick(FPS) / 1000, MAX_DT)

    for action in handle_events(state):
        new_state = next_state(state, action)
        if action == "quit":
            running = False
        elif new_state != state:
            if action == "play":
                game = new_game(START_X, START_Y)      # νέο παιχνίδι: τα δεδομένα ξαναρχίζουν από την αρχή
            state = new_state

    if state == PLAYING:
        action = update_game(game, dt)
        if action is not None:
            state = next_state(state, action)

    screen.fill(BACKGROUND)
    if state == MENU:
        draw_menu(screen)
    else:
        draw_player(screen, game)
        draw_hud(screen, font, game)
        if state == GAME_OVER:
            draw_game_over(screen, game)
    pygame.display.flip()

pygame.quit()
