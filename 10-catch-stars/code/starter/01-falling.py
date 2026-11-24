"""Στάδιο 1 — Αστέρια που πέφτουν: μια λίστα αντικειμένων, με κλικ ένα νέο αστέρι.

Συμπλήρωσε τα επτά κενά (____). Κάθε κλικ φτιάχνει ένα νέο αστέρι και το βάζει στη λίστα. Σε κάθε καρέ όλα τα αστέρια
πέφτουν, και όσα βγουν από το παράθυρο φεύγουν από τη λίστα.
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
MAX_DT = 0.05

BACKGROUND = (25, 35, 60)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)
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
        # TODO 1: το αστέρι μένει στη λίστα όσο δεν έχει περάσει το όριο
        if star.y ____ limit:
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
    # TODO 2: η λίστα με τις μετατοπίσεις των κορυφών του αστεριού
    for dx, dy in ____:
        # TODO 3: η μέθοδος της λίστας που προσθέτει στοιχείο στο τέλος
        points.____((x + dx, y + dy))
    return points


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


# TODO 4: η λίστα των αστεριών ξεκινά κενή
stars = ____

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # TODO 5: ένα νέο αστέρι μπαίνει στο τέλος της λίστας
            stars.____(Star(event.pos[0], HUD_HEIGHT + STAR_RADIUS, random.randint(MIN_SPEED, MAX_SPEED)))

    for star in stars:
        # TODO 6: η μέθοδος του αστεριού που το κάνει να πέσει
        star.____(dt)
    # TODO 7: η συνάρτηση που επιστρέφει τα αστέρια που δεν έχουν βγει από το παράθυρο
    stars = ____(stars, HEIGHT + STAR_RADIUS)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Αστέρια στη λίστα: {len(stars)}", WHITE, (20, 20))
    draw_centered_text(screen, font, "Κάνε κλικ για να ρίξεις ένα αστέρι.", GREY, (WIDTH // 2, HEIGHT - 30))
    for star in stars:
        draw_star(screen, star)
    pygame.display.flip()

pygame.quit()
