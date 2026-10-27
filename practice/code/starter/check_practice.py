"""Αυτοέλεγχος των ασκήσεων εξάσκησης.

Τρέξε:  python check_practice.py              (όλες οι ασκήσεις)
Ή μόνο ένα μέρος:  python check_practice.py lists     (functions, lists, dicts, tuples ή mixed)

Ελέγχει τις συναρτήσεις του αρχείου practice.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import copy
import sys
import traceback

try:
    import practice
except ImportError:
    print("Δεν βρέθηκε το practice.py. Βάλ' το στον ίδιο φάκελο με αυτό το αρχείο.")
    sys.exit(1)
except SyntaxError as error:
    print(f"Το practice.py έχει συντακτικό λάθος στη γραμμή {error.lineno}: {error.msg}")
    sys.exit(1)

MAX_SHOWN = 3        # πόσες αποτυχημένες δοκιμές δείχνει για κάθε συνάρτηση
results = []         # "passed", "failed" ή "pending": μία τιμή για κάθε δοκιμή
ready = []           # True για κάθε συνάρτηση που πέρασε όλες τις δοκιμές της, αλλιώς False


def call_text(function, args, kwargs):
    """Το κείμενο μιας κλήσης, π.χ. clamp(15, 0, 10)."""
    parts = []
    for argument in args:
        parts.append(repr(argument))
    for key in kwargs:
        parts.append(f"{key}={kwargs[key]!r}")
    return f"{function.__name__}({', '.join(parts)})"


def same(got, expected):
    """Ίσο αποτέλεσμα. Τα True, False και None πρέπει να είναι ακριβώς αυτά (το 1 δεν είναι True)."""
    if expected is None or isinstance(expected, bool):
        return got is expected
    return got == expected


def pending_lines(function, error):
    """Η σημείωση για μια συνάρτηση που δεν είναι έτοιμη: ποια συνάρτηση λείπει, αν η εξαίρεση ξεκίνησε αλλού."""
    frames = traceback.extract_tb(error.__traceback__)
    if frames[-1].name == function.__name__:
        return []
    return [f"(χρησιμοποιεί τη συνάρτηση {frames[-1].name}, που δεν την έχεις γράψει ακόμη)"]


def run_pure(function, entry):
    """Μία δοκιμή συνάρτησης που επιστρέφει τιμή και δεν πρέπει να αλλάζει τα δεδομένα της: (ορίσματα, αναμενόμενο[, ορίσματα με όνομα])."""
    args = entry[0]
    expected = entry[1]
    kwargs = {}
    if len(entry) == 3:
        kwargs = entry[2]
    title = f"{call_text(function, args, kwargs)} -> {expected!r}"
    before = copy.deepcopy(args)
    try:
        got = function(*args, **kwargs)
    except NotImplementedError as error:
        return "pending", pending_lines(function, error)
    except Exception as error:
        return "failed", [title, f"    Προκλήθηκε σφάλμα {type(error).__name__}: {error}"]
    if args != before:
        return "failed", [title, "    Η συνάρτηση άλλαξε τα δεδομένα που πήρε.", f"    πριν:  {before!r}", f"    μετά:  {args!r}"]
    if not same(got, expected):
        return "failed", [title, f"    αναμενόμενο: {expected!r}", f"    πήρα:        {got!r}"]
    return "passed", []


def run_inplace(function, entry):
    """Μία δοκιμή συνάρτησης που αλλάζει το πρώτο της όρισμα (λεξικό): (ορίσματα, τιμή επιστροφής, λεξικό μετά)."""
    args = entry[0]
    expected_result = entry[1]
    expected_state = entry[2]
    title = f"{call_text(function, args, {})} -> επιστρέφει {expected_result!r}, και το λεξικό γίνεται {expected_state!r}"
    try:
        got = function(*args)
    except NotImplementedError as error:
        return "pending", pending_lines(function, error)
    except Exception as error:
        return "failed", [title, f"    Προκλήθηκε σφάλμα {type(error).__name__}: {error}"]
    state = args[0]
    if same(got, expected_result) and state == expected_state:
        return "passed", []
    return "failed", [title,
                      f"    αναμενόμενο: επιστρέφει {expected_result!r}, το λεξικό γίνεται {expected_state!r}",
                      f"    πήρα:        επιστρέφει {got!r}, το λεξικό έγινε {state!r}"]


def run_cases(code, name, table, inplace=False):
    """Τρέχει όλες τις δοκιμές μιας συνάρτησης και γράφει μία γραμμή. Λεπτομέρειες δείχνει μόνο για τα λάθη."""
    function = getattr(practice, name, None)
    if function is None:
        for entry in table:
            results.append("failed")
        ready.append(False)
        print(f"  {code} {name}: [ΛΑΘΟΣ] δεν βρέθηκε η συνάρτηση {name} στο practice.py")
        return
    passed = 0
    pending = 0
    failed_details = []
    note = []
    for entry in table:
        if inplace:
            outcome, lines = run_inplace(function, entry)
        else:
            outcome, lines = run_pure(function, entry)
        results.append(outcome)
        if outcome == "passed":
            passed += 1
        elif outcome == "pending":
            pending += 1
            note = lines
        else:
            failed_details.append(lines)
    if len(failed_details) > 0:
        ready.append(False)
        print(f"  {code} {name}: [ΛΑΘΟΣ] {passed} από {len(table)} δοκιμές")
        for lines in failed_details[:MAX_SHOWN]:
            for line in lines:
                print("      " + line)
        if len(failed_details) > MAX_SHOWN:
            print(f"      ... και άλλες {len(failed_details) - MAX_SHOWN} δοκιμές με λάθος")
    elif pending > 0:
        ready.append(False)
        print(f"  {code} {name}: [ΔΕΝ ΕΙΝΑΙ ΕΤΟΙΜΗ ΑΚΟΜΗ]")
        for line in note:
            print("      " + line)
    else:
        ready.append(True)
        print(f"  {code} {name}: [ΟΚ] {passed} από {len(table)} δοκιμές")


# ---- Μέρος Α: συναρτήσεις

IS_EVEN = (
    ((4,), True), ((7,), False), ((0,), True), ((-3,), False), ((-4,), True), ((1,), False), ((100,), True), ((101,), False),
)
CLAMP = (
    ((15, 0, 10), 10), ((-3, 0, 10), 0), ((5, 0, 10), 5), ((10, 0, 10), 10), ((0, 0, 10), 0), ((7, 7, 7), 7),
    ((-20, -10, -5), -10), ((-7, -10, -5), -7), ((2.5, 0, 1), 1),
)
GRADE_TEXT = (
    ((95,), "άριστα"), ((90,), "άριστα"), ((100,), "άριστα"), ((89,), "πολύ καλά"), ((70,), "πολύ καλά"),
    ((69,), "καλά"), ((50,), "καλά"), ((49,), "χρειάζεσαι εξάσκηση"), ((0,), "χρειάζεσαι εξάσκηση"),
)
REPEAT_TEXT = (
    (("να",), "να-να"), (("ε", 3, ""), "εεε"), (("α", 1), "α"), (("α", 3), "α-α-α"), (("ab", 2, ", "), "ab, ab"),
    (("α", 3), "α+α+α", {"separator": "+"}), (("x",), "x:x:x", {"times": 3, "separator": ":"}),
)
IS_PRIME = (
    ((2,), True), ((3,), True), ((4,), False), ((5,), True), ((9,), False), ((13,), True), ((25,), False),
    ((29,), True), ((97,), True), ((100,), False), ((1,), False), ((0,), False), ((-5,), False),
)


def part_functions():
    print("Μέρος Α — συναρτήσεις")
    run_cases("Α6", "is_even", IS_EVEN)
    run_cases("Α7", "clamp", CLAMP)
    run_cases("Α8", "grade_text", GRADE_TEXT)
    run_cases("Α9", "repeat_text", REPEAT_TEXT)
    run_cases("Α10", "is_prime", IS_PRIME)


# ---- Μέρος Β: λίστες

COUNT_ABOVE = (
    (([5, 12, 7, 20], 6), 3), (([], 3), 0), (([1, 1, 1], 1), 0), (([-5, -1, 4], -3), 2), (([10], 9), 1),
    (([2.5, 3.5], 3), 1), (([6, 6, 7], 6), 1),
)
AVERAGE = (
    (([2, 4, 9],), 5.0), (([7],), 7.0), (([1, 2],), 1.5), (([-3, 3],), 0.0), (([10, 20, 30, 40],), 25.0),
)
WITHOUT_NEGATIVES = (
    (([3, -1, 0, -7, 5],), [3, 0, 5]), (([],), []), (([-2, -9],), []), (([0],), [0]), (([1, 2, 3],), [1, 2, 3]),
    (([-1, -2, 3, -4, 5, 6],), [3, 5, 6]),
)
SECOND_LARGEST = (
    (([5, 9, 7],), 7), (([4, 4, 2],), 4), (([1, 2],), 1), (([10, 3, 3, 8],), 8), (([-1, -5, -3],), -3),
    (([9, 8, 7, 6],), 8), (([2, 2],), 2),
)
REMOVE_DUPLICATES = (
    (([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), []), ((["α", "α", "α"],), ["α"]), (([1, 2, 3],), [1, 2, 3]),
    ((["β", "α", "β", "γ", "α"],), ["β", "α", "γ"]), (([5],), [5]),
)


def part_lists():
    print("Μέρος Β — λίστες")
    run_cases("Β6", "count_above", COUNT_ABOVE)
    run_cases("Β7", "average", AVERAGE)
    run_cases("Β8", "without_negatives", WITHOUT_NEGATIVES)
    run_cases("Β9", "second_largest", SECOND_LARGEST)
    run_cases("Β10", "remove_duplicates", REMOVE_DUPLICATES)


# ---- Μέρος Γ: λεξικά

COUNT_WORDS = (
    ((["α", "β", "α"],), {"α": 2, "β": 1}), (([],), {}), ((["ναι", "ναι", "ναι"],), {"ναι": 3}),
    ((["a", "B", "a"],), {"a": 2, "B": 1}), ((["γ", "β", "α"],), {"γ": 1, "β": 1, "α": 1}),
)
LOOKUP = (
    (({"Άννα": "6970000001", "Νίκη": "6970000002"}, "Νίκη"), "6970000002"), (({}, "Άρης"), "άγνωστο"),
    (({"Άννα": "6970000001"}, "άννα"), "άγνωστο"), (({"Άννα": "6970000001"}, "Άννα"), "6970000001"),
    (({"Άννα": "6970000001"}, "Νίκη"), "άγνωστο"),
)
CART_TOTAL = (
    (({"ψωμί": 2, "γάλα": 3}, {"ψωμί": 1.5, "γάλα": 1.0, "τυρί": 5.0}), 6.0), (({}, {"ψωμί": 1.5}), 0),
    (({"τυρί": 2}, {"ψωμί": 1.5, "τυρί": 5.0}), 10.0), (({"ψωμί": 3}, {"ψωμί": 1.5}), 4.5),
    (({"α": 1, "β": 1}, {"α": 2, "β": 3, "γ": 100}), 5),
)
HIGHEST = (
    (({"Άννα": 40, "Νίκη": 55, "Άρης": 31},), "Νίκη"), (({"Α": 1},), "Α"), (({"α": -5, "β": -2},), "β"),
    (({"x": 9, "y": 3},), "x"), (({"x": 1, "y": 2, "z": 3},), "z"),
)
ADD_POINTS = (
    (({"Άννα": 5}, "Άννα", 3), None, {"Άννα": 8}), (({"Άννα": 8}, "Νίκη", 4), None, {"Άννα": 8, "Νίκη": 4}),
    (({}, "Α", 10), None, {"Α": 10}), (({"Α": 1, "Β": 2}, "Β", 0), None, {"Α": 1, "Β": 2}),
    (({"Α": 0}, "Α", -2), None, {"Α": -2}),
)
GROUP_BY_LENGTH = (
    ((["α", "βγ", "δ"],), {1: ["α", "δ"], 2: ["βγ"]}), (([],), {}),
    ((["ναι", "όχι", "ίσως"],), {3: ["ναι", "όχι"], 4: ["ίσως"]}),
    ((["αα", "β", "γγ", "δ"],), {2: ["αα", "γγ"], 1: ["β", "δ"]}),
)


def part_dicts():
    print("Μέρος Γ — λεξικά")
    run_cases("Γ7", "count_words", COUNT_WORDS)
    run_cases("Γ8", "lookup", LOOKUP)
    run_cases("Γ9", "cart_total", CART_TOTAL)
    run_cases("Γ10", "highest", HIGHEST)
    run_cases("Γ11", "add_points", ADD_POINTS, inplace=True)
    run_cases("Γ12", "group_by_length", GROUP_BY_LENGTH)


# ---- Μέρος Δ: πλειάδες

MANHATTAN = (
    (((1, 2), (4, 6)), 7), (((0, 0), (0, 0)), 0), (((-1, -1), (2, 3)), 7), (((4, 6), (1, 2)), 7), (((0, 5), (0, 2)), 3),
    (((3, 3), (3, 9)), 6),
)
SWAP_PAIR = (
    (((1, "α"),), ("α", 1)), ((("x", "y"),), ("y", "x")), (((0, 0),), (0, 0)), (((1, 2),), (2, 1)),
)
SPLIT_NAME = (
    (("Μαρία Παπαδοπούλου",), ("Μαρία", "Παπαδοπούλου")), (("Νίκος Λ",), ("Νίκος", "Λ")),
    (("  Άννα   Κ ",), ("Άννα", "Κ")), (("Άρης Βέλλιος",), ("Άρης", "Βέλλιος")),
)
STATS = (
    (([2, 4, 9],), (2, 9, 5.0)), (([7],), (7, 7, 7.0)), (([-1, 1],), (-1, 1, 0.0)), (([5, 3, 8, 1],), (1, 8, 4.25)),
    (([3, 2, 1],), (1, 3, 2.0)),
)
RICHEST = (
    (([("Άννα", 5), ("Βασίλης", 9), ("Γεωργία", 7)],), ("Βασίλης", 9)), (([("Νίκη", 3)],), ("Νίκη", 3)),
    (([("α", 3), ("β", 3)],), ("α", 3)), (([("α", 9), ("β", 3)],), ("α", 9)),
    (([("α", 1), ("β", 2), ("γ", 3)],), ("γ", 3)), (([("α", -5), ("β", -2)],), ("β", -2)),
)
CLOSEST = (
    (([(0, 0), (5, 5), (2, 3)], (3, 3)), (2, 3)), (([(1, 0), (0, 1)], (0, 0)), (1, 0)), (([(4, 4)], (0, 0)), (4, 4)),
    (([(9, 9), (1, 1), (5, 5)], (6, 6)), (5, 5)), (([(2, 2), (2, 2)], (0, 0)), (2, 2)),
    (([(-3, 0), (2, 0)], (0, 0)), (2, 0)),
)


def part_tuples():
    print("Μέρος Δ — πλειάδες")
    run_cases("Δ5", "manhattan", MANHATTAN)
    run_cases("Δ6", "swap_pair", SWAP_PAIR)
    run_cases("Δ7", "split_name", SPLIT_NAME)
    run_cases("Δ8", "stats", STATS)
    run_cases("Δ9", "richest", RICHEST)
    run_cases("Δ10", "closest", CLOSEST)


# ---- Μέρος Ε: όλα μαζί

ADD_ITEM = (
    (({"σπαθί": 1}, "φίλτρο", 3), None, {"σπαθί": 1, "φίλτρο": 3}),
    (({"σπαθί": 1, "φίλτρο": 3}, "σπαθί"), None, {"σπαθί": 2, "φίλτρο": 3}),
    (({}, "ασπίδα"), None, {"ασπίδα": 1}), (({"α": 2}, "α", 5), None, {"α": 7}),
)
REMOVE_ITEM = (
    (({"σπαθί": 1, "φίλτρο": 3}, "φίλτρο", 2), True, {"σπαθί": 1, "φίλτρο": 1}),
    (({"σπαθί": 1, "φίλτρο": 3}, "σπαθί"), True, {"φίλτρο": 3}),
    (({"σπαθί": 1, "φίλτρο": 3}, "φίλτρο", 5), False, {"σπαθί": 1, "φίλτρο": 3}),
    (({"σπαθί": 1, "φίλτρο": 3}, "ασπίδα"), False, {"σπαθί": 1, "φίλτρο": 3}),
    (({"α": 2}, "α", 2), True, {}), (({}, "α"), False, {}), (({"α": 3}, "α"), True, {"α": 2}),
)
TOTAL_ITEMS = (
    (({"σπαθί": 1, "φίλτρο": 3},), 4), (({},), 0), (({"α": 5},), 5), (({"α": 2, "β": 2, "γ": 2},), 6),
)
AVERAGES = (
    (([("Άννα", [8, 9, 10]), ("Βασίλης", [5, 6])],), {"Άννα": 9.0, "Βασίλης": 5.5}), (([],), {}),
    (([("Νίκη", [10])],), {"Νίκη": 10.0}), (([("α", [1, 2]), ("β", [3, 3, 3])],), {"α": 1.5, "β": 3.0}),
)
BEST_STUDENT = (
    (([("Άννα", [8, 9, 10]), ("Βασίλης", [5, 6])],), ("Άννα", 9.0)), (([("Νίκη", [10])],), ("Νίκη", 10.0)),
    (([("α", [6, 8]), ("β", [7])],), ("α", 7.0)), (([("α", [5]), ("β", [9, 9]), ("γ", [8])],), ("β", 9.0)),
    (([("α", [2]), ("β", [1])],), ("α", 2.0)),
)
WORD_STATS = (
    (("ναι όχι ναι ίσως",), (4, 3, "ναι")), (("Α α β",), (3, 2, "α")), (("β α α β",), (4, 2, "β")),
    (("",), (0, 0, "")), (("α",), (1, 1, "α")), (("Ναι ΝΑΙ όχι",), (3, 2, "ναι")), (("α β γ",), (3, 3, "α")),
)
RANKING = (
    (({"Άννα": [30, 50], "Νίκη": [40], "Άρης": [10, 60, 20]},), ["Άρης", "Άννα", "Νίκη"]),
    (({"Α": [1]},), ["Α"]), (({},), []), (({"α": [3], "β": [1, 2], "γ": [5]},), ["γ", "α", "β"]),
    (({"α": [-1], "β": [-5, -3]},), ["α", "β"]),
)


def part_mixed():
    print("Μέρος Ε — όλα μαζί")
    run_cases("Ε3", "add_item", ADD_ITEM, inplace=True)
    run_cases("Ε4", "remove_item", REMOVE_ITEM, inplace=True)
    run_cases("Ε5", "total_items", TOTAL_ITEMS)
    run_cases("Ε6", "averages", AVERAGES)
    run_cases("Ε7", "best_student", BEST_STUDENT)
    run_cases("Ε8", "word_stats", WORD_STATS)
    run_cases("Ε9", "ranking", RANKING)


PARTS = {"functions": part_functions, "lists": part_lists, "dicts": part_dicts, "tuples": part_tuples, "mixed": part_mixed}

wanted = []
for argument in sys.argv[1:]:
    wanted.append(argument.lower())
if len(wanted) == 0:
    wanted = ["functions", "lists", "dicts", "tuples", "mixed"]
for name in wanted:
    if name not in PARTS:
        print(f"Άγνωστο μέρος «{name}». Διάλεξε ένα από: functions, lists, dicts, tuples, mixed.")
        sys.exit(1)
for name in wanted:
    PARTS[name]()

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
else:
    print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
print(f"Έτοιμες συναρτήσεις: {ready.count(True)} από {len(ready)}.")
sys.exit(0 if failed == 0 and pending == 0 else 1)
