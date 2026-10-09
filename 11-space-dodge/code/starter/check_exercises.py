"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 11.

Τρέξε:  python check_exercises.py

Ελέγχει τα περιεχόμενα του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pygame
except ImportError:
    print("Δεν βρέθηκε η pygame-ce. Εγκατέστησέ την όπως στο Μάθημα 7.")
    sys.exit(1)

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


# ---- Άσκηση 1: fit_size

def call_fit_size(arguments):
    width, height, new_width = arguments
    return exercises.fit_size(width, height, new_width)


def fit_size_types(arguments):
    """Οι τύποι του αποτελέσματος: πλειάδα με δύο ακέραιους."""
    width, height, new_width = arguments
    result = exercises.fit_size(width, height, new_width)
    return type(result).__name__, type(result[0]).__name__, type(result[1]).__name__


# ---- Άσκηση 2: Asteroid

def make_asteroid(size, x, y, speed):
    """Ένας αστεροειδής με εικόνα size = (πλάτος, ύψος). Η εικόνα είναι ένα απλό Surface."""
    image = pygame.Surface(size)
    return exercises.Asteroid(image, x, y, speed), image


def asteroid_start(arguments):
    """Το κέντρο και το μέγεθος του rect αμέσως μετά τη δημιουργία: (κέντρο, μέγεθος)."""
    size, x, y = arguments
    asteroid, image = make_asteroid(size, x, y, 100)
    return asteroid.rect.center, asteroid.rect.size


def asteroid_attributes(unused):
    """Οι ιδιότητες image, x, y και speed έχουν ακριβώς όσα δόθηκαν."""
    asteroid, image = make_asteroid((40, 30), 123.5, -20.25, 140)
    return asteroid.image is image, asteroid.x, asteroid.y, asteroid.speed


def asteroid_after(arguments):
    """Ύστερα από count κλήσεις της update(dt): (y στρογγυλοποιημένο στο 6ο δεκαδικό, κέντρο y του rect, x, κέντρο x)."""
    y, speed, dt, count = arguments
    asteroid, image = make_asteroid((40, 30), 200, y, speed)
    for repetition in range(count):
        asteroid.update(dt)
    return round(asteroid.y, 6), asteroid.rect.centery, asteroid.x, asteroid.rect.centerx


def asteroid_odd_size(unused):
    """Εικόνα με περιττό μέγεθος 31 x 17 και κέντρο (100, 50): πάνω αριστερή γωνία του rect."""
    asteroid, image = make_asteroid((31, 17), 100, 50, 80)
    return asteroid.rect.topleft


def asteroid_size_after_update(unused):
    """Το μέγεθος του rect δεν αλλάζει όταν κινείται ο αστεροειδής."""
    asteroid, image = make_asteroid((48, 34), 100, 100, 150)
    asteroid.update(0.25)
    asteroid.update(0.25)
    return asteroid.rect.size


def asteroid_independent(unused):
    """Δύο αστεροειδείς είναι ανεξάρτητοι: το update του πρώτου δεν κινεί τον δεύτερο."""
    first, image_one = make_asteroid((40, 30), 100, 100, 100)
    second, image_two = make_asteroid((40, 30), 300, 100, 200)
    first.update(0.5)
    return first.y, second.y, second.rect.centery


def asteroid_update_returns(unused):
    """Η update δεν επιστρέφει τιμή."""
    asteroid, image = make_asteroid((40, 30), 100, 100, 100)
    return asteroid.update(0.1)


def asteroid_rect_type(unused):
    """Το rect είναι αντικείμενο Rect της pygame."""
    asteroid, image = make_asteroid((40, 30), 100, 100, 100)
    return type(asteroid.rect).__name__


# ---- Άσκηση 3: hitbox και rects_overlap

def call_hitbox(box):
    return exercises.hitbox(box)


def hitbox_type(box):
    return type(exercises.hitbox(box)).__name__


def hitbox_from_rect(arguments):
    """Το hitbox δέχεται και pygame.Rect."""
    return exercises.hitbox(pygame.Rect(*arguments))


def call_overlap(arguments):
    first, second = arguments
    return exercises.rects_overlap(first, second)


def overlap_symmetric(arguments):
    """Το αποτέλεσμα δεν εξαρτάται από τη σειρά των δύο ορθογωνίων."""
    first, second = arguments
    return exercises.rects_overlap(first, second) == exercises.rects_overlap(second, first)


def overlap_type(arguments):
    first, second = arguments
    return type(exercises.rects_overlap(first, second)).__name__


