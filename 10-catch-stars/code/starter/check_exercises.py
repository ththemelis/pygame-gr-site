"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 10.

Τρέξε:  python check_exercises.py

Ελέγχει τις συναρτήσεις του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import sys

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


# ---- Άσκηση 1: remove_fallen

class FakeStar:
    """Ένα απλό αστέρι για τις δοκιμές: έχει μόνο ένα όνομα και την ιδιότητα y."""

    def __init__(self, name, y):
        self.name = name
        self.y = y


def make_stars(ys):
    """Φτιάχνει αστέρια με ονόματα A, B, C, … και τα y που δίνονται."""
    stars = []
    for index in range(len(ys)):
        stars.append(FakeStar("ABCDEFGH"[index], ys[index]))
    return stars


def names_of(stars):
    names = []
    for star in stars:
        names.append(star.name)
    return names


def fallen_names(arguments):
    """Τα ονόματα των αστεριών που μένουν στη λίστα."""
    ys, limit = arguments
    return names_of(exercises.remove_fallen(make_stars(ys), limit))


def fallen_original_unchanged(unused):
    """Η αρχική λίστα δεν αλλάζει, και το αποτέλεσμα είναι άλλη λίστα."""
    stars = make_stars((100, 600, 300))
    result = exercises.remove_fallen(stars, 500)
    return names_of(stars), result is stars


def fallen_new_list(unused):
    """Ακόμη κι όταν μένουν όλα τα αστέρια, επιστρέφεται ΝΕΑ λίστα (τύπου list)."""
    stars = make_stars((100, 200))
    result = exercises.remove_fallen(stars, 500)
    return result is stars, type(result).__name__


def fallen_same_objects(unused):
    """Στη λίστα μένουν τα ίδια αντικείμενα, όχι αντίγραφα."""
    first = FakeStar("A", 100)
    second = FakeStar("B", 600)
    third = FakeStar("C", 300)
    result = exercises.remove_fallen([first, second, third], 500)
    return len(result) == 2 and result[0] is first and result[1] is third


# ---- Άσκηση 2: spawn_interval

def call_spawn_interval(score):
    return exercises.spawn_interval(score)


def interval_type(score):
    return type(exercises.spawn_interval(score)).__name__


# ---- Άσκηση 3: distance και circle_touches_rect

def call_distance(arguments):
    x1, y1, x2, y2 = arguments
    return round(exercises.distance(x1, y1, x2, y2), 6)


def distance_type(arguments):
    x1, y1, x2, y2 = arguments
    return type(exercises.distance(x1, y1, x2, y2)).__name__


def touches(arguments):
    """Ο κύκλος (cx, cy, radius) και το ορθογώνιο (left, top, width, height), με την ίδια σειρά της συνάρτησης."""
    cx, cy, radius, left, top, width, height = arguments
    return exercises.circle_touches_rect(cx, cy, radius, left, top, width, height)


# ---- Άσκηση 4: game_status

def call_status(arguments):
    score, lives, goal = arguments
    return exercises.game_status(score, lives, goal)


print("Άσκηση 1 (κύκλος 1): remove_fallen")
for arguments, expected in (
        (((), 500), []),
        (((100, 600, 300), 500), ["A", "C"]),
        (((100, 200, 300), 500), ["A", "B", "C"]),
        (((600, 700), 500), []),
        (((500,), 500), ["A"]),
        (((500.5,), 500), []),
        (((600, 600, 600, 100), 500), ["D"]),
        (((100, 600, 600, 600), 500), ["A"]),
        (((600, 100, 600, 200, 700, 300), 500), ["B", "D", "F"]),
        (((-5, 0, 5), 0), ["A", "B"]),
        (((493.9, 494.0, 494.1), 494), ["A", "B"]),
):
    run_check(f"remove_fallen με y = {arguments[0]} και όριο {arguments[1]} -> μένουν {expected}", fallen_names, arguments, expected)
run_check("η αρχική λίστα δεν αλλάζει και το αποτέλεσμα είναι άλλη λίστα", fallen_original_unchanged, None, (["A", "B", "C"], False))
run_check("ακόμη κι όταν μένουν όλα τα αστέρια, επιστρέφεται νέα λίστα", fallen_new_list, None, (False, "list"))
run_check("στη λίστα μένουν τα ίδια αντικείμενα, όχι αντίγραφα", fallen_same_objects, None, True)

print("Άσκηση 2 (κύκλος 2): spawn_interval")
for score, expected in (
        (0, 1000), (1, 1000), (2, 1000), (3, 850), (4, 850), (5, 850), (6, 700), (8, 700), (9, 550), (11, 550), (12, 400),
        (13, 400), (30, 400), (100, 400),
):
    run_check(f"spawn_interval({score}) -> {expected}", call_spawn_interval, score, expected)
