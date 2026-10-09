"""Στάδιο 1 — Εικόνες: φόντο και διαστημόπλοιο που ακολουθεί το ποντίκι.

Συμπλήρωσε τα οκτώ κενά (____). Οι εικόνες φορτώνονται μία φορά, πριν από τον βρόχο. Κάθε φορά που κινείται το ποντίκι, το
κέντρο του διαστημόπλοιου πηγαίνει εκεί, μέσα στα όρια της περιοχής παιχνιδιού. Πρώτα τρέξε το make_assets.py, για να
φτιαχτεί ο φάκελος assets.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
SHIP_WIDTH = 64            # το πλάτος του διαστημόπλοιου στην οθόνη, σε pixel

HUD_COLOR = (12, 18, 36)
GREY = (120, 130, 150)
WHITE = (245, 245, 245)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Διαστημική αποφυγή")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Η περιοχή όπου κινείται το διαστημόπλοιο: όλο το παράθυρο κάτω από το HUD
PLAY_AREA = pygame.Rect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT)


def fit_size(width, height, new_width):
    """Το μέγεθος (πλάτος, ύψος) μιας εικόνας με πλάτος new_width, όταν διατηρεί τις αναλογίες της."""
    # TODO 1: το ύψος αλλάζει με τον ίδιο λόγο που αλλάζει το πλάτος: νέο πλάτος προς παλιό
    return new_width, round(height * ____ / width)


def load_image(path):
    """Φορτώνει μια εικόνα με διαφάνεια από το αρχείο path, έτοιμη για γρήγορη σχεδίαση."""
    # TODO 2: η μέθοδος που προσαρμόζει στην οθόνη μια εικόνα με διαφάνεια
    return pygame.image.load(path).____()


def resize(image, new_width):
    """Επιστρέφει νέα εικόνα με πλάτος new_width, χωρίς να παραμορφώνεται. Η αρχική εικόνα δεν αλλάζει."""
    size = fit_size(image.get_width(), image.get_height(), new_width)
    # TODO 3: η συνάρτηση που φτιάχνει νέα εικόνα με άλλο μέγεθος
    return pygame.transform.____(image, size)


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


# Οι εικόνες φορτώνονται μία φορά, πριν από τον βρόχο
background = pygame.image.load("assets/background.png").convert()
ship_image = resize(load_image("assets/ship.png"), SHIP_WIDTH)
# TODO 4: η μέθοδος που δίνει το ορθογώνιο μιας εικόνας
ship_rect = ship_image.____(center=(WIDTH // 2, HEIGHT - 70))

pygame.mouse.set_visible(False)       # το διαστημόπλοιο παίρνει τη θέση του δείκτη

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # TODO 5: το συμβάν που έρχεται όταν κινείται το ποντίκι
        elif event.type == pygame.____:
            # TODO 6: η θέση του ποντικιού, όπως στο κλικ του Μαθήματος 7
            ship_rect.center = event.____
            # TODO 7: κράτα το ορθογώνιο μέσα στην PLAY_AREA (μία γραμμή)
            ____

    screen.blit(background, (0, 0))
    # TODO 8: ζωγράφισε το διαστημόπλοιο στη θέση του ορθογωνίου του (μία γραμμή)
    ____
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Κέντρο: {ship_rect.center}", WHITE, (20, 20))
    draw_text(screen, font, f"Μέγεθος: {ship_rect.size}", WHITE, (WIDTH - 250, 20))
    pygame.display.flip()

pygame.quit()
