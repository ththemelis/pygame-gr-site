"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 8.

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


# ---- Άσκηση 1: positions

def call_positions(arguments):
    start, speed, count = arguments
    return exercises.positions(start, speed, count)


def positions_shape(arguments):
    """Ο τύπος του αποτελέσματος, το πλήθος των θέσεων και η τελευταία θέση."""
    result = call_positions(arguments)
    if type(result).__name__ != "list":
        return f"το αποτέλεσμα είναι {type(result).__name__}, όχι list"
    if len(result) == 0:
        return 0, None
    return len(result), result[-1]


# ---- Άσκηση 2: bounce

def call_bounce(arguments):
    position, speed, low, high = arguments
    return exercises.bounce(position, speed, low, high)


def bounce_type(arguments):
    """Ο τύπος του αποτελέσματος: το ζεύγος (θέση, ταχύτητα) είναι πλειάδα, όπως στο παιχνίδι."""
    return type(call_bounce(arguments)).__name__


def bounce_simulation(arguments):
    """100 καρέ: σε κάθε καρέ η θέση αυξάνεται κατά την ταχύτητα και μετά καλείται η bounce.

    Επιστρέφει αν η θέση έμεινε πάντα μέσα στα όρια, ποιες ταχύτητες εμφανίστηκαν και πόσες φορές άλλαξε φορά.
    """
    position, speed, low, high = arguments
    inside = True
    speeds = set()
    turns = 0
    for frame in range(100):
        position += speed
        old_speed = speed
        position, speed = exercises.bounce(position, speed, low, high)
        if not low <= position <= high:
            inside = False
        if speed != old_speed:
            turns += 1
        speeds.add(speed)
    return inside, sorted(speeds), turns


# ---- Άσκηση 3: points_for

def call_points(distance):
    return exercises.points_for(distance)


def points_type(distance):
    """Ο τύπος των πόντων: ακέραιος αριθμός (όχι 8.0 αλλά 8)."""
    return type(exercises.points_for(distance)).__name__


# ---- Άσκηση 4: first_moving

def make_balls_from(flags):
    """Φτιάχνει τη λίστα των μπαλών (λεξικά) από μια πλειάδα True/False για το κλειδί "frozen"."""
    balls = []
    for frozen in flags:
        balls.append({"x": 100, "y": 130, "speed": 180, "frozen": frozen, "points": 0})
    return balls


def call_first_moving(flags):
    return exercises.first_moving(make_balls_from(flags))


def first_moving_type(flags):
    """Ο τύπος του αποτελέσματος: int όταν βρέθηκε μπάλα, NoneType όταν δεν βρέθηκε."""
    return type(call_first_moving(flags)).__name__


def flags_after_call(flags):
    """Τα "frozen" όλων των μπαλών μετά την κλήση: η first_moving μόνο ψάχνει, δεν αλλάζει τίποτα."""
    balls = make_balls_from(flags)
    exercises.first_moving(balls)
    after = []
    for ball in balls:
        after.append(ball["frozen"])
    return tuple(after)


def freeze_order(flags):
    """Παγώνει τις μπάλες μία μία, όπως το παιχνίδι: ποια πάγωσε πρώτη, ποια δεύτερη κ.ο.κ. (δείκτες)."""
    balls = make_balls_from(flags)
    order = []
    for attempt in range(10):
        index = exercises.first_moving(balls)
        if index is None:
            break
        order.append(index)
        balls[index]["frozen"] = True
    return order


print("Άσκηση 1 (κύκλος 1): positions")
for arguments, expected in (
        ((100, 5, 4), [105, 110, 115, 120]),
        ((50, -20, 3), [30, 10, -10]),
        ((0, 5, 0), []),
        ((0, 0, 3), [0, 0, 0]),
        ((10, 3, 1), [13]),
        ((-5, 2, 3), [-3, -1, 1]),
        ((0, 0.5, 4), [0.5, 1.0, 1.5, 2.0]),
):
    run_check(f"positions{arguments} -> {expected}", call_positions, arguments, expected)
run_check("positions(100, 5, 60): 60 θέσεις, η τελευταία είναι η 400", positions_shape, (100, 5, 60), (60, 400))
run_check("positions(0, -3, 10): 10 θέσεις, η τελευταία είναι η -30", positions_shape, (0, -3, 10), (10, -30))
run_check("positions(7, 2, 0): καμία θέση", positions_shape, (7, 2, 0), (0, None))

print("Άσκηση 2 (κύκλος 2): bounce")
for arguments, expected in (
        ((100, 5, 22, 618), (100, 5)),
        ((630, 5, 22, 618), (618, -5)),
        ((10, -5, 22, 618), (22, 5)),
        ((22, -5, 22, 618), (22, -5)),
        ((618, 5, 22, 618), (618, 5)),
        ((618.5, 5, 22, 618), (618, -5)),
        ((21.9, -300, 22, 618), (22, 300)),
        ((-50, -200, 0, 100), (0, 200)),
        ((150, 30, 0, 100), (100, -30)),
        ((50, 0, 0, 100), (50, 0)),
):
    run_check(f"bounce{arguments} -> {expected}", call_bounce, arguments, expected)
run_check("το αποτέλεσμα της bounce είναι πλειάδα", bounce_type, (100, 5, 22, 618), "tuple")
run_check("100 καρέ με ταχύτητα 30 από το 100 (όρια 22, 618): πάντα μέσα στα όρια, 5 αναπηδήσεις",
          bounce_simulation, (100, 30, 22, 618), (True, [-30, 30], 5))

print("Άσκηση 3 (κύκλος 3): points_for")
for distance, expected in (
        (0, 10), (1, 10), (9, 10), (10, 9), (19, 9), (20, 8), (25, 8), (50, 5), (95, 1), (99, 1),
        (100, 0), (101, 0), (250, 0), (320, 0),
):
    run_check(f"points_for({distance}) -> {expected}", call_points, distance, expected)
run_check("οι πόντοι είναι ακέραιος αριθμός (int), όχι δεκαδικός", points_type, 25, "int")

print("Άσκηση 4 (κύκλος 4): first_moving")
for flags, expected in (
        ((True, False, False), 1),
        ((False, False, False), 0),
        ((True, True, True), None),
        ((), None),
        ((True, True, False), 2),
        ((False, True, True), 0),
        ((True, False, True), 1),
):
    run_check(f"first_moving με frozen = {flags} -> {expected}", call_first_moving, flags, expected)
run_check("όταν βρεθεί μπάλα, το αποτέλεσμα είναι ακέραιος δείκτης (int)", first_moving_type, (True, False), "int")
run_check("όταν όλες είναι παγωμένες, το αποτέλεσμα είναι None", first_moving_type, (True, True), "NoneType")
run_check("η first_moving δεν αλλάζει τις μπάλες", flags_after_call, (True, False, False), (True, False, False))
run_check("παγώνουν με τη σειρά 0, 1, 2", freeze_order, (False, False, False), [0, 1, 2])
run_check("παγώνουν με τη σειρά 1, 3 (η 0 και η 2 ήταν ήδη παγωμένες)", freeze_order, (True, False, True, False), [1, 3])

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
