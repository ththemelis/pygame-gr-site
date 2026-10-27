"""Αυτοέλεγχος της λογικής του παιχνιδιού (το logic.py).

Τρέξε:  python check_logic.py

Κάθε δοκιμή είναι μια γραμμή του πίνακα TESTS: (όνομα συνάρτησης, ορίσματα σε παρενθέσεις, αναμενόμενο αποτέλεσμα).
Για κάθε συνάρτηση που γράφετε στο logic.py, προσθέστε εδώ τα παραδείγματά της από το φύλλο σχεδίου, ΠΡΙΝ τη γράψετε:
πρώτα ορίζετε τι πρέπει να επιστρέφει και μετά τη γράφετε μέχρι να περάσουν όλα.
"""

import math
import sys

try:
    import logic
except ImportError:
    print("Δεν βρέθηκε το logic.py. Βάλ' το στον ίδιο φάκελο με αυτό το αρχείο.")
    sys.exit(1)

TESTS = [
    # ο πίνακας μεταβάσεων
    ("next_state", ("menu", "play"), "playing"),
    ("next_state", ("playing", "lose"), "game over"),
    ("next_state", ("playing", "menu"), "menu"),
    ("next_state", ("game over", "play"), "playing"),
    ("next_state", ("game over", "menu"), "menu"),
    ("next_state", ("menu", "lose"), "menu"),                  # στο μενού δεν χάνεις: τίποτα δεν αλλάζει
    ("next_state", ("playing", "play"), "playing"),            # το «play» δεν ξαναρχίζει ένα παιχνίδι που τρέχει
    # η clamp
    ("clamp", (5, 0, 10), 5),
    ("clamp", (-3, 0, 10), 0),
    ("clamp", (15, 0, 10), 10),
    ("clamp", (0, 0, 10), 0),
    ("clamp", (10, 0, 10), 10),
    # η move
    ("move", (100, 1, 200, 0.5, 0, 600), 200),
    ("move", (100, -1, 200, 0.5, 0, 600), 0),
    ("move", (100, 0, 200, 0.5, 0, 600), 100),
    ("move", (590, 1, 200, 0.5, 0, 600), 600),                 # σταματά στο όριο
    ("move", (10, -1, 200, 0.5, 0, 600), 0),
    # η new_game
    ("new_game", (300, 245), {"x": 300, "y": 245, "time": 0.0, "score": 0}),
    # ΠΡΟΣΘΕΣΤΕ ΕΔΩ τα παραδείγματα των δικών σας συναρτήσεων
]


# ---- Από εδώ και κάτω δεν χρειάζεται να αλλάξετε τίποτα

def same(got, expected):
    """Ίσα αποτελέσματα. Οι δεκαδικοί αριθμοί συγκρίνονται με μικρή ανοχή, γιατί οι πράξεις τους έχουν μικρά σφάλματα."""
    both_numbers = isinstance(got, (int, float)) and isinstance(expected, (int, float))
    both_bool = isinstance(got, bool) or isinstance(expected, bool)
    if both_numbers and not both_bool:
        return math.isclose(got, expected, abs_tol=1e-9)
    return got == expected and type(got) == type(expected)


def describe(name, arguments):
    """Η κλήση όπως γράφεται στον κώδικα, π.χ. clamp(5, 0, 10)."""
    texts = []
    for argument in arguments:
        texts.append(repr(argument))
    return f"{name}({', '.join(texts)})"


passed = 0
failed = 0
for name, arguments, expected in TESTS:
    if not isinstance(arguments, tuple):
        arguments = (arguments,)
    call = describe(name, arguments)
    function = getattr(logic, name, None)
    if function is None:
        failed += 1
        print(f"  [ΛΑΘΟΣ] {call}")
        print(f"      Δεν υπάρχει η συνάρτηση {name} στο logic.py.")
        continue
    try:
        got = function(*arguments)
    except Exception as error:
        failed += 1
        print(f"  [ΛΑΘΟΣ] {call}")
        print(f"      Προκλήθηκε σφάλμα {type(error).__name__}: {error}")
        continue
    if same(got, expected):
        passed += 1
        print(f"  [ΟΚ] {call} -> {expected!r}")
    else:
        failed += 1
        print(f"  [ΛΑΘΟΣ] {call}")
        print(f"      αναμενόμενο: {expected!r}")
        print(f"      πήρα:        {got!r}")

print()
if failed == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {passed} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {passed + failed} δοκιμές. Λάθος: {failed}.")
sys.exit(1)