run_check("το αποτέλεσμα της spawn_interval είναι ακέραιος αριθμός", interval_type, 7, "int")

print("Άσκηση 3 (κύκλος 3): distance και circle_touches_rect")
for arguments, expected in (
        ((0, 0, 3, 4), 5.0),
        ((3, 4, 0, 0), 5.0),
        ((1, 1, 1, 1), 0.0),
        ((-3, -4, 0, 0), 5.0),
        ((0, 0, 0, 7), 7.0),
        ((5, 0, 0, 0), 5.0),
        ((10, 2, 4, -6), 10.0),
        ((2.5, 1.5, 2.5, 5.5), 4.0),
        ((0, 0, 1, 1), 1.414214),
):
    run_check(f"distance{arguments} -> {expected}", call_distance, arguments, expected)
run_check("το αποτέλεσμα της distance είναι δεκαδικός αριθμός (float)", distance_type, (0, 0, 3, 4), "float")
for arguments, expected in (
        ((245, 450, 14, 200, 440, 90, 28), True),      # το κέντρο μέσα στο ορθογώνιο
        ((245, 430, 14, 200, 440, 90, 28), True),      # από πάνω, σε απόσταση 10
        ((245, 426, 14, 200, 440, 90, 28), True),      # από πάνω, σε απόσταση ακριβώς 14: ακουμπά
        ((245, 425, 14, 200, 440, 90, 28), False),     # από πάνω, σε απόσταση 15
        ((186, 450, 14, 200, 440, 90, 28), True),      # από αριστερά, απόσταση 14
        ((185, 450, 14, 200, 440, 90, 28), False),     # από αριστερά, απόσταση 15
        ((304, 450, 14, 200, 440, 90, 28), True),      # από δεξιά, απόσταση 14
        ((305, 450, 14, 200, 440, 90, 28), False),     # από δεξιά, απόσταση 15
        ((245, 482, 14, 200, 440, 90, 28), True),      # από κάτω, απόσταση 14
        ((245, 483, 14, 200, 440, 90, 28), False),     # από κάτω, απόσταση 15
        ((190, 430, 14, 200, 440, 90, 28), False),     # κοντά στη γωνία: dx = 10, dy = 10, απόσταση 14,14
        ((191, 431, 14, 200, 440, 90, 28), True),      # κοντά στη γωνία: dx = 9, dy = 9, απόσταση 12,7
        ((197, 436, 5, 200, 440, 90, 28), True),       # γωνία: dx = 3, dy = 4, απόσταση ακριβώς 5
        ((196, 436, 5, 200, 440, 90, 28), False),      # γωνία: dx = 4, dy = 4, απόσταση 5,7
        ((293, 472, 5, 200, 440, 90, 28), True),       # κάτω δεξιά γωνία: dx = 3, dy = 4
        ((294, 472, 5, 200, 440, 90, 28), False),      # κάτω δεξιά γωνία: dx = 4, dy = 4
        ((0, 0, 14, 200, 440, 90, 28), False),         # πολύ μακριά
        ((200, 450, 0, 200, 440, 90, 28), True),       # ακτίνα 0, πάνω στην αριστερή πλευρά
        ((199, 450, 0, 200, 440, 90, 28), False),      # ακτίνα 0, έξω
        ((245, 450, 0, 200, 440, 90, 28), True),       # ακτίνα 0, μέσα
        ((5, 5, 15, 10, 20, 30, 40), False),           # άλλο ορθογώνιο: απόσταση 15,8
        ((5, 5, 16, 10, 20, 30, 40), True),
        ((60, 0, 10, -50, -50, 100, 100), True),       # αρνητικές συντεταγμένες: απόσταση ακριβώς 10
        ((61, 0, 10, -50, -50, 100, 100), False),
):
    run_check(f"circle_touches_rect{arguments} -> {expected}", touches, arguments, expected)

print("Άσκηση 4 (κύκλος 4): game_status")
for arguments, expected in (
        ((0, 3, 15), "playing"),
        ((14, 1, 15), "playing"),
        ((14, 3, 15), "playing"),
        ((2, 1, 3), "playing"),
        ((15, 3, 15), "won"),
        ((16, 3, 15), "won"),
        ((15, 0, 15), "won"),
        ((20, 0, 15), "won"),
        ((5, 0, 15), "lost"),
        ((5, -1, 15), "lost"),
        ((0, 0, 1), "lost"),
        ((0, 1, 1), "playing"),
        ((1, 1, 1), "won"),
):
    run_check(f"game_status{arguments} -> {expected!r}", call_status, arguments, expected)

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
