"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 13.

Τρέξε:  python check_exercises.py

Ελέγχει τα περιεχόμενα του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import contextlib
import random
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


@contextlib.contextmanager
def limited_random(limit=5000):
    """Όσο τρέχει, οι συναρτήσεις του random μετρούν τις κλήσεις τους και σταματούν με σφάλμα μετά από limit κλήσεις.
    Έτσι ένας βρόχος που δεν τελειώνει ποτέ δεν κολλά τον έλεγχο."""
    calls = {"count": 0}
    names = ("random", "randint", "randrange", "choice", "choices", "shuffle", "sample", "uniform")
    saved = {}

    def counting(real):
        def wrapper(*args, **kwargs):
            calls["count"] += 1
            if calls["count"] > limit:
                raise RuntimeError(f"η random κλήθηκε πάνω από {limit} φορές (βρόχος που δεν τελειώνει;)")
            return real(*args, **kwargs)
        return wrapper

    for name in names:
        saved[name] = getattr(random, name)
        setattr(random, name, counting(saved[name]))
    try:
        yield
    finally:
        for name in names:
            setattr(random, name, saved[name])


# ---- Άσκηση 1: next_cell και turn

def call_next_cell(arguments):
    cell, direction = arguments
    return exercises.next_cell(cell, direction)


def next_cell_type(unused):
    return type(exercises.next_cell((5, 3), (1, 0))).__name__


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NAMES = {UP: "πάνω", DOWN: "κάτω", LEFT: "αριστερά", RIGHT: "δεξιά"}


def call_turn(arguments):
    direction, wanted = arguments
    return exercises.turn(direction, wanted)


def turn_type(unused):
    return type(exercises.turn((1, 0), (0, -1))).__name__


# ---- Άσκηση 2: move_snake και place_food

def call_move_snake(arguments):
    snake, direction, grow = arguments
    return exercises.move_snake(snake, direction, grow)


def move_snake_keeps_original(arguments):
    """Η λίστα που δίνουμε δεν αλλάζει, και το αποτέλεσμα είναι άλλη λίστα. Επιστρέφει (η αρχική δεν άλλαξε, είναι άλλη λίστα)."""
    snake, direction, grow = arguments
    given = list(snake)
    result = exercises.move_snake(given, direction, grow)
    return given == snake, result is not given


def move_snake_types(arguments):
    """Ο τύπος του αποτελέσματος και των κελιών του."""
    snake, direction, grow = arguments
    result = exercises.move_snake(snake, direction, grow)
    kinds = []
    for cell in result:
        kinds.append(type(cell).__name__)
    return type(result).__name__, kinds


def food_with_limit(arguments):
    snake, cols, rows = arguments
    with limited_random():
        return exercises.place_food(snake, cols, rows)


def food_is_valid(arguments):
    """Σε πολλές κλήσεις, πόσες φορές η τροφή είναι πλειάδα μέσα στο πλέγμα και έξω από το φίδι."""
    snake, cols, rows, count = arguments
    random.seed(12)
    good = 0
    with limited_random(20000):
        for number in range(count):
            food = exercises.place_food(snake, cols, rows)
            if isinstance(food, tuple) and len(food) == 2 and food not in snake:
                if 0 <= food[0] < cols and 0 <= food[1] < rows:
                    good += 1
    return good


def food_covers_all(arguments):
    """Σε πολλές κλήσεις, ποια κελιά εμφανίστηκαν (ταξινομημένα και χωρίς επαναλήψεις)."""
    snake, cols, rows, count = arguments
    random.seed(5)
    seen = []
    with limited_random(20000):
        for number in range(count):
            food = exercises.place_food(snake, cols, rows)
            if food not in seen:
                seen.append(food)
    return sorted(seen)


def food_keeps_snake(arguments):
    snake, cols, rows = arguments
    given = list(snake)
    with limited_random():
        exercises.place_food(given, cols, rows)
    return given == snake


