"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 9.

Τρέξε:  python check_exercises.py

Ελέγχει τις συναρτήσεις και την κλάση του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
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


# ---- Άσκηση 1: key_direction

def call_key_direction(arguments):
    up_pressed, down_pressed = arguments
    return exercises.key_direction(up_pressed, down_pressed)


def key_direction_type(arguments):
    """Ο τύπος του αποτελέσματος: ακέραιος αριθμός (-1, 0 ή 1)."""
    return type(call_key_direction(arguments)).__name__


# ---- Άσκηση 2: Paddle

def new_paddle(y=230, speed=200, top=60, bottom=480):
    """Φτιάχνει μια ρακέτα 14 x 80 στη θέση x = 24."""
    return exercises.Paddle(24, y, 14, 80, speed, top, bottom)


def paddle_start(unused):
    """Οι ιδιότητες μιας νέας ρακέτας, με τη σειρά x, y, width, height, speed, top, bottom, score."""
    paddle = exercises.Paddle(24, 230, 14, 80, 360, 60, 480)
    return paddle.x, paddle.y, paddle.width, paddle.height, paddle.speed, paddle.top, paddle.bottom, paddle.score


def two_paddles(unused):
    """Δύο ρακέτες: η καθεμία κρατά τις δικές της τιμές."""
    first = exercises.Paddle(24, 100, 14, 80, 200, 60, 480)
    second = exercises.Paddle(602, 300, 20, 100, 150, 70, 470)
    return first.x, first.y, first.height, second.x, second.y, second.height, second.speed


def moved_y(arguments):
    """Το y μετά από μία κλήση της move. Τα arguments είναι (direction, dt, αρχικό y)."""
    direction, dt, y = arguments
    paddle = new_paddle(y)
    paddle.move(direction, dt)
    return round(paddle.y, 6)


def move_result(unused):
    """Η move δεν επιστρέφει τίποτα. Ελέγχουμε και ότι δεν αλλάζει το x."""
    paddle = new_paddle()
    result = paddle.move(1, 0.1)
    return result, paddle.x


def move_uses_own_limits(unused):
    """Η move χρησιμοποιεί τα top, bottom και height της ίδιας της ρακέτας."""
    paddle = exercises.Paddle(0, 20, 10, 50, 100, 0, 200)
    paddle.move(-1, 10)
    at_top = paddle.y
    paddle.move(1, 10)
    return at_top, paddle.y


def move_uses_own_speed(unused):
    """Η ταχύτητα είναι ιδιότητα του αντικειμένου: ρακέτες με άλλη ταχύτητα κινούνται αλλιώς."""
    slow = exercises.Paddle(24, 100, 14, 80, 100, 60, 480)
    fast = exercises.Paddle(24, 100, 14, 80, 300, 60, 480)
    slow.move(1, 1)
    fast.move(1, 1)
    return slow.y, fast.y


def move_is_independent(unused):
    """Αν κινήσουμε τη μία ρακέτα, η άλλη μένει στη θέση της."""
    first = new_paddle()
    second = new_paddle()
    first.move(1, 0.5)
    return round(first.y, 6), second.y


def center_value(y):
    return round(new_paddle(y).center_y(), 6)


def center_after_move(unused):
    """Η center_y χρησιμοποιεί την τρέχουσα θέση, όχι την αρχική."""
    paddle = new_paddle(100)
    paddle.move(1, 0.5)
    return round(paddle.center_y(), 6)


def box_value(y):
    return new_paddle(y).box()


def box_type(unused):
    return type(new_paddle().box()).__name__


def box_after_move(unused):
    paddle = new_paddle(100)
    paddle.move(1, 0.5)
    return paddle.box()


def points_of(unused):
    """Δύο add_point στην πρώτη ρακέτα, κανένα στη δεύτερη. Η add_point δεν επιστρέφει τίποτα."""
    first = new_paddle()
    second = new_paddle()
    result = first.add_point()
    first.add_point()
    return first.score, second.score, result


# ---- Άσκηση 3: rebound_vy

def call_rebound(arguments):
    ball_y, paddle_center, paddle_height, max_vy = arguments
    return round(exercises.rebound_vy(ball_y, paddle_center, paddle_height, max_vy), 6)


# ---- Άσκηση 4: scorer

def call_scorer(arguments):
    ball_x, radius, width = arguments
    return exercises.scorer(ball_x, radius, width)


def scorer_type(arguments):
    """Ο τύπος του αποτελέσματος: κείμενο όταν κάποιος παίρνει πόντο, NoneType όταν κανείς."""
    return type(call_scorer(arguments)).__name__


