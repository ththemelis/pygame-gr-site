"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 6.

Τρέξε:  python check_exercises.py

Ελέγχει τις κλάσεις και τις συναρτήσεις του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
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


# ---- Άσκηση 1: Point

def point_info(arguments):
    """Φτιάχνει ένα Point και επιστρέφει τις ιδιότητές του και το κείμενο της describe."""
    x, y = arguments
    point = exercises.Point(x, y)
    return point.x, point.y, point.describe()


def two_points(unused):
    """Φτιάχνει δύο Point και επιστρέφει τις ιδιότητες και των δύο: το καθένα πρέπει να κρατά τις δικές του."""
    first = exercises.Point(1, 2)
    second = exercises.Point(5, 6)
    return first.x, first.y, second.x, second.y


def changed_point(unused):
    """Αλλάζει μια ιδιότητα ενός Point και επιστρέφει το κείμενο και των δύο."""
    first = exercises.Point(1, 2)
    second = exercises.Point(5, 6)
    first.x = 99
    return first.describe(), second.describe()


# ---- Άσκηση 2: Stamina

def stamina_start(maximum):
    stamina = exercises.Stamina(maximum)
    return stamina.value, stamina.maximum


def stamina_spend(unused):
    """Τρεις δαπάνες: 4 (αρκεί), 7 (δεν αρκεί), 6 (ακριβώς όσο έμεινε)."""
    stamina = exercises.Stamina(10)
    first = stamina.spend(4)
    after_first = stamina.value
    second = stamina.spend(7)
    after_second = stamina.value
    third = stamina.spend(6)
    return first, after_first, second, after_second, third, stamina.value, stamina.is_empty()


def stamina_rest(unused):
    """Ξεκούραση: μέσα στο όριο και πάνω από το όριο."""
    stamina = exercises.Stamina(10)
    stamina.spend(8)
    stamina.rest(3)
    after_first = stamina.value
    answer = stamina.rest(100)
    return after_first, stamina.value, answer


def stamina_is_empty(unused):
    return exercises.Stamina(5).is_empty(), exercises.Stamina(0).is_empty()


def stamina_independent(unused):
    first = exercises.Stamina(10)
    second = exercises.Stamina(20)
    first.spend(5)
    return first.value, second.value


# ---- Άσκηση 3: make_monster

def monster_description(kind):
    monster = exercises.make_monster(kind)
    if monster is None:
        return None
    return monster.describe()


def monster_is_fighter(kind):
    return isinstance(exercises.make_monster(kind), exercises.Fighter)


def monsters_are_new(kind):
    """Αν χτυπήσουμε το πρώτο αντικείμενο, το δεύτερο που θα ζητήσουμε πρέπει να έχει πλήρη ζωή."""
    first = exercises.make_monster(kind)
    first.health = 1
    second = exercises.make_monster(kind)
    return second.health


# ---- Άσκηση 4: alive_names

def fighters_from(specs):
    fighters = []
    for name, health in specs:
        fighter = exercises.Fighter(name, 10, 5, 1)
        fighter.health = health
        fighters.append(fighter)
    return fighters


def names_of_alive(specs):
    return exercises.alive_names(fighters_from(specs))


def unchanged_after_call(specs):
    """Επιστρέφει το πλήθος των μαχητών και τις ζωές τους μετά την κλήση, για να δούμε αν άλλαξαν."""
    fighters = fighters_from(specs)
    exercises.alive_names(fighters)
    healths = []
    for fighter in fighters:
        healths.append(fighter.health)
    return len(fighters), healths


print("Άσκηση 1 (κύκλος 1): κλάση Point")
for arguments, expected in (((3, 4), (3, 4, "(3, 4)")), ((0, 0), (0, 0, "(0, 0)")), ((-1, 2), (-1, 2, "(-1, 2)"))):
    run_check(f"Point{arguments} -> ιδιότητες και describe {expected}", point_info, arguments, expected)
run_check("δύο αντικείμενα κρατούν τις δικές τους ιδιότητες", two_points, None, (1, 2, 5, 6))
run_check("η αλλαγή μιας ιδιότητας ενός αντικειμένου δεν αλλάζει το άλλο", changed_point, None, ("(99, 2)", "(5, 6)"))

print("Άσκηση 2 (κύκλος 2): κλάση Stamina")
run_check("Stamina(10): ιδιότητες value και maximum στην αρχή", stamina_start, 10, (10, 10))
run_check("spend(4), spend(7), spend(6) σε αντοχή 10", stamina_spend, None, (True, 6, False, 6, True, 0, True))
run_check("rest(3) και rest(100) σε αντοχή 2 από 10", stamina_rest, None, (5, 10, None))
run_check("is_empty: Stamina(5) και Stamina(0)", stamina_is_empty, None, (False, True))
run_check("δύο αντικείμενα Stamina είναι ανεξάρτητα", stamina_independent, None, (5, 20))

print("Άσκηση 3 (κύκλος 3): make_monster")
for kind, expected in (("goblin", "Γκόμπλιν: ζωή 25/25, δύναμη 5, θεραπείες 1"),
                       ("orc", "Ορκ: ζωή 40/40, δύναμη 7, θεραπείες 1"),
                       ("dragon", "Δράκος: ζωή 60/60, δύναμη 9, θεραπείες 1"),
                       ("troll", None), ("", None)):
    run_check(f"make_monster({kind!r}) -> {expected!r}", monster_description, kind, expected)
run_check("το αποτέλεσμα είναι αντικείμενο της κλάσης Fighter", monster_is_fighter, "orc", True)
run_check("κάθε κλήση φτιάχνει ΝΕΟ αντικείμενο (ζωή 25)", monsters_are_new, "goblin", 25)

print("Άσκηση 4 (κύκλος 4): alive_names")
alive_tests = (
    ([], []),
    ([("Α", 10), ("Β", 0), ("Γ", 3)], ["Α", "Γ"]),
    ([("Α", 0), ("Β", 0)], []),
    ([("Ζ", 5), ("Α", 5)], ["Ζ", "Α"]),
)
for specs, expected in alive_tests:
    run_check(f"alive_names για {specs} -> {expected}", names_of_alive, specs, expected)
run_check("η alive_names δεν αλλάζει τη λίστα ούτε τους μαχητές", unchanged_after_call,
          [("Α", 10), ("Β", 0), ("Γ", 3)], (3, [10, 0, 3]))

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