def food_type(unused):
    with limited_random():
        return type(exercises.place_food([(0, 0)], 3, 3)).__name__


# ---- Άσκηση 3: is_dead

def call_is_dead(arguments):
    snake, cols, rows = arguments
    return exercises.is_dead(snake, cols, rows)


def is_dead_keeps_snake(arguments):
    snake, cols, rows = arguments
    given = list(snake)
    exercises.is_dead(given, cols, rows)
    return given == snake


def is_dead_type(unused):
    return type(exercises.is_dead([(1, 1), (0, 1)], 8, 5)).__name__


# ---- Άσκηση 4: step και step_interval

def call_step(arguments):
    snake, direction, food, cols, rows = arguments
    return exercises.step(snake, direction, food, cols, rows)


def step_keeps_original(arguments):
    """Η λίστα που δίνουμε δεν αλλάζει, ούτε όταν το φίδι τρώει ούτε όταν χτυπά."""
    snake, direction, food, cols, rows = arguments
    given = list(snake)
    exercises.step(given, direction, food, cols, rows)
    return given == snake


def step_types(arguments):
    """Οι τύποι των τριών τιμών που επιστρέφει η step."""
    snake, direction, food, cols, rows = arguments
    result = exercises.step(snake, direction, food, cols, rows)
    kinds = []
    for item in result:
        kinds.append(type(item).__name__)
    return kinds


def call_step_interval(score):
    return exercises.step_interval(score)


def step_interval_type(score):
    return type(exercises.step_interval(score)).__name__


print("Άσκηση 1 (κύκλος 1): next_cell και turn")
for arguments, expected in (
        (((5, 3), RIGHT), (6, 3)),
        (((5, 3), LEFT), (4, 3)),
        (((5, 3), DOWN), (5, 4)),
        (((5, 3), UP), (5, 2)),
        (((0, 0), LEFT), (-1, 0)),
        (((0, 0), UP), (0, -1)),
        (((31, 20), RIGHT), (32, 20)),
        (((31, 20), DOWN), (31, 21)),
        (((16, 10), RIGHT), (17, 10)),
        (((16, 10), UP), (16, 9)),
):
    cell, direction = arguments
    run_check(f"next_cell({cell}, {NAMES[direction]}) -> {expected}", call_next_cell, arguments, expected)
run_check("το αποτέλεσμα της next_cell είναι πλειάδα (tuple)", next_cell_type, None, "tuple")
for direction in (UP, DOWN, LEFT, RIGHT):
    for wanted in (UP, DOWN, LEFT, RIGHT):
        opposite = (wanted[0] == -direction[0] and wanted[1] == -direction[1])
        expected = direction if opposite else wanted
        what = "αντίθετη, μένει η ίδια κατεύθυνση" if opposite else "γίνεται δεκτή"
        run_check(f"turn: το φίδι πάει {NAMES[direction]} και ο παίκτης ζητά {NAMES[wanted]} ({what})", call_turn, (direction, wanted), expected)
run_check("το αποτέλεσμα της turn είναι πλειάδα (tuple)", turn_type, None, "tuple")

