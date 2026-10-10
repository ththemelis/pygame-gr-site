"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 5.

Τρέξε:  python check_exercises.py

Ελέγχει τις συναρτήσεις του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.

Οι δοκιμές με αρχεία γίνονται σε προσωρινό φάκελο, που σβήνεται μόλις τελειώσει η δοκιμή:
δεν αγγίζουν κανένα δικό σου αρχείο.
"""

import os
import sys
import tempfile

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


def lines_in_file(text):
    """Γράφει το text σε προσωρινό αρχείο και επιστρέφει όσα δίνει η count_lines για αυτό."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        path = os.path.join(folder, "test.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return exercises.count_lines(path)


def lines_in_missing_file(name):
    """Καλεί την count_lines για αρχείο που δεν υπάρχει."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        return exercises.count_lines(os.path.join(folder, name))


def symbol_count(arguments):
    grid, symbol = arguments
    return exercises.count_symbol(grid, symbol)


def one_step(arguments):
    grid, x, y, key = arguments
    return exercises.step(grid, x, y, key)


def square_grid():
    """Νέο πλέγμα 3x3 χωρίς εξωτερικούς τοίχους, με τοίχο στο κέντρο."""
    return ["...", ".#.", "..."]


def wide_grid():
    """Νέο πλέγμα 2 γραμμών και 4 στηλών, με τοίχο στη θέση x=1, y=1."""
    return ["....", ".#.."]


def grid_after_steps(grid):
    """Καλεί τη step πολλές φορές και επιστρέφει το πλέγμα, για να δούμε αν άλλαξε."""
    exercises.step(grid, 0, 0, "D")
    exercises.step(grid, 0, 0, "S")
    exercises.step(grid, 2, 2, "W")
    return grid


def file_after_appends(arguments):
    """Βάζει (αν χρειάζεται) αρχικό περιεχόμενο, καλεί την append_line για κάθε γραμμή και επιστρέφει το αρχείο."""
    initial, lines = arguments
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        path = os.path.join(folder, "log.txt")
        if initial is not None:
            with open(path, "w", encoding="utf-8") as file:
                file.write(initial)
        for line in lines:
            exercises.append_line(path, line)
        with open(path, "r", encoding="utf-8") as file:
            return file.read()


print("Άσκηση 1 (κύκλος 1): count_lines")
for text, expected in (("α\nβ\nγ\n", 3), ("α\nβ\nγ", 3), ("α", 1), ("", 0), ("\n\n", 2), ("Γειά σου\nκόσμε\n", 2)):
    run_check(f"αρχείο με κείμενο {text!r} -> {expected}", lines_in_file, text, expected)
run_check("αρχείο που δεν υπάρχει -> None", lines_in_missing_file, "δεν-υπάρχει.txt", None)

print("Άσκηση 2 (κύκλος 2): count_symbol")
symbol_tests = (
    (["#.#", "..#"], "#", 3),
    (["#.#", "..#"], ".", 3),
    (["#.#", "..#"], "$", 0),
    ([], "#", 0),
    (["P...", "..$."], ".", 6),
    (["####", "#..#", "####"], "#", 10),
)
for grid, symbol, expected in symbol_tests:
    run_check(f"count_symbol({grid}, {symbol!r}) -> {expected}", symbol_count, (grid, symbol), expected)

print("Άσκηση 3 (κύκλος 3): step")
step_tests = (
    ("3x3", square_grid, 0, 0, "D", (1, 0)),
    ("3x3", square_grid, 0, 0, "S", (0, 1)),
    ("3x3", square_grid, 2, 2, "W", (2, 1)),
    ("3x3", square_grid, 2, 2, "A", (1, 2)),
    ("3x3, τοίχος", square_grid, 1, 0, "S", (1, 0)),
    ("3x3, τοίχος", square_grid, 0, 1, "D", (0, 1)),
    ("3x3, πάνω άκρο", square_grid, 0, 0, "W", (0, 0)),
    ("3x3, αριστερό άκρο", square_grid, 0, 0, "A", (0, 0)),
    ("3x3, κάτω άκρο", square_grid, 2, 2, "S", (2, 2)),
    ("3x3, δεξί άκρο", square_grid, 2, 2, "D", (2, 2)),
    ("3x3, πεζό πλήκτρο", square_grid, 0, 0, "d", (1, 0)),
    ("3x3, άκυρο πλήκτρο", square_grid, 0, 0, "X", (0, 0)),
    ("3x3, κενό πλήκτρο", square_grid, 0, 0, "", (0, 0)),
    ("2x4", wide_grid, 3, 0, "S", (3, 1)),
    ("2x4, κάτω άκρο", wide_grid, 3, 1, "S", (3, 1)),
    ("2x4, δεξί άκρο", wide_grid, 3, 0, "D", (3, 0)),
)
for name, make_grid, x, y, key, expected in step_tests:
    run_check(f"πλέγμα {name}: step(x={x}, y={y}, {key!r}) -> {expected}", one_step, (make_grid(), x, y, key), expected)
run_check("η step δεν αλλάζει το πλέγμα που παίρνει", grid_after_steps, square_grid(), square_grid())

print("Άσκηση 4 (κύκλος 4): append_line")
append_tests = (
    ("νέο αρχείο, μία γραμμή", (None, ["α"]), "α\n"),
    ("νέο αρχείο, δύο γραμμές", (None, ["α", "β"]), "α\nβ\n"),
    ("υπάρχον αρχείο: δεν σβήνεται το περιεχόμενο", ("α\n", ["β"]), "α\nβ\n"),
    ("ελληνικά και κενά", (None, ["Νίκη σε 30 βήματα"]), "Νίκη σε 30 βήματα\n"),
)
for description, arguments, expected in append_tests:
    run_check(f"{description} -> {expected!r}", file_after_appends, arguments, expected)

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