def overlap_with_rects(arguments):
    """Η rects_overlap δέχεται και pygame.Rect."""
    first, second = arguments
    return exercises.rects_overlap(pygame.Rect(*first), pygame.Rect(*second))


# ---- Άσκηση 4: difficulty

def call_difficulty(score):
    return exercises.difficulty(score)


def difficulty_types(score):
    result = exercises.difficulty(score)
    return type(result).__name__, len(result), type(result[0]).__name__, type(result[1]).__name__


print("Άσκηση 1 (κύκλος 1): fit_size")
for arguments, expected in (
        ((128, 96, 64), (64, 48)),
        ((128, 96, 32), (32, 24)),
        ((96, 96, 48), (48, 48)),
        ((96, 96, 72), (72, 72)),
        ((120, 84, 48), (48, 34)),
        ((120, 84, 72), (72, 50)),
        ((100, 50, 30), (30, 15)),
        ((100, 70, 33), (33, 23)),
        ((200, 100, 300), (300, 150)),
        ((64, 48, 64), (64, 48)),
        ((50, 80, 20), (20, 32)),
        ((30, 20, 17), (17, 11)),
        ((30, 20, 19), (19, 13)),
):
    run_check(f"fit_size{arguments} -> {expected}", call_fit_size, arguments, expected)
run_check("το αποτέλεσμα της fit_size είναι πλειάδα με δύο ακέραιους", fit_size_types, (120, 84, 48), ("tuple", "int", "int"))

print("Άσκηση 2 (κύκλος 2): Asteroid")
for arguments, expected in (
        (((48, 34), 100, 80), ((100, 80), (48, 34))),
        (((72, 72), 320, 60), ((320, 60), (72, 72))),
        (((48, 34), 100.6, 50.4), ((101, 50), (48, 34))),
        (((40, 30), 10.2, 10.8), ((10, 11), (40, 30))),
        (((40, 30), 100, -20.4), ((100, -20), (40, 30))),
):
    run_check(f"το rect ενός αστεροειδή με εικόνα {arguments[0]} στο ({arguments[1]}, {arguments[2]}): κέντρο και μέγεθος",
              asteroid_start, arguments, expected)
run_check("οι ιδιότητες image, x, y και speed έχουν όσα δόθηκαν", asteroid_attributes, None, (True, 123.5, -20.25, 140))
run_check("εικόνα 31 x 17 με κέντρο (100, 50): η πάνω αριστερή γωνία του rect είναι (85, 42)", asteroid_odd_size, None, (85, 42))
for arguments, expected in (
        ((100, 100, 0.5, 1), (150.0, 150, 200, 200)),
        ((100, 100, 0, 1), (100.0, 100, 200, 200)),
        ((100, 100, 1.0, 1), (200.0, 200, 200, 200)),
        ((0, 130, 0.016, 10), (20.8, 21, 200, 200)),
        ((0, 100, 0.016, 5), (8.0, 8, 200, 200)),
        ((0, 100, 0.016, 1), (1.6, 2, 200, 200)),
        ((-20.4, 50, 0.1, 1), (-15.4, -15, 200, 200)),
):
    y, speed, dt, count = arguments
    run_check(f"y = {y}, speed = {speed}, {count} × update({dt}): y, κέντρο y του rect, x, κέντρο x", asteroid_after, arguments, expected)
run_check("το μέγεθος του rect δεν αλλάζει όταν κινείται ο αστεροειδής", asteroid_size_after_update, None, (48, 34))
run_check("δύο αστεροειδείς είναι ανεξάρτητοι", asteroid_independent, None, (150.0, 100, 100))
run_check("η update δεν επιστρέφει τιμή", asteroid_update_returns, None, None)
run_check("το rect είναι Rect της pygame", asteroid_rect_type, None, "Rect")

print("Άσκηση 3 (κύκλος 3): hitbox και rects_overlap")
for box, expected in (
        ((100, 200, 64, 48), (108, 206, 48, 36)),
        ((0, 0, 48, 34), (6, 4, 36, 26)),
        ((0, 0, 72, 50), (9, 6, 54, 38)),
        ((0, 0, 48, 48), (6, 6, 36, 36)),
        ((10, 20, 40, 40), (15, 25, 30, 30)),
        ((-30, -20, 60, 40), (-23, -15, 45, 30)),
        ((5, 5, 3, 3), (5, 5, 3, 3)),
        ((0, 0, 7, 9), (0, 1, 6, 7)),
):
    run_check(f"hitbox({box}) -> {expected}", call_hitbox, box, expected)