print("Άσκηση 2 (κύκλος 2): move_snake και place_food")
STRAIGHT = [(5, 3), (4, 3), (3, 3)]
BENT = [(5, 3), (5, 4), (4, 4), (3, 4)]
for arguments, expected in (
        ((STRAIGHT, RIGHT, False), [(6, 3), (5, 3), (4, 3)]),
        ((STRAIGHT, RIGHT, True), [(6, 3), (5, 3), (4, 3), (3, 3)]),
        ((STRAIGHT, UP, False), [(5, 2), (5, 3), (4, 3)]),
        ((STRAIGHT, DOWN, False), [(5, 4), (5, 3), (4, 3)]),
        ((STRAIGHT, UP, True), [(5, 2), (5, 3), (4, 3), (3, 3)]),
        ((BENT, UP, False), [(5, 2), (5, 3), (5, 4), (4, 4)]),
        ((BENT, RIGHT, False), [(6, 3), (5, 3), (5, 4), (4, 4)]),
        ((BENT, RIGHT, True), [(6, 3), (5, 3), (5, 4), (4, 4), (3, 4)]),
        (([(5, 5)], RIGHT, False), [(6, 5)]),
        (([(5, 5)], RIGHT, True), [(6, 5), (5, 5)]),
        (([(0, 0), (1, 0)], LEFT, False), [(-1, 0), (0, 0)]),
        (([(0, 0), (1, 0)], LEFT, True), [(-1, 0), (0, 0), (1, 0)]),
        (([(7, 2), (6, 2)], RIGHT, False), [(8, 2), (7, 2)]),
):
    snake, direction, grow = arguments
    verb = "μεγαλώνει" if grow else "δεν μεγαλώνει"
    run_check(f"move_snake({snake}, {NAMES[direction]}, {grow}): το φίδι {verb} -> {expected}", call_move_snake, arguments, expected)
run_check("η move_snake δεν αλλάζει τη λίστα που της δίνουμε, και επιστρέφει άλλη λίστα (χωρίς μεγάλωμα)", move_snake_keeps_original,
          (STRAIGHT, RIGHT, False), (True, True))
run_check("η move_snake δεν αλλάζει τη λίστα που της δίνουμε, και επιστρέφει άλλη λίστα (με μεγάλωμα)", move_snake_keeps_original,
          (STRAIGHT, RIGHT, True), (True, True))
run_check("η move_snake επιστρέφει λίστα από πλειάδες", move_snake_types, (STRAIGHT, RIGHT, False), ("list", ["tuple", "tuple", "tuple"]))
for arguments, expected in (
        (([(0, 0), (1, 0), (0, 1)], 2, 2), (1, 1)),
        (([(0, 0), (1, 0), (1, 1)], 2, 2), (0, 1)),
        (([(1, 1), (0, 1), (1, 0)], 2, 2), (0, 0)),
        (([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)], 3, 2), (2, 1)),
        (([(0, 0)], 1, 1), None),
        (([(0, 0), (1, 0), (0, 1), (1, 1)], 2, 2), None),
        (([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], 3, 2), None),
):
    snake, cols, rows = arguments
    what = "ένα ελεύθερο κελί" if expected is not None else "κανένα ελεύθερο κελί"
    run_check(f"place_food({snake}, {cols}, {rows}): {what} -> {expected}", food_with_limit, arguments, expected)
run_check("place_food: σε 200 κλήσεις η τροφή είναι πάντα μέσα στο πλέγμα και έξω από το φίδι", food_is_valid,
          ([(3, 2), (3, 3), (2, 3), (1, 3), (1, 2), (1, 1)], 6, 5, 200), 200)
run_check("place_food: στο πλέγμα του παιχνιδιού η τροφή είναι πάντα έξω από το φίδι", food_is_valid,
          ([(16, 10), (15, 10), (14, 10)], 32, 21, 200), 200)
run_check("place_food: κάθε ελεύθερο κελί μπορεί να βγει (σε πλέγμα 3 × 2 με δύο κελιά του φιδιού)", food_covers_all,
          ([(0, 0), (1, 0)], 3, 2, 300), [(0, 1), (1, 1), (2, 0), (2, 1)])
run_check("place_food: η τροφή μπορεί να βγει στις δύο ακραίες γωνίες που μένουν ελεύθερες", food_covers_all,
          ([(1, 0), (0, 1), (1, 1), (2, 1)], 3, 2, 200), [(0, 0), (2, 0)])
run_check("η place_food δεν αλλάζει τη λίστα του φιδιού", food_keeps_snake, ([(0, 0), (1, 0)], 3, 2), True)
run_check("το αποτέλεσμα της place_food είναι πλειάδα (tuple)", food_type, None, "tuple")

