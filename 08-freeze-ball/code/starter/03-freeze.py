"""Στάδιο 3 — Πληκτρολόγιο, καταστάσεις και πόντοι: μία μπάλα, πέντε γύροι.

Συμπλήρωσε τα οκτώ κενά (____). Η μπάλα αναπηδά στις δύο πλευρές. Το SPACE την παγώνει και δίνει πόντους ανάλογα με
την απόσταση από το κέντρο της πράσινης ζώνης. Το επόμενο SPACE ξεκινά τον επόμενο γύρο, με μεγαλύτερη ταχύτητα.
Το ESC κλείνει το παιχνίδι.
"""
import random

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
RADIUS = 22
LANE_Y = 270
ZONE_X = WIDTH // 2
ZONE_WIDTH = 200
ROUNDS = 5
BASE_SPEED = 200           # pixel ανά δευτερόλεπτο, στον πρώτο γύρο
SPEED_STEP = 40            # αύξηση της ταχύτητας σε κάθε γύρο
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


def start_round(round_number):
    """Επιστρέφει τη θέση και την ταχύτητα της μπάλας στην αρχή ενός γύρου."""
    x = random.randint(RADIUS, WIDTH - RADIUS)
    speed = (BASE_SPEED + SPEED_STEP * (round_number - 1)) * random.choice([-1, 1])
    return x, speed


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
points = 0
state = PLAYING
ball_x, speed = start_round(round_number)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO 1: το συμβάν «πατήθηκε πλήκτρο»
        elif event.type == pygame.____:
            # TODO 2: το πλήκτρο Escape
            if event.key == pygame.____:
                running = False
            # TODO 3: το πλήκτρο του διαστήματος
            elif event.key == pygame.____:
                # TODO 4: το SPACE παγώνει την μπάλα μόνο όσο το παιχνίδι βρίσκεται σε αυτή την κατάσταση
                if state == ____:
                    points = points_for(round(abs(ball_x - ZONE_X)))
                    total += points
                    # TODO 5: η μπάλα πάγωσε και ο γύρος τελείωσε
                    state = ____
                # TODO 6: το SPACE μετά το τέλος του γύρου
                elif state == ____:
                    if round_number == ROUNDS:
                        state = GAME_OVER
                    else:
                        round_number += 1
                        ball_x, speed = start_round(round_number)
                        state = PLAYING
                else:
                    round_number = 1
                    total = 0
                    ball_x, speed = start_round(round_number)
                    state = PLAYING

    if state == PLAYING:
        ball_x += speed * dt
        # TODO 7: η bounce παίρνει τη θέση, την ταχύτητα και τα δύο όρια, και επιστρέφει νέα θέση και νέα ταχύτητα
        ball_x, speed = bounce(ball_x, ____, RADIUS, WIDTH - RADIUS)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Γύρος {round_number} / {ROUNDS}", WHITE, (20, 20))
    draw_text(screen, font, f"Πόντοι: {total}", WHITE, (WIDTH - 170, 20))

    if state == GAME_OVER:
        draw_centered_text(screen, font, "Τέλος παιχνιδιού", GREEN, (WIDTH // 2, 200))
        draw_centered_text(screen, font, f"Πόντοι: {total} από {ROUNDS * MAX_POINTS}", WHITE, (WIDTH // 2, 250))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι.", WHITE, (WIDTH // 2, 300))
    else:
        pygame.draw.rect(screen, GREEN, zone, 2)
        pygame.draw.line(screen, GREEN, (ZONE_X, zone.top), (ZONE_X, zone.bottom), 1)
        # TODO 8: κόκκινη όσο κινείται, κίτρινη όταν είναι παγωμένη
        color = ____ if state == PLAYING else YELLOW
        pygame.draw.circle(screen, color, (ball_x, LANE_Y), RADIUS)
        if state == ROUND_OVER:
            draw_centered_text(screen, font, f"+{points}", WHITE, (ball_x, LANE_Y - 50))
            draw_centered_text(screen, font, "Πάτα SPACE για να συνεχίσεις.", WHITE, (WIDTH // 2, HEIGHT - 22))

    pygame.display.flip()

pygame.quit()
