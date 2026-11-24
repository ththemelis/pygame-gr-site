"""Στάδιο 2 — Τροφή και ανάπτυξη: το φίδι τρώει, μεγαλώνει και μετρά πόντους.

Συμπλήρωσε τα οκτώ κενά (____). Η τροφή μπαίνει σε ένα τυχαίο ελεύθερο κελί. Όταν το νέο κεφάλι πέφτει πάνω της, το φίδι δεν χάνει
την ουρά του και μεγαλώνει κατά ένα κελί. Στο Στάδιο 2 το φίδι ακόμη δεν σταματά στους τοίχους.
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
    pygame.K_ESCAPE: "quit",
}

DARK = (20, 30, 28)
LIGHT = (30, 46, 42)
BODY_COLOR = (90, 200, 120)
HEAD_COLOR = (170, 245, 190)
FOOD_COLOR = (230, 70, 70)
HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
YELLOW = (255, 210, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Φίδι")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


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
            # TODO 1: το κελί είναι ελεύθερο όταν δεν ανήκει στο φίδι
            if (col, row) ____ snake:
                # TODO 2: πρόσθεσε το ελεύθερο κελί στο τέλος της λίστας
                free.____((col, row))
    if len(free) == 0:
        return None
    return random.choice(free)


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


def draw_board(surface):
    """Ζωγραφίζει το πλέγμα: τα κελιά εναλλάσσονται σε ανοιχτό και σκούρο χρώμα, σαν σκακιέρα."""
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT if (col + row) % 2 == 0 else DARK
            pygame.draw.rect(surface, color, cell_rect((col, row)))


def draw_food(surface, food):
    """Ζωγραφίζει την τροφή: έναν κύκλο στο κέντρο του κελιού της."""
    # TODO 3: η τροφή ζωγραφίζεται στο κέντρο του κελιού της
    pygame.draw.circle(surface, FOOD_COLOR, cell_rect(food).____, CELL // 2 - 3)


def draw_snake(surface, snake):
    """Ζωγραφίζει το φίδι: κάθε κελί του ως τετράγωνο λίγο μικρότερο από το κελί, και το κεφάλι (το πρώτο κελί) με άλλο χρώμα."""
    for index in range(len(snake)):
        color = HEAD_COLOR if index == 0 else BODY_COLOR
        pygame.draw.rect(surface, color, cell_rect(snake[index]).inflate(-2, -2))


def draw_hud(surface, font, score):
    """Ζωγραφίζει την περιοχή των ενδείξεων: οι πόντοι και μια υπόδειξη για τα πλήκτρα."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    # TODO 4: ζωγράφισε στο HUD, στο (20, 20), το κείμενο «Πόντοι: …» με κίτρινο χρώμα (μία γραμμή)
    ____
    draw_text(surface, font, "Βέλη ή WASD", GREY, (430, 20))


snake = [(16, 10), (15, 10), (14, 10)]
direction = (1, 0)
next_direction = direction
food = place_food(snake, COLS, ROWS)
score = 0
pygame.time.set_timer(STEP, START_INTERVAL)

running = True
while running:
    clock.tick(60)

    for action in handle_events():
        if action == "quit":
            running = False
        elif action == "step":
            direction = next_direction
            # TODO 5: το φίδι τρώει όταν το νέο κεφάλι είναι στο ίδιο κελί με την τροφή
            eating = next_cell(snake[0], direction) ____ food
            # TODO 6: το φίδι μεγαλώνει όταν τρώει
            snake = move_snake(snake, direction, ____)
            # TODO 7: ό,τι ακολουθεί γίνεται μόνο όταν το φίδι έφαγε
            if ____:
                score += 1
                # TODO 8: βάλε νέα τροφή σε ένα ελεύθερο κελί (μία γραμμή)
                ____
        elif action in DIRECTIONS:
            next_direction = turn(direction, DIRECTIONS[action])

    draw_board(screen)
    draw_food(screen, food)
    draw_snake(screen, snake)
    draw_hud(screen, font, score)
    pygame.display.flip()

pygame.quit()
