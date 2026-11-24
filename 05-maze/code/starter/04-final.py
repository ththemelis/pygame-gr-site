"""Στάδιο 4 — Το ολοκληρωμένο παιχνίδι, με ρεκόρ σε αρχείο.

Το ρεκόρ (το λιγότερο πλήθος βημάτων) αποθηκεύεται στο αρχείο record.txt και διατηρείται όταν κλείσει
το πρόγραμμα. Το αρχείο δημιουργείται μόνο του την πρώτη φορά που θα σπάσεις ρεκόρ. Οι υπόλοιπες
συναρτήσεις δίνονται έτοιμες από τα προηγούμενα στάδια.

Συμπλήρωσε τα έξι κενά (____).
"""

MAP_FILE = "maze.txt"
RECORD_FILE = "record.txt"
FLOOR = "."
WALL = "#"
START = "P"
TREASURE = "$"
PLAYER = "@"
MOVES = {"W": (0, -1), "S": (0, 1), "A": (-1, 0), "D": (1, 0)}


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
        for x in range(len(grid[y])):
            if grid[y][x] == symbol:
                return x, y
    return None


def set_cell(grid, x, y, symbol):
    """Αλλάζει το κελί (x, y). Οι συμβολοσειρές δεν αλλάζουν, άρα φτιάχνουμε νέα γραμμή."""
    grid[y] = grid[y][:x] + symbol + grid[y][x + 1:]


def draw(grid, player_x, player_y):
    """Εμφανίζει τον χάρτη, με τον παίκτη (@) στη θέση του."""
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[y])):
            if x == player_x and y == player_y:
                line += PLAYER
            else:
                line += grid[y][x]
        print(line)


def is_free(grid, x, y):
    """Επιστρέφει True αν η θέση (x, y) είναι μέσα στον χάρτη και δεν είναι τοίχος."""
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[y]):
        return False
    return grid[y][x] != WALL


def load_record(filename):
    """Επιστρέφει το ρεκόρ (ακέραιο) από το αρχείο, ή None αν δεν υπάρχει ή δεν περιέχει αριθμό."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return None
    try:
        # TODO 1: η συνάρτηση που μετατρέπει το κείμενο του αρχείου σε ακέραιο (αγνοεί κενά και αλλαγή γραμμής γύρω από τον αριθμό)
        return ____(text)
    # TODO 2: το σφάλμα που προκαλεί η int όταν το κείμενο δεν είναι αριθμός
    except ____:
        return None


def save_record(filename, steps):
    """Γράφει το ρεκόρ στο αρχείο. Ό,τι υπήρχε πριν σβήνεται."""
    # TODO 3: ο τρόπος (mode) που δημιουργεί το αρχείο, ή σβήνει ό,τι είχε και γράφει από την αρχή
    with open(filename, "____", encoding="utf-8") as file:
        # TODO 4: η μέθοδος που γράφει κείμενο στο αρχείο (ο αριθμός μετατρέπεται πρώτα σε κείμενο)
        file.____(str(steps))


def play(grid, x, y):
    """Παίζει μέχρι ο παίκτης να βρει τον θησαυρό ή να γράψει Q. Επιστρέφει τα βήματα, ή None αν τα παράτησε."""
    steps = 0
    while True:
        print()
        draw(grid, x, y)
        key = input("Κίνηση (W πάνω, S κάτω, A αριστερά, D δεξιά, Q έξοδος): ").strip().upper()
        if key == "Q":
            return None
        if key not in MOVES:
            print("Δεν ξέρω αυτό το πλήκτρο.")
            continue
        dx, dy = MOVES[key]
        new_x = x + dx
        new_y = y + dy
        if not is_free(grid, new_x, new_y):
            print("Από εκεί δεν περνάς.")
            continue
        x = new_x
        y = new_y
        steps += 1
        if grid[y][x] == TREASURE:
            print()
            draw(grid, x, y)
            return steps


def main():
    print("ΛΑΒΥΡΙΝΘΟΣ")
    print(f"Φτάσε στον θησαυρό ({TREASURE}) με όσο το δυνατόν λιγότερα βήματα.")
    print(f"Εσύ είσαι το {PLAYER}. Οι τοίχοι είναι {WALL}.")
    grid = load_map(MAP_FILE)
    if grid is None:
        print(f"Δεν βρέθηκε το αρχείο {MAP_FILE}.")
        print("Το τερματικό πρέπει να δείχνει τον φάκελο όπου βρίσκεται το αρχείο.")
        return
    start = find_symbol(grid, START)
    if start is None:
        print("Ο χάρτης δεν έχει αφετηρία (P).")
        return
    if find_symbol(grid, TREASURE) is None:
        print("Ο χάρτης δεν έχει θησαυρό ($).")
        return
    x, y = start
    set_cell(grid, x, y, FLOOR)
    record = load_record(RECORD_FILE)
    if record is None:
        print("Δεν υπάρχει ρεκόρ ακόμη.")
    else:
        print(f"Ρεκόρ: {record} βήματα.")
    steps = play(grid, x, y)
    if steps is None:
        print("Τα παράτησες.")
        return
    print(f"Βρήκες τον θησαυρό σε {steps} βήματα.")
    # TODO 5: νέο ρεκόρ είναι όταν δεν υπάρχει ρεκόρ ακόμη (record is None) Ή όταν τα βήματα είναι λιγότερα από το ρεκόρ
    if ____ or steps < record:
        # TODO 6: αποθήκευσε τα βήματα της νίκης ως νέο ρεκόρ
        save_record(RECORD_FILE, ____)
        print("Νέο ρεκόρ.")
    else:
        print(f"Το ρεκόρ παραμένει {record} βήματα.")


main()