print("Άσκηση 3 (κύκλος 3): is_dead")
for arguments, expected in (
        (([(3, 2), (2, 2), (1, 2)], 8, 5), False),
        (([(0, 0), (1, 0), (2, 0)], 8, 5), False),          # η πάνω αριστερή γωνία είναι μέσα στο πλέγμα
        (([(7, 0), (6, 0), (5, 0)], 8, 5), False),
        (([(0, 4), (1, 4), (2, 4)], 8, 5), False),
        (([(7, 4), (6, 4), (5, 4)], 8, 5), False),          # η κάτω δεξιά γωνία είναι μέσα στο πλέγμα
        (([(-1, 2), (0, 2), (1, 2)], 8, 5), True),          # έξω από την αριστερή πλευρά
        (([(8, 2), (7, 2), (6, 2)], 8, 5), True),           # έξω από τη δεξιά πλευρά: η στήλη 8 δεν υπάρχει
        (([(3, -1), (3, 0), (3, 1)], 8, 5), True),          # έξω από την πάνω πλευρά
        (([(3, 5), (3, 4), (3, 3)], 8, 5), True),           # έξω από την κάτω πλευρά: η γραμμή 5 δεν υπάρχει
        (([(8, 5), (7, 5)], 8, 5), True),
        (([(-1, -1), (0, 0)], 8, 5), True),
        (([(100, 2), (99, 2)], 8, 5), True),
        (([(4, 3), (4, 4), (3, 4), (3, 3), (4, 3)], 8, 5), True),     # το κεφάλι πέφτει στο τελευταίο κελί
        (([(3, 3), (4, 3), (4, 4), (3, 4), (3, 3), (2, 3)], 8, 5), True),    # το κεφάλι πέφτει σε κελί στη μέση
        (([(3, 3), (3, 3)], 8, 5), True),                   # το κεφάλι πέφτει στο δεύτερο κελί
        (([(3, 2), (3, 3), (2, 3), (2, 2), (2, 1)], 8, 5), False),    # το κεφάλι ακουμπά το σώμα, χωρίς να πέφτει πάνω του
        (([(1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (1, 2), (0, 2)], 8, 5), False),
        (([(31, 20), (30, 20), (29, 20)], 32, 21), False),
        (([(32, 20), (31, 20), (30, 20)], 32, 21), True),
        (([(31, 21), (31, 20), (31, 19)], 32, 21), True),
):
    snake, cols, rows = arguments
    run_check(f"is_dead({snake}, {cols}, {rows}) -> {expected}", call_is_dead, arguments, expected)
run_check("η is_dead δεν αλλάζει τη λίστα του φιδιού", is_dead_keeps_snake, ([(3, 3), (4, 3), (4, 4), (3, 4), (3, 3)], 8, 5), True)
run_check("το αποτέλεσμα της is_dead είναι True ή False (bool)", is_dead_type, None, "bool")

print("Άσκηση 4 (κύκλος 4): step και step_interval")
for arguments, expected in (
        (([(5, 3), (4, 3), (3, 3)], RIGHT, (9, 9), 32, 21), ([(6, 3), (5, 3), (4, 3)], False, False)),
        (([(5, 3), (4, 3), (3, 3)], RIGHT, (6, 3), 32, 21), ([(6, 3), (5, 3), (4, 3), (3, 3)], True, False)),
        (([(5, 3), (4, 3), (3, 3)], DOWN, (5, 4), 32, 21), ([(5, 4), (5, 3), (4, 3), (3, 3)], True, False)),
        (([(5, 3), (4, 3), (3, 3)], UP, (6, 3), 32, 21), ([(5, 2), (5, 3), (4, 3)], False, False)),
        (([(5, 3), (5, 4), (4, 4), (3, 4)], LEFT, (4, 3), 32, 21), ([(4, 3), (5, 3), (5, 4), (4, 4), (3, 4)], True, False)),
        (([(31, 3), (30, 3), (29, 3)], RIGHT, (9, 9), 32, 21), ([(31, 3), (30, 3), (29, 3)], False, True)),
        (([(0, 3), (1, 3), (2, 3)], LEFT, (9, 9), 32, 21), ([(0, 3), (1, 3), (2, 3)], False, True)),
        (([(5, 0), (5, 1), (5, 2)], UP, (9, 9), 32, 21), ([(5, 0), (5, 1), (5, 2)], False, True)),
        (([(5, 20), (5, 19), (5, 18)], DOWN, (9, 9), 32, 21), ([(5, 20), (5, 19), (5, 18)], False, True)),
        (([(3, 2), (3, 3), (2, 3), (2, 2), (2, 1)], LEFT, (9, 9), 8, 5), ([(3, 2), (3, 3), (2, 3), (2, 2), (2, 1)], False, True)),
        (([(3, 2), (3, 3), (2, 3), (2, 2)], LEFT, (9, 9), 8, 5), ([(2, 2), (3, 2), (3, 3), (2, 3)], False, False)),
        (([(3, 2), (3, 3), (2, 3), (2, 2)], LEFT, (1, 1), 8, 5), ([(2, 2), (3, 2), (3, 3), (2, 3)], False, False)),
        (([(0, 0)], LEFT, (3, 3), 8, 5), ([(0, 0)], False, True)),
        (([(0, 0)], RIGHT, (1, 0), 8, 5), ([(1, 0), (0, 0)], True, False)),
        (([(7, 4), (6, 4), (5, 4)], RIGHT, (3, 3), 8, 5), ([(7, 4), (6, 4), (5, 4)], False, True)),
        (([(7, 4), (6, 4), (5, 4)], UP, (7, 3), 8, 5), ([(7, 3), (7, 4), (6, 4), (5, 4)], True, False)),
        (([(3, 2), (3, 3), (2, 3), (2, 2), (2, 1)], LEFT, (2, 2), 8, 5), ([(3, 2), (3, 3), (2, 3), (2, 2), (2, 1)], False, True)),
        (([(31, 3), (30, 3), (29, 3)], RIGHT, (32, 3), 32, 21), ([(31, 3), (30, 3), (29, 3)], False, True)),
):
    snake, direction, food, cols, rows = arguments
    run_check(f"step({snake}, {NAMES[direction]}, τροφή {food}, {cols}, {rows}) -> {expected}", call_step, arguments, expected)
run_check("η step δεν αλλάζει τη λίστα που της δίνουμε (κίνηση)", step_keeps_original, ([(5, 3), (4, 3), (3, 3)], RIGHT, (9, 9), 32, 21), True)
run_check("η step δεν αλλάζει τη λίστα που της δίνουμε (φαγητό)", step_keeps_original, ([(5, 3), (4, 3), (3, 3)], RIGHT, (6, 3), 32, 21), True)
run_check("η step δεν αλλάζει τη λίστα που της δίνουμε (χτύπημα)", step_keeps_original, ([(31, 3), (30, 3), (29, 3)], RIGHT, (9, 9), 32, 21), True)
run_check("η step επιστρέφει λίστα, bool και bool", step_types, ([(5, 3), (4, 3), (3, 3)], RIGHT, (9, 9), 32, 21), ["list", "bool", "bool"])
run_check("η step επιστρέφει λίστα, bool και bool (όταν το φίδι χτυπά)", step_types, ([(31, 3), (30, 3), (29, 3)], RIGHT, (9, 9), 32, 21),
          ["list", "bool", "bool"])
for score, expected in (
        (0, 160), (1, 155), (2, 150), (3, 145), (4, 140), (5, 135), (10, 110), (17, 75), (18, 70), (19, 70), (25, 70), (100, 70),
):
    run_check(f"step_interval({score}) -> {expected}", call_step_interval, score, expected)
run_check("το αποτέλεσμα της step_interval είναι ακέραιος (int)", step_interval_type, 7, "int")

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
