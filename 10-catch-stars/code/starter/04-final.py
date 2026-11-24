"""Στάδιο 4 — Το ολοκληρωμένο παιχνίδι, με καταστάσεις και αυξανόμενη δυσκολία.

Συμπλήρωσε τα οκτώ κενά (____). Όσο πιάνεις αστέρια, ο χρονιστής ξαναρυθμίζεται και τα αστέρια εμφανίζονται πιο συχνά. Το
παιχνίδι τελειώνει όταν φτάσεις τον στόχο ή χάσεις όλες τις ζωές.
"""
import math
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
GOAL = 15                  # πόσα αστέρια πρέπει να πιάσεις για να κερδίσεις
START_INTERVAL = 1000      # χιλιοστά του δευτερολέπτου ανάμεσα σε δύο αστέρια, στην αρχή
MAX_DT = 0.05

SPAWN_STAR = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής

PLAYING = "playing"
WON = "won"
LOST = "lost"

BACKGROUND = (25, 35, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)
YELLOW = (255, 210, 70)
RED = (220, 60, 60)
GREEN = (90, 220, 150)
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


def spawn_interval(score):
    """Ο χρόνος ανάμεσα σε δύο αστέρια, σε χιλιοστά: 1000 στην αρχή, 150 λιγότερα για κάθε 3 πόντους, ποτέ κάτω από 400."""
    return max(400, 1000 - 150 * (score // 3))


def distance(x1, y1, x2, y2):
    """Η απόσταση ανάμεσα στα σημεία (x1, y1) και (x2, y2)."""
    return math.hypot(x2 - x1, y2 - y1)


def circle_touches_rect(cx, cy, radius, left, top, width, height):
    """True αν ο κύκλος με κέντρο (cx, cy) και ακτίνα radius ακουμπά το ορθογώνιο (left, top, width, height)."""
    nearest_x = max(left, min(cx, left + width))
    nearest_y = max(top, min(cy, top + height))
    return distance(cx, cy, nearest_x, nearest_y) <= radius


def game_status(score, lives, goal):
    """Η κατάσταση του παιχνιδιού: WON αν οι πόντοι έφτασαν τον στόχο, αλλιώς LOST αν τελείωσαν οι ζωές, αλλιώς PLAYING."""
    # TODO 1: οι πόντοι έφτασαν ή ξεπέρασαν τον στόχο
    if score ____ goal:
        return WON
    if lives <= 0:
        return LOST
    return PLAYING


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


def handle_key(event):
    """Χειριστής του συμβάντος KEYDOWN: λέει ποια ενέργεια ζητά το πλήκτρο ("quit", "space"), ή None αν δεν μας νοιάζει."""
    if event.key == pygame.K_ESCAPE:
        return "quit"
    if event.key == pygame.K_SPACE:
        return "space"
    return None


def handle_events():
    """Διαβάζει όλα τα συμβάντα του καρέ και επιστρέφει τη λίστα των ενεργειών που ζητήθηκαν, με τη σειρά τους."""
    actions = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append("quit")
        elif event.type == SPAWN_STAR:
            # TODO 2: η ενέργεια μπαίνει στο τέλος της λίστας
            actions.____("spawn")
        elif event.type == pygame.KEYDOWN:
            action = handle_key(event)
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
interval = START_INTERVAL
state = PLAYING
pygame.time.set_timer(SPAWN_STAR, interval)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for action in handle_events():
        if action == "quit":
            running = False
        # TODO 3: το SPACE ξεκινά νέο παιχνίδι μόνο όταν το παιχνίδι δεν παίζεται
        elif action == "space" and state ____ PLAYING:
            stars = []
            score = 0
            lives = START_LIVES
            interval = START_INTERVAL
            state = PLAYING
            # TODO 4: ο χρονιστής ξεκινά ξανά με το αρχικό διάστημα
            pygame.time.set_timer(SPAWN_STAR, ____)
        elif action == "spawn" and state == PLAYING:
            x = random.randint(STAR_RADIUS, WIDTH - STAR_RADIUS)
            stars.append(Star(x, HUD_HEIGHT + STAR_RADIUS, random.randint(MIN_SPEED, MAX_SPEED)))

    keys = pygame.key.get_pressed()
    basket.move(key_direction(keys[pygame.K_LEFT], keys[pygame.K_RIGHT]), dt)

    if state == PLAYING:
        for star in stars:
            star.update(dt)

        # Πρώτο πέρασμα: τα αστέρια που πιάστηκαν
        remaining = []
        for star in stars:
            if star.touches(basket):
                score += 1
            else:
                remaining.append(star)
        stars = remaining

        # Δεύτερο πέρασμα: τα αστέρια που έπεσαν έξω από το παράθυρο
        survivors = remove_fallen(stars, HEIGHT + STAR_RADIUS)
        lives = max(0, lives - (len(stars) - len(survivors)))
        stars = survivors

        # Όσο αυξάνονται οι πόντοι, τα αστέρια εμφανίζονται πιο συχνά
        # TODO 5: το νέο διάστημα, από τους πόντους
        new_interval = ____(score)
        # TODO 6: ο χρονιστής ξαναρυθμίζεται μόνο όταν το διάστημα άλλαξε
        if new_interval ____ interval:
            interval = new_interval
            pygame.time.set_timer(SPAWN_STAR, interval)

        # TODO 7: η συνάρτηση που αποφασίζει την κατάσταση
        state = ____(score, lives, GOAL)
        if state != PLAYING:
            stars = []
            # TODO 8: το διάστημα 0 σταματά τον χρονιστή
            pygame.time.set_timer(SPAWN_STAR, ____)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Πόντοι: {score} από {GOAL}", YELLOW, (20, 20))
    draw_text(screen, font, f"Ζωές: {lives}", RED, (WIDTH - 130, 20))
    for star in stars:
        draw_star(screen, star)
    draw_basket(screen, basket)
    if state == WON:
        draw_centered_text(screen, font, f"Κέρδισες. Έπιασες {GOAL} αστέρια.", GREEN, (WIDTH // 2, 200))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι.", WHITE, (WIDTH // 2, 250))
    elif state == LOST:
        draw_centered_text(screen, font, f"Έχασες. Έπιασες {score} αστέρια.", RED, (WIDTH // 2, 200))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι.", WHITE, (WIDTH // 2, 250))
    pygame.display.flip()

pygame.quit()
