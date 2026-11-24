"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 7.

Τρέξε:  python check_exercises.py

Ελέγχει τις συναρτήσεις του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import sys
from unittest import mock

try:
    import exercises
except ImportError:
    print("Δεν βρέθηκε το exercises.py. Βάλ' το στον ίδιο φάκελο με αυτό το αρχείο.")
    sys.exit(1)

results = []


def run_check(description, function, argument, expected):
    """Καλεί τη function με το argument και συγκρίνει το αποτέλεσμα με το expected."""
    try:
        got = function(argument)
    except NotImplementedError:
        results.append("pending")
        print(f"  [ΔΕΝ ΕΙΝΑΙ ΕΤΟΙΜΗ ΑΚΟΜΗ] {description}")
        return
    except Exception as error:
        results.append("failed")
        print(f"  [ΛΑΘΟΣ] {description}")
        print(f"      Προκλήθηκε σφάλμα {type(error).__name__}: {error}")
        return
    if got == expected:
        results.append("passed")
        print(f"  [ΟΚ] {description}")
    else:
        results.append("failed")
        print(f"  [ΛΑΘΟΣ] {description}")
        print(f"      αναμενόμενο: {expected!r}")
        print(f"      πήρα:        {got!r}")


# ---- Άσκηση 1: brighter

def call_brighter(arguments):
    color, amount = arguments
    return exercises.brighter(color, amount)


def brighter_type(arguments):
    """Ο τύπος του αποτελέσματος: το χρώμα είναι πλειάδα, όπως αυτά που δέχεται η pygame."""
    return type(call_brighter(arguments)).__name__


# ---- Άσκηση 2: inside_rect

def call_inside_rect(arguments):
    x, y, left, top, width, height = arguments
    return exercises.inside_rect(x, y, left, top, width, height)


# ---- Άσκηση 3: random_position

def positions_with(arguments):
    """Καλεί τη random_position με «τυχαίο» αριθμό που είναι πάντα ο μεγαλύτερος ή ο μικρότερος δυνατός.

    Επιστρέφει τη θέση που βγήκε. Έτσι ελέγχουμε τα όρια χωρίς να εξαρτάται το αποτέλεσμα από την τύχη.
    """
    choice, args = arguments

    def fake_randint(low, high):
        if choice == "μεγαλύτερο":
            return high
        return low

    with mock.patch("random.randint", side_effect=fake_randint):
        return exercises.random_position(*args)


def limits_asked(args):
    """Τα (από, μέχρι) που ζήτησε η random_position από τη random.randint, ταξινομημένα."""
    calls = []

    def recording_randint(low, high):
        calls.append((low, high))
        return low

    with mock.patch("random.randint", side_effect=recording_randint):
        exercises.random_position(*args)
    return sorted(calls)


def many_positions(args):
    """200 πραγματικές κλήσεις: όλες μέσα στα όρια, ακέραιοι αριθμοί, και όχι πάντα η ίδια θέση."""
    width, height, size, top = args
    positions = []
    for repeat in range(200):
        positions.append(exercises.random_position(width, height, size, top))
    inside = True
    for x, y in positions:
        if not (isinstance(x, int) and isinstance(y, int)):
            inside = False
        elif not (0 <= x <= width - size and top <= y <= height - size):
            inside = False
    different = len(set(positions)) > 1
    return inside, different


# ---- Άσκηση 4: accuracy

def call_accuracy(arguments):
    hits, misses = arguments
    return round(exercises.accuracy(hits, misses), 6)


print("Άσκηση 1 (κύκλος 1): brighter")
for arguments, expected in (
        (((200, 50, 20), 60), (255, 110, 80)),
        (((0, 0, 0), 30), (30, 30, 30)),
        (((10, 20, 30), 0), (10, 20, 30)),
        (((254, 0, 100), 1), (255, 1, 101)),
        (((250, 250, 250), 10), (255, 255, 255)),
        (((255, 255, 255), 5), (255, 255, 255)),
):
    run_check(f"brighter{arguments} -> {expected}", call_brighter, arguments, expected)
run_check("το αποτέλεσμα της brighter είναι πλειάδα", brighter_type, ((1, 2, 3), 1), "tuple")

print("Άσκηση 2 (κύκλος 2): inside_rect")
for arguments, expected in (
        ((5, 5, 0, 0, 10, 10), True),
        ((0, 5, 0, 0, 10, 10), True),
        ((5, 0, 0, 0, 10, 10), True),
        ((9, 9, 0, 0, 10, 10), True),
        ((10, 5, 0, 0, 10, 10), False),
        ((5, 10, 0, 0, 10, 10), False),
        ((-1, 5, 0, 0, 10, 10), False),
        ((5, -1, 0, 0, 10, 10), False),
        ((150, 120, 100, 100, 80, 60), True),
        ((180, 120, 100, 100, 80, 60), False),
        ((99, 120, 100, 100, 80, 60), False),
        ((0, 0, 0, 0, 0, 0), False),
):
    run_check(f"inside_rect{arguments} -> {expected}", call_inside_rect, arguments, expected)

print("Άσκηση 3 (κύκλος 3): random_position")
run_check("μεγαλύτερα δυνατά x και y για (640, 480, 80)", positions_with, ("μεγαλύτερο", (640, 480, 80)), (560, 400))
run_check("μικρότερα δυνατά x και y για (640, 480, 80)", positions_with, ("μικρότερο", (640, 480, 80)), (0, 0))
run_check("μεγαλύτερα δυνατά με top = 60", positions_with, ("μεγαλύτερο", (640, 480, 80, 60)), (560, 400))
run_check("μικρότερα δυνατά με top = 60 (το y ξεκινά από το top)", positions_with, ("μικρότερο", (640, 480, 80, 60)), (0, 60))
run_check("τα όρια που ζητά από τη random.randint για (640, 480, 80, 60)", limits_asked, (640, 480, 80, 60),
          [(0, 560), (60, 400)])
run_check("τα όρια που ζητά από τη random.randint για (100, 100, 10)", limits_asked, (100, 100, 10), [(0, 90), (0, 90)])
run_check("200 πραγματικές θέσεις: μέσα στα όρια και ακέραιες, όχι πάντα ίδιες", many_positions, (640, 480, 80, 60),
          (True, True))

print("Άσκηση 4 (κύκλος 4): accuracy")
for arguments, expected in (
        ((5, 0), 100.0),
        ((5, 5), 50.0),
        ((0, 5), 0.0),
        ((0, 0), 0),
        ((3, 1), 75.0),
        ((7, 3), 70.0),
        ((1, 2), 33.333333),
):
    run_check(f"accuracy{arguments} -> {expected}", call_accuracy, arguments, expected)

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
