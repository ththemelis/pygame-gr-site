"""Στάδιο 3 — Συγκρούσεις: κουτιά σύγκρουσης, ζωές και εικονίδια ζωών.

Συμπλήρωσε τα οκτώ κενά (____). Ένας αστεροειδής που ακουμπά το διαστημόπλοιο εξαφανίζεται και κοστίζει μία ζωή. Οι ζωές
φαίνονται ως μικρά διαστημόπλοια στο HUD. Το Στάδιο 3 δεν έχει τέλος.
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
MIN_SPEED = 110                      # η ταχύτητα κάθε αστεροειδή είναι τυχαία, σε pixel το δευτερόλεπτο
MAX_SPEED = 190
SPAWN_INTERVAL = 800                 # χιλιοστά του δευτερολέπτου ανάμεσα σε δύο αστεροειδείς
MAX_DT = 0.05

SPAWN_ASTEROID = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής

HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Διαστημική αποφυγή")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Η περιοχή όπου κινείται το διαστημόπλοιο: όλο το παράθυρο κάτω από το HUD
PLAY_AREA = pygame.Rect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT)


def fit_size(width, height, new_width):
    """Το μέγεθος (πλάτος, ύψος) μιας εικόνας με πλάτος new_width, όταν διατηρεί τις αναλογίες της."""
    return new_width, round(height * new_width / width)


def load_image(path):
    """Φορτώνει μια εικόνα με διαφάνεια από το αρχείο path, έτοιμη για γρήγορη σχεδίαση."""
    return pygame.image.load(path).convert_alpha()


def resize(image, new_width):
    """Επιστρέφει νέα εικόνα με πλάτος new_width, χωρίς να παραμορφώνεται. Η αρχική εικόνα δεν αλλάζει."""
    size = fit_size(image.get_width(), image.get_height(), new_width)
    return pygame.transform.scale(image, size)


def hitbox(rect):
    """Το κουτί σύγκρουσης ενός sprite: το ορθογώνιο της εικόνας, μικρότερο κατά το ένα τέταρτο σε πλάτος και ύψος, με το ίδιο κέντρο."""
    # TODO 1: η μέθοδος που δίνει ορθογώνιο με το ίδιο κέντρο και άλλο μέγεθος
    return rect.____(-(rect.width // 4), -(rect.height // 4))


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
    # TODO 2: η μέθοδος που ελέγχει αν δύο ορθογώνια επικαλύπτονται
    return hitbox(asteroid.rect).____(hitbox(ship.rect))


def new_asteroid(top_speed):
    """Φτιάχνει έναν νέο αστεροειδή: τυχαία εικόνα, τυχαίο x και τυχαία ταχύτητα, ακριβώς πάνω από το HUD."""
    image = random.choice(ASTEROID_IMAGES)
    half = image.get_width() // 2
    x = random.randint(half, WIDTH - half)
    speed = random.randint(MIN_SPEED, top_speed)
    return Asteroid(image, x, HUD_HEIGHT - image.get_height() // 2, speed)


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_sprite(surface, sprite):
    """Ζωγραφίζει την εικόνα ενός sprite (διαστημόπλοιου ή αστεροειδή) στη θέση του ορθογωνίου του."""
    surface.blit(sprite.image, sprite.rect)


# Οι εικόνες φορτώνονται μία φορά, πριν από τον βρόχο
background = pygame.image.load("assets/background.png").convert()
ship_image = resize(load_image("assets/ship.png"), SHIP_WIDTH)
# TODO 3: η συνάρτηση που αλλάζει το μέγεθος μιας εικόνας, χωρίς να την παραμορφώνει
life_icon = ____(ship_image, LIFE_ICON_WIDTH)
ASTEROID_IMAGES = []
for path in ASTEROID_FILES:
    original = load_image(path)
    for width in ASTEROID_WIDTHS:
        ASTEROID_IMAGES.append(resize(original, width))

pygame.mouse.set_visible(False)       # το διαστημόπλοιο παίρνει τη θέση του δείκτη

ship = Ship(ship_image, WIDTH // 2, HEIGHT - 70)
asteroids = []
score = 0
lives = START_LIVES
pygame.time.set_timer(SPAWN_ASTEROID, SPAWN_INTERVAL)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            ship.move_to(event.pos[0], event.pos[1])
        elif event.type == SPAWN_ASTEROID:
            asteroids.append(new_asteroid(MAX_SPEED))

    # Κάθε αστεροειδής έχει τρεις δυνατότητες: χτυπά το διαστημόπλοιο, βγαίνει από το παράθυρο, ή συνεχίζει να πέφτει.
    hits = 0
    remaining = []
    for asteroid in asteroids:
        asteroid.update(dt)
        # TODO 4: ο αστεροειδής ακουμπά το διαστημόπλοιο
        if ____:
            # TODO 5: ένα χτύπημα παραπάνω
            hits ____ 1
        elif asteroid.rect.top > HEIGHT:
            score += 1
        else:
            remaining.append(asteroid)
    asteroids = remaining
    # TODO 6: οι ζωές δεν γίνονται ποτέ αρνητικές
    lives = ____(0, lives - hits)

    screen.blit(background, (0, 0))
    for asteroid in asteroids:
        draw_sprite(screen, asteroid)
    draw_sprite(screen, ship)
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Πόντοι: {score}", YELLOW, (20, 20))
    # TODO 7: ένα εικονίδιο για κάθε ζωή που απομένει
    for index in ____(lives):
        # TODO 8: ζωγράφισε το life_icon στη θέση (WIDTH - 140 + index * 40, 18): κάθε επόμενο εικονίδιο 40 pixel δεξιότερα (μία γραμμή)
        ____
    pygame.display.flip()

pygame.quit()