print("Άσκηση 1 (κύκλος 1): key_direction")
for arguments, expected in (
        ((False, False), 0),
        ((True, False), -1),
        ((False, True), 1),
        ((True, True), 0),
):
    run_check(f"key_direction{arguments} -> {expected}", call_key_direction, arguments, expected)
run_check("το αποτέλεσμα της key_direction είναι ακέραιος αριθμός", key_direction_type, (True, False), "int")

print("Άσκηση 2 (κύκλος 2): Paddle")
run_check("οι ιδιότητες μιας νέας ρακέτας (το score ξεκινά από 0)", paddle_start, None, (24, 230, 14, 80, 360, 60, 480, 0))
run_check("κάθε ρακέτα κρατά τις δικές της τιμές", two_paddles, None, (24, 100, 80, 602, 300, 100, 150))
for arguments, expected in (
        ((1, 0.5, 230), 330.0),
        ((-1, 0.25, 230), 180.0),
        ((0, 1, 230), 230),
        ((1, 0.05, 230), 240.0),
        ((-1, 1, 100), 60),
        ((-1, 0.1, 65), 60),
        ((1, 1, 350), 400),
        ((1, 0.1, 395), 400),
):
    run_check(f"move: direction, dt, y = {arguments} -> y = {expected}", moved_y, arguments, expected)
run_check("η move δεν επιστρέφει τίποτα και δεν αλλάζει το x", move_result, None, (None, 24))
run_check("η move χρησιμοποιεί τα top και bottom της ρακέτας", move_uses_own_limits, None, (0, 150))
run_check("η move χρησιμοποιεί την ταχύτητα της ρακέτας", move_uses_own_speed, None, (200.0, 400.0))
run_check("η move μετακινεί μόνο τη ρακέτα που καλείται", move_is_independent, None, (330.0, 230))
run_check("center_y: y = 100 -> 140.0", center_value, 100, 140.0)
run_check("center_y: y = 100.5 -> 140.5", center_value, 100.5, 140.5)
run_check("η center_y χρησιμοποιεί την τρέχουσα θέση", center_after_move, None, 240.0)
run_check("box: y = 100 -> (24, 100, 14, 80)", box_value, 100, (24, 100, 14, 80))
run_check("box: y = 100.4 -> το y στρογγυλοποιείται προς τα κάτω", box_value, 100.4, (24, 100, 14, 80))
run_check("box: y = 100.6 -> το y στρογγυλοποιείται προς τα πάνω", box_value, 100.6, (24, 101, 14, 80))
run_check("το αποτέλεσμα της box είναι πλειάδα", box_type, None, "tuple")
run_check("η box χρησιμοποιεί την τρέχουσα θέση", box_after_move, None, (24, 200, 14, 80))
run_check("add_point: δύο πόντοι στην πρώτη ρακέτα, κανένας στη δεύτερη, χωρίς επιστροφή τιμής", points_of, None, (2, 0, None))

print("Άσκηση 3 (κύκλος 3): rebound_vy")
for arguments, expected in (
        ((270, 270, 80, 280), 0.0),
        ((250, 270, 80, 280), -140.0),
        ((290, 270, 80, 280), 140.0),
        ((230, 270, 80, 280), -280.0),
        ((310, 270, 80, 280), 280.0),
        ((500, 270, 80, 280), 280.0),
        ((100, 270, 80, 280), -280.0),
        ((260, 270, 100, 200), -40.0),
        ((115, 100, 60, 300), 150.0),
        ((150, 100, 60, 300), 300.0),
        ((270, 270, 80, 0), 0.0),
):
    run_check(f"rebound_vy{arguments} -> {expected}", call_rebound, arguments, expected)

print("Άσκηση 4 (κύκλος 4): scorer")
for arguments, expected in (
        ((320, 10, 640), None),
        ((0, 10, 640), None),
        ((640, 10, 640), None),
        ((-10, 10, 640), None),
        ((650, 10, 640), None),
        ((-10.5, 10, 640), "right"),
        ((-11, 10, 640), "right"),
        ((-500, 10, 640), "right"),
        ((650.5, 10, 640), "left"),
        ((651, 10, 640), "left"),
        ((700, 10, 640), "left"),
        ((-1, 0, 100), "right"),
        ((100, 0, 100), None),
        ((101, 0, 100), "left"),
):
    run_check(f"scorer{arguments} -> {expected!r}", call_scorer, arguments, expected)
run_check("όταν κανείς δεν παίρνει πόντο, το αποτέλεσμα είναι None", scorer_type, (320, 10, 640), "NoneType")
run_check("όταν κάποιος παίρνει πόντο, το αποτέλεσμα είναι κείμενο", scorer_type, (-20, 10, 640), "str")

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
