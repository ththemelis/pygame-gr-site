"""Στάδιο 1 — Καταστάσεις: μενού, παιχνίδι, παύση και τέλος παιχνιδιού.

Συμπλήρωσε τα οκτώ κενά (____). Το πρόγραμμα έχει τέσσερις καταστάσεις. Τα συμβάντα γίνονται ενέργειες («play», «pause» κ.λπ.)
και ο πίνακας μεταβάσεων λέει ποια κατάσταση ακολουθεί. Πρώτα τρέξε το make_assets.py, για να φτιαχτεί ο φάκελος assets.
"""
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
SHIP_WIDTH = 64            # το πλάτος του διαστημόπλοιου στην οθόνη, σε pixel
LIFE_ICON_WIDTH = 32       # το πλάτος του εικονιδίου κάθε ζωής
START_LIVES = 3
ASTEROID_FILES = ("assets/asteroid-1.png", "assets/asteroid-2.png")
ASTEROID_WIDTHS = (48, 72)           # κάθε αστεροειδής εμφανίζεται σε δύο μεγέθη
MIN_SPEED = 110                      # η ελάχιστη ταχύτητα ενός αστεροειδή, σε pixel το δευτερόλεπτο
MAX_DT = 0.05

SPAWN_ASTEROID = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής

MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game over"

# Ο πίνακας μεταβάσεων: (κατάσταση, ενέργεια) -> νέα κατάσταση. Ό,τι δεν υπάρχει εδώ δεν αλλάζει την κατάσταση.
TRANSITIONS = {
    (MENU, "play"): PLAYING,
    # TODO 1: από το παιχνίδι, η ενέργεια «pause» πηγαίνει στην παύση
    (PLAYING, "pause"): ____,
    (PLAYING, "lose"): GAME_OVER,
    # TODO 2: από την παύση, η ενέργεια «resume» γυρίζει στο παιχνίδι
    (PAUSED, "resume"): ____,
    (PAUSED, "menu"): MENU,
    (GAME_OVER, "play"): PLAYING,
    (GAME_OVER, "menu"): MENU,
}

# Τα πλήκτρα κάθε κατάστασης: (κατάσταση, πλήκτρο) -> ενέργεια
KEY_ACTIONS = {
    (MENU, pygame.K_SPACE): "play",
    (MENU, pygame.K_ESCAPE): "quit",
    # TODO 3: το πλήκτρο P ζητά την ενέργεια που σταματά το παιχνίδι
    (PLAYING, pygame.K_p): "____",
    (PLAYING, pygame.K_ESCAPE): "pause",
    (PAUSED, pygame.K_p): "resume",
    (PAUSED, pygame.K_ESCAPE): "resume",
    (PAUSED, pygame.K_q): "menu",
    (GAME_OVER, pygame.K_SPACE): "play",
    (GAME_OVER, pygame.K_ESCAPE): "menu",
}

HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)
RED = (220, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Διαστημική αποφυγή")
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 64)
clock = pygame.time.Clock()

# Η περιοχή όπου κινείται το διαστημόπλοιο: όλο το παράθυρο κάτω από το HUD
PLAY_AREA = pygame.Rect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT)
# Το πλαίσιο της παύσης και του τέλους του παιχνιδιού
PANEL = pygame.Rect(120, 130, 400, 290)


def fit_size(width, height, new_width):
    """Το μέγεθος (πλάτος, ύψος) μιας εικόνας με πλάτος new_width, όταν διατηρεί τις αναλογίες της."""
    return new_width, round(height * new_width / width)


def difficulty(score):
    """Επιστρέφει (διάστημα, μέγιστη ταχύτητα) για τους πόντους score.

    Για κάθε 5 πόντους το διάστημα ανάμεσα σε δύο αστεροειδείς μικραίνει κατά 60 χιλιοστά του δευτερολέπτου (από 800, ποτέ
    κάτω από 300) και η μέγιστη ταχύτητα μεγαλώνει κατά 15 (από 190, ποτέ πάνω από 330).
    """
    level = score // 5
    interval = max(300, 800 - 60 * level)
    top_speed = min(330, 190 + 15 * level)
    return interval, top_speed


