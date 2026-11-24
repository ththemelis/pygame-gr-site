"""Στάδιο 3 — Συγκρούσεις και τέλος: ο τοίχος, το σώμα, το τέλος του παιχνιδιού και το νέο παιχνίδι.

Συμπλήρωσε τα οκτώ κενά (____). Πρώτα φτιάχνεται το φίδι μετά την κίνηση και μετά ελέγχεται: αν χτυπήσει, το παιχνίδι τελειώνει και
το φίδι μένει όπως ήταν. Το SPACE ξεκινά νέο παιχνίδι.
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
START_INTERVAL = 160       # ο χρόνος ανάμεσα σε δύο βήματα του φιδιού, σε χιλιοστά του δευτερολέπτου

STEP = pygame.USEREVENT + 1      # το συμβάν που στέλνει ο χρονιστής για κάθε βήμα του φιδιού

PLAYING = "playing"
GAME_OVER = "game over"

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
    # TODO 1: η τελευταία στήλη έχει δείκτη cols - 1, άρα το col είναι έξω όταν φτάσει το πλήθος των στηλών
    if col < 0 or col >= ____ or row < 0 or row >= rows:
        return True
    # TODO 2: όλα τα κελιά εκτός από το κεφάλι
    return snake[0] in snake[____:]


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


def draw_hud(surface, font, score):
    """Ζωγραφίζει την περιοχή των ενδείξεων: οι πόντοι και μια υπόδειξη για τα πλήκτρα."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(surface, font, f"Πόντοι: {score}", YELLOW, (20, 20))
    draw_text(surface, font, "Βέλη ή WASD", GREY, (430, 20))


snake, direction, food = new_game()
next_direction = direction
score = 0
state = PLAYING
pygame.time.set_timer(STEP, START_INTERVAL)

running = True
while running:
    clock.tick(60)

    for action in handle_events():
        if action == "quit":
            running = False
        elif action == "step" and state == PLAYING:
            direction = next_direction
            eating = next_cell(snake[0], direction) == food
            # TODO 3: φτιάξε το φίδι μετά την κίνηση, χωρίς να αλλάξεις ακόμη το snake (μία γραμμή)
            ____
            # TODO 4: ελέγχουμε το φίδι μετά την κίνηση
            if is_dead(____, COLS, ROWS):
                # TODO 5: το παιχνίδι τελειώνει
                state = ____
                # TODO 6: με αυτό τον αριθμό ο χρονιστής σταματά
                pygame.time.set_timer(STEP, ____)
            else:
                # TODO 7: το φίδι γίνεται το νέο φίδι (μία γραμμή)
                ____
                if eating:
                    score += 1
                    food = place_food(snake, COLS, ROWS)
        elif action in DIRECTIONS and state == PLAYING:
            next_direction = turn(direction, DIRECTIONS[action])
        elif action == "restart" and state == GAME_OVER:
            # TODO 8: ξεκίνα νέο παιχνίδι: φίδι, κατεύθυνση και τροφή (μία γραμμή)
            ____
            next_direction = direction
            score = 0
            state = PLAYING
            pygame.time.set_timer(STEP, START_INTERVAL)

    draw_board(screen)
    draw_food(screen, food)
    draw_snake(screen, snake)
    draw_hud(screen, font, score)
    if state == GAME_OVER:
        pygame.draw.rect(screen, HUD_COLOR, PANEL)
        pygame.draw.rect(screen, GREY, PANEL, 2)
        draw_centered_text(screen, font, "Τέλος παιχνιδιού", RED, (WIDTH // 2, 200))
        draw_centered_text(screen, font, f"Πόντοι: {score}", WHITE, (WIDTH // 2, 245))
        draw_centered_text(screen, font, "SPACE: ξανά · ESC: έξοδος", GREY, (WIDTH // 2, 335))
    pygame.display.flip()

pygame.quit()
