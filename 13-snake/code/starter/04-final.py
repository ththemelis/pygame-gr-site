"""Στάδιο 4 — Το Φίδι ολοκληρωμένο: ταχύτητα που μεγαλώνει, νίκη όταν γεμίσει ο πίνακας και ρεκόρ.

Συμπλήρωσε τα οκτώ κενά (____). Η λογική ενός βήματος είναι πια η συνάρτηση step, ο χρονιστής γίνεται πιο γρήγορος με τους πόντους,
και το ρεκόρ μένει όσο το παιχνίδι είναι ανοιχτό.
"""
import random

import pygame

pygame.init()

CELL = 20                  # το μέγεθος κάθε κελιού, σε pixel
COLS = 32                  # πόσα κελιά έχει κάθε γραμμή του πλέγματος
ROWS = 21                  # πόσες γραμμές έχει το πλέγμα
HUD_HEIGHT = 60
WIDTH = COLS * CELL
HEIGHT = HUD_HEIGHT + ROWS * CELL
START_INTERVAL = 160       # ο χρόνος ανάμεσα σε δύο βήματα στην αρχή, σε χιλιοστά του δευτερολέπτου
MIN_INTERVAL = 70          # ο μικρότερος χρόνος ανάμεσα σε δύο βήματα
FASTER = 5                 # πόσα χιλιοστά του δευτερολέπτου κερδίζει το φίδι για κάθε πόντο

STEP = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής για κάθε βήμα του φιδιού

PLAYING = "playing"
GAME_OVER = "game over"
WON = "won"

DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

# Τα πλήκτρα: πλήκτρο -> ενέργεια
KEY_ACTIONS = {
    pygame.K_UP: "up",
    pygame.K_w: "up",
    pygame.K_DOWN: "down",
    pygame.K_s: "down",
    pygame.K_LEFT: "left",
    pygame.K_a: "left",
    pygame.K_RIGHT: "right",
    pygame.K_d: "right",
    pygame.K_SPACE: "restart",
    pygame.K_ESCAPE: "quit",
}

DARK = (20, 30, 28)
LIGHT = (30, 46, 42)
BODY_COLOR = (90, 200, 120)
HEAD_COLOR = (170, 245, 190)
FOOD_COLOR = (230, 70, 70)
HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 70)
RED = (220, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Φίδι")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Το πλαίσιο του τέλους του παιχνιδιού
PANEL = pygame.Rect(120, 160, 400, 220)


def next_cell(cell, direction):
    """Το κελί που βρίσκεται ένα βήμα από το cell προς την κατεύθυνση direction."""
    return cell[0] + direction[0], cell[1] + direction[1]


def turn(direction, wanted):
    """Η νέα κατεύθυνση: η wanted, εκτός αν είναι ακριβώς αντίθετη από την direction (το φίδι δεν γυρίζει πίσω)."""
    if wanted == (-direction[0], -direction[1]):
        return direction
    return wanted


def move_snake(snake, direction, grow):
    """Το φίδι μετά από ένα βήμα: ένα νέο κεφάλι μπροστά και, αν δεν μεγαλώνει, χωρίς το τελευταίο κελί. Επιστρέφει νέα λίστα."""
    new_head = next_cell(snake[0], direction)
    if grow:
        return [new_head] + snake
    return [new_head] + snake[:-1]


def place_food(snake, cols, rows):
    """Ένα τυχαίο ελεύθερο κελί του πλέγματος για την τροφή, ή None αν δεν υπάρχει κανένα ελεύθερο κελί."""
    free = []
    for row in range(rows):
        for col in range(cols):
            if (col, row) not in snake:
                free.append((col, row))
    if len(free) == 0:
        return None
    return random.choice(free)


def is_dead(snake, cols, rows):
    """True αν το κεφάλι του φιδιού είναι έξω από το πλέγμα ή πάνω στο σώμα του."""
    col, row = snake[0]
    if col < 0 or col >= cols or row < 0 or row >= rows:
        return True
    return snake[0] in snake[1:]


def step(snake, direction, food, cols, rows):
    """Ένα βήμα του φιδιού. Επιστρέφει την τριάδα (νέο φίδι, έφαγε, πέθανε).

    Αν το νέο κεφάλι πέφτει στην τροφή, το φίδι μεγαλώνει. Αν χτυπήσει, μένει όπως ήταν."""
    ate = next_cell(snake[0], direction) == food
    new_snake = move_snake(snake, direction, ate)
    if is_dead(new_snake, cols, rows):
        # TODO 1: αν το φίδι χτυπήσει, μένει όπως ήταν
        return ____, False, True
    return new_snake, ate, False


def step_interval(score):
    """Ο χρόνος ανάμεσα σε δύο βήματα, σε χιλιοστά του δευτερολέπτου: μικραίνει με τους πόντους, αλλά όχι κάτω από το MIN_INTERVAL."""
    # TODO 2: ο χρόνος ανάμεσα στα βήματα δεν πέφτει ποτέ κάτω από το MIN_INTERVAL
    return ____(MIN_INTERVAL, START_INTERVAL - FASTER * score)


def new_game():
    """Τα στοιχεία ενός νέου παιχνιδιού: το φίδι (τρία κελιά, κεφάλι στα δεξιά), η κατεύθυνσή του και η πρώτη τροφή."""
    snake = [(16, 10), (15, 10), (14, 10)]
    return snake, (1, 0), place_food(snake, COLS, ROWS)


def cell_rect(cell):
    """Το ορθογώνιο, σε pixel, ενός κελιού του πλέγματος."""
    col, row = cell
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)