run_check("το αποτέλεσμα της hitbox είναι πλειάδα", hitbox_type, (100, 200, 64, 48), "tuple")
run_check("η hitbox δέχεται και pygame.Rect", hitbox_from_rect, (100, 200, 64, 48), (108, 206, 48, 36))
for arguments, expected in (
        (((0, 0, 10, 10), (5, 5, 10, 10)), True),
        (((0, 0, 10, 10), (9, 9, 10, 10)), True),         # επικάλυψη ενός pixel
        (((0, 0, 10, 10), (10, 0, 10, 10)), False),       # ακουμπούν στη δεξιά πλευρά
        (((0, 0, 10, 10), (0, 10, 10, 10)), False),       # ακουμπούν στην κάτω πλευρά
        (((0, 0, 10, 10), (10, 10, 10, 10)), False),      # ακουμπούν μόνο σε μια γωνία
        (((0, 0, 10, 10), (11, 0, 10, 10)), False),
        (((0, 0, 10, 10), (0, 11, 10, 10)), False),
        (((0, 0, 10, 10), (-10, 0, 10, 10)), False),      # ακουμπούν στην αριστερή πλευρά
        (((0, 0, 10, 10), (-9, 0, 10, 10)), True),
        (((0, 0, 10, 10), (0, -10, 10, 10)), False),      # ακουμπούν στην πάνω πλευρά
        (((0, 0, 10, 10), (0, -9, 10, 10)), True),
        (((0, 0, 100, 100), (40, 40, 10, 10)), True),     # το ένα μέσα στο άλλο
        (((40, 40, 10, 10), (0, 0, 100, 100)), True),
        (((0, 0, 10, 10), (0, 0, 10, 10)), True),         # ίδια ορθογώνια
        (((0, 0, 10, 10), (50, 50, 10, 10)), False),
        (((0, 5, 10, 10), (20, 5, 10, 10)), False),       # ίδιο ύψος, μακριά οριζόντια
        (((5, 0, 10, 10), (5, 20, 10, 10)), False),       # ίδιο x, μακριά κάθετα
        (((-20, -20, 15, 15), (-10, -10, 15, 15)), True),     # αρνητικές συντεταγμένες
        (((-20, -20, 10, 10), (-10, -10, 10, 10)), False),    # αρνητικές συντεταγμένες, ακουμπούν σε γωνία
        (((100, 200, 48, 36), (130, 220, 36, 36)), True),
        (((0, 0, 20, 10), (15, 0, 10, 10)), True),        # ορθογώνια με διαφορετικά πλάτη και ύψη
        (((15, 0, 10, 10), (0, 0, 20, 10)), True),
        (((0, 0, 10, 20), (0, 15, 10, 10)), True),
        (((0, 15, 10, 10), (0, 0, 10, 20)), True),
        (((0, 0, 20, 10), (25, 0, 5, 10)), False),
):
    run_check(f"rects_overlap{arguments} -> {expected}", call_overlap, arguments, expected)
for arguments in (
        ((0, 0, 10, 10), (5, 5, 10, 10)),
        ((0, 0, 10, 10), (10, 0, 10, 10)),
        ((0, 0, 100, 100), (40, 40, 10, 10)),
        ((-20, -20, 15, 15), (-10, -10, 15, 15)),
):
    run_check(f"το αποτέλεσμα δεν εξαρτάται από τη σειρά των ορισμάτων: {arguments}", overlap_symmetric, arguments, True)
run_check("το αποτέλεσμα της rects_overlap είναι True ή False (bool)", overlap_type, ((0, 0, 10, 10), (5, 5, 10, 10)), "bool")
run_check("η rects_overlap δέχεται και pygame.Rect", overlap_with_rects, ((0, 0, 10, 10), (9, 9, 10, 10)), True)

print("Άσκηση 4 (κύκλος 4): difficulty")
for score, expected in (
        (0, (800, 190)), (4, (800, 190)), (5, (740, 205)), (9, (740, 205)), (10, (680, 220)), (12, (680, 220)),
        (15, (620, 235)), (25, (500, 265)), (40, (320, 310)), (44, (320, 310)), (45, (300, 325)), (50, (300, 330)),
        (100, (300, 330)),
):
    run_check(f"difficulty({score}) -> {expected}", call_difficulty, score, expected)
run_check("το αποτέλεσμα της difficulty είναι πλειάδα με δύο ακέραιους", difficulty_types, 12, ("tuple", 2, "int", "int"))

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