def next_state(state, action):
    """Η νέα κατάσταση μετά από μια ενέργεια. Αν η ενέργεια δεν αλλάζει κάτι σε αυτή την κατάσταση, επιστρέφει την ίδια."""
    # TODO 4: αν το ζεύγος (κατάσταση, ενέργεια) δεν υπάρχει στον πίνακα, η κατάσταση μένει ίδια
    return TRANSITIONS.get((state, action), ____)


def load_image(path):
    """Φορτώνει μια εικόνα με διαφάνεια από το αρχείο path, έτοιμη για γρήγορη σχεδίαση."""
    return pygame.image.load(path).convert_alpha()


def resize(image, new_width):
    """Επιστρέφει νέα εικόνα με πλάτος new_width, χωρίς να παραμορφώνεται. Η αρχική εικόνα δεν αλλάζει."""
    size = fit_size(image.get_width(), image.get_height(), new_width)
    return pygame.transform.scale(image, size)


def hitbox(rect):
    """Το κουτί σύγκρουσης ενός sprite: το ορθογώνιο της εικόνας, μικρότερο κατά το ένα τέταρτο σε πλάτος και ύψος, με το ίδιο κέντρο."""
    return rect.inflate(-(rect.width // 4), -(rect.height // 4))


class Ship:
    """Το διαστημόπλοιο: η εικόνα του και το ορθογώνιό της. Ακολουθεί το ποντίκι."""

    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect(center=(x, y))

    def move_to(self, x, y):
        """Βάζει το κέντρο του διαστημόπλοιου στο (x, y) και το κρατά μέσα στην περιοχή παιχνιδιού."""
        self.rect.center = (x, y)
        self.rect.clamp_ip(PLAY_AREA)


class Asteroid:
    """Ένας αστεροειδής που πέφτει: η εικόνα του, η ακριβής θέση του κέντρου του (x, y) και η ταχύτητά του (pixel το δευτερόλεπτο)."""

    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = image.get_rect(center=(round(x), round(y)))

    def update(self, dt):
        """Ο αστεροειδής πέφτει, και το ορθογώνιό του ακολουθεί την ακριβή θέση."""
        self.y += self.speed * dt
        self.rect.center = (round(self.x), round(self.y))


def collides(asteroid, ship):
    """True αν τα κουτιά σύγκρουσης του αστεροειδή και του διαστημόπλοιου επικαλύπτονται."""
    return hitbox(asteroid.rect).colliderect(hitbox(ship.rect))


def new_asteroid(top_speed):
    """Φτιάχνει έναν νέο αστεροειδή: τυχαία εικόνα, τυχαίο x και τυχαία ταχύτητα, ακριβώς πάνω από το HUD."""
    image = random.choice(ASTEROID_IMAGES)
    half = image.get_width() // 2
    x = random.randint(half, WIDTH - half)
    speed = random.randint(MIN_SPEED, top_speed)
    return Asteroid(image, x, HUD_HEIGHT - image.get_height() // 2, speed)


def handle_events(state, ship):
    """Διαβάζει όλα τα συμβάντα του καρέ και επιστρέφει τη λίστα των ενεργειών που ζητήθηκαν, με τη σειρά τους.

    Κινεί και το διαστημόπλοιο, αλλά μόνο όταν παίζεται το παιχνίδι."""
    actions = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append("quit")
        elif event.type == SPAWN_ASTEROID:
            actions.append("spawn")
        elif event.type == pygame.MOUSEMOTION:
            if state == PLAYING:
                ship.move_to(event.pos[0], event.pos[1])
        elif event.type == pygame.KEYDOWN:
            action = KEY_ACTIONS.get((state, event.key))
            if action is not None:
                actions.append(action)
    return actions


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def draw_sprite(surface, sprite):
    """Ζωγραφίζει την εικόνα ενός sprite (διαστημόπλοιου ή αστεροειδή) στη θέση του ορθογωνίου του."""
    surface.blit(sprite.image, sprite.rect)


def draw_hud(surface, font, score, lives, life_icon):
    """Ζωγραφίζει την περιοχή των ενδείξεων: οι πόντοι και ένα εικονίδιο για κάθε ζωή που απομένει."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(surface, font, f"Πόντοι: {score}", YELLOW, (20, 20))
    for index in range(lives):
        surface.blit(life_icon, (WIDTH - 140 + index * 40, 18))


def draw_panel(surface):
    """Ζωγραφίζει το πλαίσιο της παύσης και του τέλους του παιχνιδιού."""
    pygame.draw.rect(surface, HUD_COLOR, PANEL)
    pygame.draw.rect(surface, GREY, PANEL, 2)


# Οι εικόνες και οι ήχοι φορτώνονται μία φορά, πριν από τον βρόχο
background = pygame.image.load("assets/background.png").convert()
ship_image = resize(load_image("assets/ship.png"), SHIP_WIDTH)
life_icon = resize(ship_image, LIFE_ICON_WIDTH)
ASTEROID_IMAGES = []
for path in ASTEROID_FILES:
    original = load_image(path)
    for width in ASTEROID_WIDTHS:
        ASTEROID_IMAGES.append(resize(original, width))

ship = Ship(ship_image, WIDTH // 2, HEIGHT - 70)

asteroids = []
score = 0
lives = START_LIVES
interval, top_speed = difficulty(score)
state = MENU

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for action in handle_events(state, ship):
        new_state = next_state(state, action)
        if action == "quit":
            running = False
        elif action == "spawn":
            if state == PLAYING:
                asteroids.append(new_asteroid(top_speed))
        elif new_state != state:
            if action == "play":
                ship.move_to(WIDTH // 2, HEIGHT - 70)
                asteroids = []
                score = 0
                lives = START_LIVES
                interval, top_speed = difficulty(score)
                pygame.time.set_timer(SPAWN_ASTEROID, interval)
            # TODO 5: η νέα κατάσταση ισχύει από εδώ και πέρα (μία γραμμή)
            ____

    if state == PLAYING:
        # Κάθε αστεροειδής έχει τρεις δυνατότητες: χτυπά το διαστημόπλοιο, βγαίνει από το παράθυρο, ή συνεχίζει να πέφτει.
        hits = 0
        remaining = []
        for asteroid in asteroids:
            asteroid.update(dt)
            if collides(asteroid, ship):
                hits += 1
            elif asteroid.rect.top > HEIGHT:
                score += 1
            else:
                remaining.append(asteroid)
        asteroids = remaining
        lives = max(0, lives - hits)

        # Όσο αυξάνονται οι πόντοι, οι αστεροειδείς έρχονται πιο συχνά και πιο γρήγορα
        new_interval, top_speed = difficulty(score)
        if new_interval != interval:
            interval = new_interval
            pygame.time.set_timer(SPAWN_ASTEROID, interval)

        if lives == 0:
            # TODO 6: οι ζωές τελείωσαν: ζήτα την ενέργεια «lose» και πάρε τη νέα κατάσταση (μία γραμμή)
            ____
            asteroids = []
            pygame.time.set_timer(SPAWN_ASTEROID, 0)

    # TODO 7: ο δείκτης του ποντικιού φαίνεται σε κάθε κατάσταση εκτός από το παιχνίδι
    pygame.mouse.set_visible(state ____ PLAYING)
    screen.blit(background, (0, 0))
    if state == MENU:
        draw_centered_text(screen, title_font, "Διαστημική αποφυγή", YELLOW, (WIDTH // 2, 110))
        draw_centered_text(screen, font, "SPACE: παίξε · ESC: έξοδος", GREY, (WIDTH // 2, 428))
    else:
        for asteroid in asteroids:
            draw_sprite(screen, asteroid)
        # TODO 8: το διαστημόπλοιο φαίνεται και όταν το παιχνίδι είναι σε παύση
        if state == PLAYING or state == ____:
            draw_sprite(screen, ship)
        draw_hud(screen, font, score, lives, life_icon)
        if state == PAUSED:
            draw_panel(screen)
            draw_centered_text(screen, title_font, "Παύση", YELLOW, (WIDTH // 2, 175))
            draw_centered_text(screen, font, "P ή ESC: συνέχεια · Q: μενού", GREY, (WIDTH // 2, 385))
        elif state == GAME_OVER:
            draw_panel(screen)
            draw_centered_text(screen, font, "Τέλος παιχνιδιού", RED, (WIDTH // 2, 165))
            draw_centered_text(screen, font, f"Πόντοι: {score}", WHITE, (WIDTH // 2, 200))
            draw_centered_text(screen, font, "SPACE: ξανά · ESC: μενού", GREY, (WIDTH // 2, 392))
    pygame.display.flip()

pygame.quit()
