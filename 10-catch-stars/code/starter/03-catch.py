"""Στάδιο 3 — Το καλάθι πιάνει τα αστέρια: απόσταση με το math, πόντοι και ζωές.

Συμπλήρωσε τα οκτώ κενά (____). Το καλάθι κινείται με τα βέλη. Ένα αστέρι που ακουμπά το καλάθι δίνει έναν πόντο, και ένα
αστέρι που πέφτει έξω από το παράθυρο κοστίζει μία ζωή.
"""
# TODO 1: το module με τα μαθηματικά
import ____
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
STAR_RADIUS = 14
MIN_SPEED = 120            # η ταχύτητα κάθε αστεριού είναι τυχαία, σε pixel το δευτερόλεπτο
MAX_SPEED = 220
BASKET_WIDTH = 90
BASKET_HEIGHT = 28
BASKET_SPEED = 420         # pixel το δευτερόλεπτο
BASKET_Y = HEIGHT - BASKET_HEIGHT - 12
START_LIVES = 3
SPAWN_INTERVAL = 1000      # χιλιοστά του δευτερολέπτου ανάμεσα σε δύο αστέρια
MAX_DT = 0.05

SPAWN_STAR = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής

BACKGROUND = (25, 35, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)
YELLOW = (255, 210, 70)
RED = (220, 60, 60)
ORANGE = (255, 170, 80)

# Οι κορυφές του αστεριού, ως μετατοπίσεις από το κέντρο του
STAR_SHAPE = ((0, -14), (4, -5), (13, -4), (6, 2), (8, 11), (0, 6), (-8, 11), (-6, 2), (-13, -4), (-4, -5))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πιάσε τα αστέρια")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


def key_direction(left_pressed, right_pressed):
    """-1 αν πατιέται μόνο το αριστερό πλήκτρο, 1 αν πατιέται μόνο το δεξί, και 0 σε κάθε άλλη περίπτωση."""
    if left_pressed and not right_pressed:
        return -1
    if right_pressed and not left_pressed:
        return 1
    return 0


def remove_fallen(stars, limit):
    """Επιστρέφει νέα λίστα με τα αστέρια που δεν έχουν περάσει το όριο limit (δηλαδή με y <= limit)."""
    remaining = []
    for star in stars:
        if star.y <= limit:
            remaining.append(star)
    return remaining


def distance(x1, y1, x2, y2):
    """Η απόσταση ανάμεσα στα σημεία (x1, y1) και (x2, y2)."""
    # TODO 2: η υποτείνουσα: η απόσταση από τις διαφορές των συντεταγμένων
    return math.____(x2 - x1, y2 - y1)


def circle_touches_rect(cx, cy, radius, left, top, width, height):
    """True αν ο κύκλος με κέντρο (cx, cy) και ακτίνα radius ακουμπά το ορθογώνιο (left, top, width, height)."""
    # TODO 3: το cx δεν ξεπερνά τη δεξιά πλευρά του ορθογωνίου
    nearest_x = max(left, ____(cx, left + width))
    nearest_y = max(top, min(cy, top + height))
    # TODO 4: ακουμπά όταν η απόσταση δεν είναι μεγαλύτερη από την ακτίνα
    return distance(cx, cy, nearest_x, nearest_y) ____ radius


class Star:
    """Ένα αστέρι που πέφτει: θέση του κέντρου, ακτίνα και ταχύτητα (σε pixel το δευτερόλεπτο)."""

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.radius = STAR_RADIUS
        self.speed = speed

    def update(self, dt):
        """Το αστέρι πέφτει."""
        self.y += self.speed * dt

    def touches(self, basket):
        """True αν το αστέρι ακουμπά το καλάθι."""
        left, top, width, height = basket.box()
        return circle_touches_rect(self.x, self.y, self.radius, left, top, width, height)


class Basket:
    """Το καλάθι: θέση της πάνω αριστερής γωνίας, μέγεθος και ταχύτητα (σε pixel το δευτερόλεπτο)."""

    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, direction, dt):
        """Μετακινεί το καλάθι (direction: -1 αριστερά, 0 ακίνητο, 1 δεξιά) και το κρατά μέσα στο παράθυρο."""
        self.x += direction * self.speed * dt
        self.x = max(0, min(self.x, WIDTH - self.width))

    def box(self):
        """Το ορθογώνιο του καλαθιού ως (x, y, πλάτος, ύψος), με το x στρογγυλοποιημένο."""
        return (round(self.x), self.y, self.width, self.height)


def star_points(x, y):
    """Οι κορυφές του αστεριού με κέντρο το (x, y)."""
    points = []
    for dx, dy in STAR_SHAPE:
        points.append((x + dx, y + dy))
    return points


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_star(surface, star):
    """Ζωγραφίζει το αστέρι."""
    pygame.draw.polygon(surface, YELLOW, star_points(star.x, star.y))


def draw_basket(surface, basket):
    """Ζωγραφίζει το καλάθι, με μια άσπρη λωρίδα στο πάνω μέρος του."""
    left, top, width, height = basket.box()
    pygame.draw.rect(surface, ORANGE, (left, top, width, height))
    pygame.draw.rect(surface, WHITE, (left, top, width, 4))


basket = Basket((WIDTH - BASKET_WIDTH) / 2, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT, BASKET_SPEED)
stars = []
score = 0
lives = START_LIVES
pygame.time.set_timer(SPAWN_STAR, SPAWN_INTERVAL)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == SPAWN_STAR:
            x = random.randint(STAR_RADIUS, WIDTH - STAR_RADIUS)
            stars.append(Star(x, HUD_HEIGHT + STAR_RADIUS, random.randint(MIN_SPEED, MAX_SPEED)))

    keys = pygame.key.get_pressed()
    basket.move(key_direction(keys[pygame.K_LEFT], keys[pygame.K_RIGHT]), dt)

    for star in stars:
        star.update(dt)

    # Πρώτο πέρασμα: τα αστέρια που πιάστηκαν
    remaining = []
    for star in stars:
        # TODO 5: η μέθοδος του αστεριού που ελέγχει αν ακουμπά το καλάθι
        if star.____(basket):
            # TODO 6: ένας πόντος παραπάνω
            score ____ 1
        else:
            remaining.append(star)
    # TODO 7: η λίστα με τα αστέρια που δεν πιάστηκαν
    stars = ____

    # Δεύτερο πέρασμα: τα αστέρια που έπεσαν έξω από το παράθυρο
    survivors = remove_fallen(stars, HEIGHT + STAR_RADIUS)
    # TODO 8: οι ζωές δεν πέφτουν ποτέ κάτω από το 0
    lives = ____(0, lives - (len(stars) - len(survivors)))
    stars = survivors

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Πόντοι: {score}", YELLOW, (20, 20))
    draw_text(screen, font, f"Ζωές: {lives}", RED, (WIDTH - 130, 20))
    for star in stars:
        draw_star(screen, star)
    draw_basket(screen, basket)
    pygame.display.flip()

pygame.quit()
