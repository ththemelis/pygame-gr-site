"""Στάδιο 3 — Ήχοι και μουσική: εφέ, μουσική, ένταση και σίγαση.

Συμπλήρωσε τα οκτώ κενά (____). Πρώτα τρέξε το make_sounds.py, για να φτιαχτούν οι ήχοι στον φάκελο assets. Τα πλήκτρα Πάνω και
Κάτω αλλάζουν την ένταση και το M κλείνει ή ανοίγει τον ήχο.
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
BUTTON_WIDTH = 260
BUTTON_HEIGHT = 50
SOUND_NAMES = ("click", "start", "point", "hit", "game_over")      # τα εφέ: assets/click.wav, assets/start.wav κ.λπ.
MUSIC_FILE = "assets/music.wav"
START_VOLUME = 0.5                   # η ένταση του ήχου στην αρχή, από 0.0 έως 1.0
VOLUME_STEP = 0.1

SPAWN_ASTEROID = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής

MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game over"

# Ο πίνακας μεταβάσεων: (κατάσταση, ενέργεια) -> νέα κατάσταση. Ό,τι δεν υπάρχει εδώ δεν αλλάζει την κατάσταση.
TRANSITIONS = {
    (MENU, "play"): PLAYING,
    (PLAYING, "pause"): PAUSED,
    (PLAYING, "lose"): GAME_OVER,
    (PAUSED, "resume"): PLAYING,
    (PAUSED, "menu"): MENU,
    (GAME_OVER, "play"): PLAYING,
    (GAME_OVER, "menu"): MENU,
}

# Τα πλήκτρα κάθε κατάστασης: (κατάσταση, πλήκτρο) -> ενέργεια
KEY_ACTIONS = {
    (MENU, pygame.K_SPACE): "play",
    (MENU, pygame.K_ESCAPE): "quit",
    (PLAYING, pygame.K_p): "pause",
    (PLAYING, pygame.K_ESCAPE): "pause",
    (PAUSED, pygame.K_p): "resume",
    (PAUSED, pygame.K_ESCAPE): "resume",
    (PAUSED, pygame.K_q): "menu",
    (GAME_OVER, pygame.K_SPACE): "play",
    (GAME_OVER, pygame.K_ESCAPE): "menu",
}

# Τα πλήκτρα του ήχου δουλεύουν σε κάθε κατάσταση
SOUND_KEYS = {
    pygame.K_UP: "louder",
    pygame.K_DOWN: "quieter",
    pygame.K_m: "mute",
}

HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)
RED = (220, 60, 60)
BUTTON_COLOR = (36, 54, 104)
BUTTON_HOVER_COLOR = (62, 98, 176)
BUTTON_BORDER_COLOR = (200, 210, 235)

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
    return TRANSITIONS.get((state, action), state)


def change_volume(volume, step):
    """Η νέα ένταση: το άθροισμα volume + step, ανάμεσα στο 0.0 και στο 1.0, στρογγυλοποιημένο στο ένα δεκαδικό ψηφίο."""
    # TODO 1: η ένταση δεν ξεπερνά ποτέ το 1.0
    return round(max(0.0, ____(1.0, volume + step)), 1)


def volume_text(volume, muted):
    """Το κείμενο της έντασης: «Ήχος: 70%» (στρογγυλοποιημένο στο εκατοστό) ή «Ήχος: κλειστός» όταν ο ήχος είναι κλειστός."""
    if muted:
        return "Ήχος: κλειστός"
    return f"Ήχος: {round(volume * 100)}%"


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


def apply_volume(sounds, volume, muted):
    """Βάζει την ίδια ένταση σε όλα τα εφέ και στη μουσική: 0 όταν ο ήχος είναι κλειστός."""
    level = 0.0 if muted else volume
    for sound in sounds.values():
        # TODO 2: η μέθοδος που βάζει την ένταση ενός εφέ
        sound.____(level)
    pygame.mixer.music.set_volume(level)


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


class Button:
    """Ένα κουμπί: το κείμενό του, η ενέργεια που ζητά όταν πατηθεί και το ορθογώνιό του. Θυμάται αν το ποντίκι είναι πάνω του."""

    def __init__(self, text, center, action):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect.center = center
        self.hovered = False

    def update(self, position):
        """Θυμάται αν το ποντίκι, στη θέση position, είναι πάνω στο κουμπί."""
        self.hovered = self.rect.collidepoint(position)

    def is_clicked(self, position):
        """True αν ένα κλικ στη θέση position πέφτει μέσα στο κουμπί."""
        return self.rect.collidepoint(position)

    def draw(self, surface, font):
        """Ζωγραφίζει το κουμπί: γέμισμα (πιο φωτεινό όταν το ποντίκι είναι πάνω του), περίγραμμα και το κείμενο στο κέντρο."""
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BUTTON_BORDER_COLOR, self.rect, 2)
        image = font.render(self.text, True, WHITE)
        surface.blit(image, image.get_rect(center=self.rect.center))


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


def handle_events(state, ship, buttons):
    """Διαβάζει όλα τα συμβάντα του καρέ και επιστρέφει τη λίστα των ενεργειών που ζητήθηκαν, με τη σειρά τους.

    Κινεί και το διαστημόπλοιο (μόνο όταν παίζεται το παιχνίδι) και θυμάται ποιο από τα κουμπιά έχει από πάνω το ποντίκι."""
    actions = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append("quit")
        elif event.type == SPAWN_ASTEROID:
            actions.append("spawn")
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.update(event.pos)
            if state == PLAYING:
                ship.move_to(event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                if button.is_clicked(event.pos):
                    actions.append("click")
                    actions.append(button.action)
        elif event.type == pygame.KEYDOWN:
            action = KEY_ACTIONS.get((state, event.key))
            if action is None:
                action = SOUND_KEYS.get(event.key)
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


def draw_buttons(surface, font, buttons):
    """Ζωγραφίζει όλα τα κουμπιά της λίστας."""
    for button in buttons:
        button.draw(surface, font)


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

sounds = {}
for name in SOUND_NAMES:
    # TODO 3: η κλάση που φορτώνει ένα σύντομο εφέ από αρχείο
    sounds[name] = pygame.mixer.____(f"assets/{name}.wav")
# TODO 4: φόρτωσε το αρχείο της μουσικής
pygame.mixer.music.____(MUSIC_FILE)

ship = Ship(ship_image, WIDTH // 2, HEIGHT - 70)
menu_buttons = [Button("Παίξε", (WIDTH // 2, 250), "play"), Button("Έξοδος", (WIDTH // 2, 320), "quit")]
pause_buttons = [Button("Συνέχεια", (WIDTH // 2, 250), "resume"), Button("Μενού", (WIDTH // 2, 315), "menu")]
over_buttons = [Button("Ξανά", (WIDTH // 2, 290), "play"), Button("Μενού", (WIDTH // 2, 350), "menu")]
BUTTONS = {MENU: menu_buttons, PAUSED: pause_buttons, GAME_OVER: over_buttons}

asteroids = []
score = 0
lives = START_LIVES
interval, top_speed = difficulty(score)
state = MENU
volume = START_VOLUME
muted = False
apply_volume(sounds, volume, muted)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for action in handle_events(state, ship, BUTTONS.get(state, [])):
        new_state = next_state(state, action)
        if action == "quit":
            running = False
        elif action == "click":
            sounds["click"].play()
        elif action == "spawn":
            if state == PLAYING:
                asteroids.append(new_asteroid(top_speed))
        elif action == "louder" or action == "quieter":
            step = VOLUME_STEP if action == "louder" else -VOLUME_STEP
            volume = change_volume(volume, step)
            muted = False
            apply_volume(sounds, volume, muted)
            sounds["click"].play()
        elif action == "mute":
            # TODO 5: η σίγαση αλλάζει από ανοιχτή σε κλειστή και αντίστροφα
            muted = ____ muted
            apply_volume(sounds, volume, muted)
        elif new_state != state:
            if action == "play":
                ship.move_to(WIDTH // 2, HEIGHT - 70)
                asteroids = []
                score = 0
                lives = START_LIVES
                interval, top_speed = difficulty(score)
                pygame.time.set_timer(SPAWN_ASTEROID, interval)
                sounds["start"].play()
                # TODO 6: η τιμή που κάνει τη μουσική να επαναλαμβάνεται χωρίς τέλος
                pygame.mixer.music.play(____)
            elif action == "pause":
                # TODO 7: σταμάτα προσωρινά τη μουσική (μία γραμμή)
                ____
            elif action == "resume":
                pygame.mixer.music.unpause()
            elif action == "menu":
                pygame.mixer.music.stop()
            state = new_state

    if state == PLAYING:
        # Κάθε αστεροειδής έχει τρεις δυνατότητες: χτυπά το διαστημόπλοιο, βγαίνει από το παράθυρο, ή συνεχίζει να πέφτει.
        old_score = score
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
        if score > old_score:
            sounds["point"].play()
        if hits > 0:
            # TODO 8: το εφέ του χτυπήματος
            sounds["____"].play()

        # Όσο αυξάνονται οι πόντοι, οι αστεροειδείς έρχονται πιο συχνά και πιο γρήγορα
        new_interval, top_speed = difficulty(score)
        if new_interval != interval:
            interval = new_interval
            pygame.time.set_timer(SPAWN_ASTEROID, interval)

        if lives == 0:
            state = next_state(state, "lose")
            asteroids = []
            pygame.time.set_timer(SPAWN_ASTEROID, 0)
            pygame.mixer.music.stop()
            sounds["game_over"].play()

    pygame.mouse.set_visible(state != PLAYING)
    screen.blit(background, (0, 0))
    if state == MENU:
        draw_centered_text(screen, title_font, "Διαστημική αποφυγή", YELLOW, (WIDTH // 2, 110))
        draw_buttons(screen, font, menu_buttons)
        draw_centered_text(screen, font, volume_text(volume, muted), GREY, (WIDTH // 2, 385))
        draw_centered_text(screen, font, "SPACE: παίξε · ESC: έξοδος", GREY, (WIDTH // 2, 428))
        draw_centered_text(screen, font, "Πάνω και Κάτω: ένταση · M: σίγαση", GREY, (WIDTH // 2, 456))
    else:
        for asteroid in asteroids:
            draw_sprite(screen, asteroid)
        if state == PLAYING or state == PAUSED:
            draw_sprite(screen, ship)
        draw_hud(screen, font, score, lives, life_icon)
        if state == PAUSED:
            draw_panel(screen)
            draw_centered_text(screen, title_font, "Παύση", YELLOW, (WIDTH // 2, 175))
            draw_buttons(screen, font, pause_buttons)
            draw_centered_text(screen, font, "P ή ESC: συνέχεια · Q: μενού", GREY, (WIDTH // 2, 385))
        elif state == GAME_OVER:
            draw_panel(screen)
            draw_centered_text(screen, font, "Τέλος παιχνιδιού", RED, (WIDTH // 2, 165))
            draw_centered_text(screen, font, f"Πόντοι: {score}", WHITE, (WIDTH // 2, 200))
            draw_buttons(screen, font, over_buttons)
            draw_centered_text(screen, font, "SPACE: ξανά · ESC: μενού", GREY, (WIDTH // 2, 392))
    pygame.display.flip()

pygame.quit()
