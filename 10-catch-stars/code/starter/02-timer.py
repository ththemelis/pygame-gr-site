"""Στάδιο 2 — Ο χρονιστής: ένα νέο αστέρι κάθε δευτερόλεπτο, χωρίς κλικ.

Συμπλήρωσε τα έξι κενά (____). Η set_timer στέλνει το δικό σου συμβάν SPAWN_STAR κάθε SPAWN_INTERVAL χιλιοστά του
δευτερολέπτου, και ο βρόχος φτιάχνει ένα αστέρι κάθε φορά που το λαμβάνει.
"""
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
STAR_RADIUS = 14
MIN_SPEED = 120            # η ταχύτητα κάθε αστεριού είναι τυχαία, σε pixel το δευτερόλεπτο
MAX_SPEED = 220
SPAWN_INTERVAL = 1000      # χιλιοστά του δευτερολέπτου ανάμεσα σε δύο αστέρια
MAX_DT = 0.05

# TODO 1: ο πρώτος αριθμός συμβάντος που είναι δικός σου
SPAWN_STAR = pygame.____ + 1      # το συμβάν που στέλνει ο χρονιστής

BACKGROUND = (25, 35, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)
YELLOW = (255, 210, 70)

# Οι κορυφές του αστεριού, ως μετατοπίσεις από το κέντρο του
STAR_SHAPE = ((0, -14), (4, -5), (13, -4), (6, 2), (8, 11), (0, 6), (-8, 11), (-6, 2), (-13, -4), (-4, -5))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πιάσε τα αστέρια")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


def remove_fallen(stars, limit):
    """Επιστρέφει νέα λίστα με τα αστέρια που δεν έχουν περάσει το όριο limit (δηλαδή με y <= limit)."""
    remaining = []
    for star in stars:
        if star.y <= limit:
            remaining.append(star)
    return remaining


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


stars = []
created = 0
# TODO 2: η συνάρτηση που ξεκινά τον χρονιστή: συμβάν και χιλιοστά του δευτερολέπτου
pygame.time.____(SPAWN_STAR, SPAWN_INTERVAL)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO 3: το συμβάν του χρονιστή
        elif event.type == ____:
            # TODO 4: τυχαίος ακέραιος, με τα δύο άκρα
            x = random.____(STAR_RADIUS, WIDTH - STAR_RADIUS)
            stars.append(Star(x, HUD_HEIGHT + STAR_RADIUS, random.randint(MIN_SPEED, MAX_SPEED)))
            # TODO 5: ο μετρητής αυξάνεται κατά 1
            created ____ 1

    for star in stars:
        star.update(dt)
    stars = remove_fallen(stars, HEIGHT + STAR_RADIUS)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    # TODO 6: το πλήθος των στοιχείων της λίστας
    draw_text(screen, font, f"Στη λίστα: {____(stars)}", WHITE, (20, 20))
    draw_text(screen, font, f"Δημιουργήθηκαν: {created}", GREY, (WIDTH - 300, 20))
    for star in stars:
        draw_star(screen, star)
    pygame.display.flip()

pygame.quit()
