"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 4.

Τρέξε:  python check_exercises.py

Ελέγχει τις συναρτήσεις του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import contextlib
import io
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


def answer_with(inputs):
    """Καλεί την ask_yes_no με προσομοιωμένες απαντήσεις του χρήστη."""
    with mock.patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(io.StringIO()):
        return exercises.ask_yes_no("Νέο παιχνίδι; ")


def numbers_after_min_max(numbers):
    """Καλεί τη min_max και επιστρέφει τη λίστα, για να δούμε αν άλλαξε."""
    exercises.min_max(numbers)
    return numbers


print("Άσκηση 1 (κύκλος 1): count_vowels")
for word, count in (("προγραμμα", 3), ("ΒΡΟΧΟΣ", 2), ("ψ", 0), ("", 0), (" Αεη ", 3), ("ΑΕΗΙΟΥΩ", 7)):
    run_check(f"count_vowels({word!r}) -> {count}", exercises.count_vowels, word, count)

print("Άσκηση 2 (κύκλος 2): letter_counts")
for word, expected in (("ΑΛΦΑ", {"Α": 2, "Λ": 1, "Φ": 1}), ("", {}), ("αΑ", {"Α": 2}), ("ΣΟΣ", {"Σ": 2, "Ο": 1})):
    run_check(f"letter_counts({word!r}) -> {expected}", exercises.letter_counts, word, expected)

print("Άσκηση 3 (κύκλος 3): min_max")
for numbers, expected in (([3, 1, 2], (1, 3)), ([5], (5, 5)), ([-4, 0, 7, 7], (-4, 7)), ([2.5, 1.5], (1.5, 2.5))):
    run_check(f"min_max({numbers}) -> {expected}", exercises.min_max, numbers, expected)
run_check("η min_max δεν αλλάζει τη λίστα που παίρνει", numbers_after_min_max, [3, 1, 2], [3, 1, 2])

print("Άσκηση 4 (κύκλος 4): ask_yes_no")
for inputs, expected in ((["ν"], True), (["ναι"], True), ([" ΝΑΙ "], True), (["ο"], False), (["όχι"], False),
                         (["x", "ν"], True), (["", "οχι"], False)):
    run_check(f"απαντήσεις {inputs} -> {expected}", answer_with, inputs, expected)

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
