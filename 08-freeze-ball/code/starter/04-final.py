"""Στάδιο 4 — Το ολοκληρωμένο παιχνίδι: τρεις μπάλες σε τρεις λωρίδες, πέντε γύροι.

Συμπλήρωσε τα οκτώ κενά (____). Κάθε μπάλα είναι ένα λεξικό και οι τρεις μπάλες μπαίνουν σε μια λίστα. Σε κάθε
γύρο το SPACE παγώνει την πρώτη μπάλα που ακόμη κινείται. Ο γύρος τελειώνει όταν παγώσουν και οι τρεις.
"""
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
RADIUS = 22
LANES = (130, 270, 410)
BASE_SPEEDS = (180, 240, 300)    # pixel ανά δευτερόλεπτο, στον πρώτο γύρο
SPEED_STEP = 30                  # αύξηση της ταχύτητας σε κάθε γύρο
ZONE_X = WIDTH // 2
ZONE_WIDTH = 200
ROUNDS = 5
MAX_POINTS = 10
MAX_DT = 0.05

PLAYING = "playing"
ROUND_OVER = "round_over"
GAME_OVER = "game_over"

BACKGROUND = (25, 35, 60)
RED = (220, 60, 60)
YELLOW = (255, 210, 70)
GREEN = (90, 220, 150)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Πάγωσε την μπάλα")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
zone = pygame.Rect(ZONE_X - ZONE_WIDTH // 2, HUD_HEIGHT + 10, ZONE_WIDTH, HEIGHT - HUD_HEIGHT - 50)


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def make_balls(round_number):
    """Φτιάχνει τις τρεις μπάλες ενός γύρου, μία σε κάθε λωρίδα. Η ταχύτητα μεγαλώνει σε κάθε γύρο."""
    balls = []
    for index in range(len(LANES)):
        speed = BASE_SPEEDS[index] + SPEED_STEP * (round_number - 1)
        # TODO 1: η μέθοδος της λίστας που προσθέτει στοιχείο στο τέλος
        balls.____({
            # TODO 2: τυχαία αρχική θέση x, ώστε η μπάλα να χωρά ολόκληρη μέσα στο παράθυρο
            "x": random.____(RADIUS, WIDTH - RADIUS),
            "y": LANES[index],
            "speed": speed * random.choice([-1, 1]),
            "frozen": False,
            "points": 0,
        })
    return balls


def bounce(position, speed, low, high):
    """Αν η θέση βγήκε από τα όρια, την επαναφέρει στο όριο και αντιστρέφει την ταχύτητα. Επιστρέφει (θέση, ταχύτητα)."""
    if position < low:
        return low, -speed
    if position > high:
        return high, -speed
    return position, speed


def points_for(distance):
    """Οι πόντοι ενός πάγωματος: 10 στο κέντρο, ένας λιγότερος για κάθε 10 pixel απόσταση, ποτέ κάτω από 0."""
    return max(0, MAX_POINTS - distance // 10)


round_number = 1
total = 0
state = PLAYING
balls = make_balls(round_number)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if state == PLAYING:
                    # Παγώνει την πρώτη μπάλα που ακόμη κινείται
                    for ball in balls:
                        if not ball["frozen"]:
                            # TODO 3: η μπάλα πάγωσε
                            ball["frozen"] = ____
                            # TODO 4: η απόσταση είναι από το κέντρο της ζώνης
                            ball["points"] = points_for(round(abs(ball["x"] - ____)))
                            total += ball["points"]
                            # TODO 5: μόνο η πρώτη μπάλα παγώνει, οπότε ο βρόχος διακόπτεται εδώ
                            ____
                    # Μετρά πόσες μπάλες κινούνται ακόμη. Αν καμία, ο γύρος τελείωσε.
                    moving = 0
                    for ball in balls:
                        if not ball["frozen"]:
                            moving += 1
                    # TODO 6: καμία μπάλα δεν κινείται
                    if moving ____ 0:
                        state = ROUND_OVER
                elif state == ROUND_OVER:
                    if round_number == ROUNDS:
                        state = GAME_OVER
                    else:
                        round_number += 1
                        balls = make_balls(round_number)
                        state = PLAYING
                else:
                    round_number = 1
                    total = 0
                    balls = make_balls(round_number)
                    state = PLAYING

    if state == PLAYING:
        for ball in balls:
            if not ball["frozen"]:
                ball["x"] += ball["speed"] * dt
                # TODO 7: ίδια ιδέα με το Στάδιο 3, αλλά με τα στοιχεία του λεξικού της μπάλας
                ____

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Γύρος {round_number} / {ROUNDS}", WHITE, (20, 20))
    draw_text(screen, font, f"Πόντοι: {total}", WHITE, (WIDTH - 170, 20))

    if state == GAME_OVER:
        draw_centered_text(screen, font, "Τέλος παιχνιδιού", GREEN, (WIDTH // 2, 200))
        draw_centered_text(screen, font, f"Πόντοι: {total} από {ROUNDS * MAX_POINTS * len(LANES)}", WHITE, (WIDTH // 2, 250))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι.", WHITE, (WIDTH // 2, 300))
    else:
        pygame.draw.rect(screen, GREEN, zone, 2)
        pygame.draw.line(screen, GREEN, (ZONE_X, zone.top), (ZONE_X, zone.bottom), 1)
        for ball in balls:
            # TODO 8: κίτρινη αν η μπάλα είναι παγωμένη, αλλιώς κόκκινη
            color = YELLOW if ball[____] else RED
            pygame.draw.circle(screen, color, (ball["x"], ball["y"]), RADIUS)
            if ball["frozen"]:
                draw_centered_text(screen, font, f"+{ball['points']}", WHITE, (ball["x"], ball["y"] - 40))
        if state == ROUND_OVER:
            draw_centered_text(screen, font, "Πάτα SPACE για να συνεχίσεις.", WHITE, (WIDTH // 2, HEIGHT - 22))

    pygame.display.flip()

pygame.quit()
