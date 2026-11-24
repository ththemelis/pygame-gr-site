"""Στάδιο 2 — Πλέγμα, αναζήτηση συμβόλου και σχεδίαση.

Ο χάρτης είναι μια λίστα από συμβολοσειρές: το grid[y][x] είναι το κελί στη γραμμή y και τη στήλη x.
Η find_symbol ψάχνει ένα σύμβολο, η set_cell αλλάζει ένα κελί και η draw εμφανίζει τον χάρτη με τον
παίκτη (@) στη θέση του. Η load_map δίνεται έτοιμη από το Στάδιο 1.

Συμπλήρωσε τα επτά κενά (____).
"""

MAP_FILE = "maze.txt"
FLOOR = "."
START = "P"
PLAYER = "@"


def load_map(filename):
    """Διαβάζει το αρχείο χάρτη. Επιστρέφει λίστα γραμμών, ή None αν το αρχείο δεν υπάρχει."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return None
    return text.splitlines()


def find_symbol(grid, symbol):
    """Επιστρέφει τη θέση (x, y) του πρώτου κελιού με αυτό το σύμβολο, ή None αν δεν υπάρχει."""
    for y in range(len(grid)):
        # TODO 1: οι στήλες της γραμμής y είναι τόσες όσο το μήκος της γραμμής grid[y]
        for x in range(len(grid[____])):
            # TODO 2: πρώτα η γραμμή (y), μετά η στήλη (x)
            if grid[y][____] == symbol:
                # TODO 3: επίστρεψε τη θέση ως πλειάδα (x, y)
                return ____
    return None


def set_cell(grid, x, y, symbol):
    """Αλλάζει το κελί (x, y). Οι συμβολοσειρές δεν αλλάζουν, άρα φτιάχνουμε νέα γραμμή."""
    # TODO 4: η νέα γραμμή = ό,τι υπάρχει πριν από το x + το νέο σύμβολο + ό,τι υπάρχει ΜΕΤΑ το x
    grid[y] = grid[y][:x] + symbol + grid[y][____:]


def draw(grid, player_x, player_y):
    """Εμφανίζει τον χάρτη, με τον παίκτη (@) στη θέση του."""
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[y])):
            # TODO 5: ο παίκτης εμφανίζεται εκεί που το x είναι player_x ΚΑΙ το y είναι player_y
            if x == player_x and y == ____:
                line += PLAYER
            else:
                line += grid[y][x]
        print(line)


def main():
    grid = load_map(MAP_FILE)
    if grid is None:
        print(f"Δεν βρέθηκε το αρχείο {MAP_FILE}.")
        return
    start = find_symbol(grid, START)
    if start is None:
        print("Ο χάρτης δεν έχει αφετηρία (P).")
        return
    # TODO 6: αποσυσκεύασε την πλειάδα start σε δύο μεταβλητές, x και y
    x, y = ____
    # TODO 7: το κελί της αφετηρίας γίνεται κανονικός διάδρομος (σταθερά FLOOR)
    set_cell(grid, x, y, ____)
    print(f"Αφετηρία: στήλη {x}, γραμμή {y}")
    draw(grid, x, y)
    print()
    print("Ο ίδιος χάρτης, με τον παίκτη δύο γραμμές πιο κάτω:")
    draw(grid, x, y + 2)


main()
