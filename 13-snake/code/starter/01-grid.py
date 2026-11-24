"""Στάδιο 1 — Το πλέγμα και το φίδι: κελιά, κατεύθυνση, χρονιστής και πλήκτρα.

Συμπλήρωσε τα οκτώ κενά (____). Το φίδι είναι μια λίστα κελιών (col, row) με το κεφάλι πρώτο. Τον ρυθμό τον δίνει ο χρονιστής: σε κάθε
βήμα το φίδι κινείται, και τα πλήκτρα αλλάζουν μόνο την κατεύθυνση του επόμενου βήματος. Στο Στάδιο 1 το φίδι δεν σταματά στους τοίχους.
"""
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

# TODO 1: προς τα αριστερά η στήλη (col) μικραίνει κατά 1
DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (____, 0), "right": (1, 0)}

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
HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)

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
    # TODO 2: όλα τα κελιά εκτός από το τελευταίο
    return [new_head] + snake[:____]


def cell_rect(cell):
    """Το ορθογώνιο, σε pixel, ενός κελιού του πλέγματος."""
    col, row = cell
    # TODO 3: το y ενός κελιού: η γραμμή επί το μέγεθος του κελιού, κάτω από το HUD
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * ____, CELL, CELL)


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
            # TODO 4: τα κελιά εναλλάσσονται: το υπόλοιπο της διαίρεσης του col + row με αυτό τον αριθμό είναι 0 ή 1
            color = LIGHT if (col + row) % ____ == 0 else DARK
            pygame.draw.rect(surface, color, cell_rect((col, row)))


def draw_snake(surface, snake):
    """Ζωγραφίζει το φίδι: κάθε κελί του ως τετράγωνο λίγο μικρότερο από το κελί, και το κεφάλι (το πρώτο κελί) με άλλο χρώμα."""
    for index in range(len(snake)):
        # TODO 5: το κεφάλι είναι το πρώτο κελί της λίστας
        color = HEAD_COLOR if index == ____ else BODY_COLOR
        pygame.draw.rect(surface, color, cell_rect(snake[index]).inflate(-2, -2))


def draw_hud(surface, font):
    """Ζωγραφίζει την περιοχή των ενδείξεων: μια υπόδειξη για τα πλήκτρα."""
    pygame.draw.rect(surface, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(surface, font, "Βέλη ή WASD", GREY, (430, 20))


snake = [(16, 10), (15, 10), (14, 10)]
direction = (1, 0)
next_direction = direction
# TODO 6: το συμβάν που θα στέλνει ο χρονιστής σε κάθε βήμα
pygame.time.set_timer(____, START_INTERVAL)

running = True
while running:
    clock.tick(60)

    for action in handle_events():
        if action == "quit":
            running = False
        elif action == "step":
            # TODO 7: το βήμα γίνεται με την κατεύθυνση που ζήτησαν τα πλήκτρα (μία γραμμή)
            ____
            snake = move_snake(snake, direction, False)
        elif action in DIRECTIONS:
            # TODO 8: η κατεύθυνση του τελευταίου βήματος, με την οποία συγκρίνεται το νέο πλήκτρο
            next_direction = turn(____, DIRECTIONS[action])

    draw_board(screen)
    draw_snake(screen, snake)
    draw_hud(screen, font)
    pygame.display.flip()

pygame.quit()