def handle_events():
    """Διαβάζει όλα τα συμβάντα του καρέ και επιστρέφει τη λίστα των ενεργειών που ζητήθηκαν, με τη σειρά τους."""
    actions = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions.append("quit")
        elif event.type == STEP:
            actions.append("step")
        elif event.type == pygame.KEYDOWN:
            action = KEY_ACTIONS.get(event.key)
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


def draw_board(surface):
    """Ζωγραφίζει το πλέγμα: τα κελιά εναλλάσσονται σε ανοιχτό και σκούρο χρώμα, σαν σκακιέρα."""
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT if (col + row) % 2 == 0 else DARK
            pygame.draw.rect(surface, color, cell_rect((col, row)))


def draw_food(surface, food):
    """Ζωγραφίζει την τροφή: έναν κύκλο στο κέντρο του κελιού της."""
    pygame.draw.circle(surface, FOOD_COLOR, cell_rect(food).center, CELL // 2 - 3)


def draw_snake(surface, snake):
    """Ζωγραφίζει το φίδι: κάθε κελί του ως τετράγωνο λίγο μικρότερο από το κελί, και το κεφάλι (το πρώτο κελί) με άλλο χρώμα."""
    for index in range(len(snake)):
        color = HEAD_COLOR if index == 0 else BODY_COLOR
        pygame.draw.rect(surface, color, cell_rect(snake[index]).inflate(-2, -2))


def draw_hud(surface, font, score, record):
    """Ζωγραφίζει την περιοχή των ενδείξεων: οι πόντοι, το ρεκόρ και μια υπόδειξη για τα πλήκτρα."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(surface, font, f"Πόντοι: {score}", YELLOW, (20, 20))
    # TODO 3: ζωγράφισε στο HUD, στο (200, 20), το κείμενο «Ρεκόρ: …» με άσπρο χρώμα (μία γραμμή)
    ____
    draw_text(surface, font, "Βέλη ή WASD", GREY, (430, 20))


snake, direction, food = new_game()
next_direction = direction
score = 0
best = 0
new_record = False
state = PLAYING
interval = step_interval(score)
pygame.time.set_timer(STEP, interval)

running = True
while running:
    clock.tick(60)

    for action in handle_events():
        if action == "quit":
            running = False
        elif action == "step" and state == PLAYING:
            direction = next_direction
            # TODO 4: η συνάρτηση που κάνει ένα ολόκληρο βήμα
            snake, ate, dead = ____(snake, direction, food, COLS, ROWS)
            if ate:
                score += 1
                food = place_food(snake, COLS, ROWS)
            if dead:
                state = GAME_OVER
            # TODO 5: δεν υπάρχει ελεύθερο κελί για νέα τροφή: ο πίνακας γέμισε
            elif food is ____:
                state = WON
            if state == PLAYING:
                # Όσο αυξάνονται οι πόντοι, τα βήματα γίνονται πιο γρήγορα
                # TODO 6: ο νέος χρόνος ανάμεσα στα βήματα, για τους πόντους που έχεις τώρα
                new_interval = ____(score)
                # TODO 7: ο χρονιστής ξαναρυθμίζεται μόνο όταν ο χρόνος αλλάζει
                if new_interval ____ interval:
                    interval = new_interval
                    pygame.time.set_timer(STEP, interval)
            else:
                pygame.time.set_timer(STEP, 0)
                # TODO 8: νέο ρεκόρ έχουμε μόνο όταν οι πόντοι είναι περισσότεροι
                new_record = score ____ best
                best = max(best, score)
        elif action in DIRECTIONS and state == PLAYING:
            next_direction = turn(direction, DIRECTIONS[action])
        elif action == "restart" and state != PLAYING:
            snake, direction, food = new_game()
            next_direction = direction
            score = 0
            state = PLAYING
            interval = step_interval(score)
            pygame.time.set_timer(STEP, interval)

    draw_board(screen)
    if food is not None:
        draw_food(screen, food)
    draw_snake(screen, snake)
    draw_hud(screen, font, score, best)
    if state != PLAYING:
        pygame.draw.rect(screen, HUD_COLOR, PANEL)
        pygame.draw.rect(screen, GREY, PANEL, 2)
        if state == WON:
            draw_centered_text(screen, font, "Κέρδισες", YELLOW, (WIDTH // 2, 200))
        else:
            draw_centered_text(screen, font, "Τέλος παιχνιδιού", RED, (WIDTH // 2, 200))
        draw_centered_text(screen, font, f"Πόντοι: {score}", WHITE, (WIDTH // 2, 245))
        if new_record:
            draw_centered_text(screen, font, f"Νέο ρεκόρ: {score}", YELLOW, (WIDTH // 2, 285))
        else:
            draw_centered_text(screen, font, f"Ρεκόρ: {best}", GREY, (WIDTH // 2, 285))
        draw_centered_text(screen, font, "SPACE: ξανά · ESC: έξοδος", GREY, (WIDTH // 2, 335))
    pygame.display.flip()

pygame.quit()
