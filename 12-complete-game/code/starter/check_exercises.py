"""Αυτοέλεγχος των ασκήσεων του Μαθήματος 12.

Τρέξε:  python check_exercises.py

Ελέγχει τα περιεχόμενα του αρχείου exercises.py, που πρέπει να βρίσκεται στον ίδιο φάκελο.
Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import os
import sys
import tempfile

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


# ---- Άσκηση 1: next_state

STATES = (exercises.MENU, exercises.PLAYING, exercises.PAUSED, exercises.GAME_OVER)


def call_next_state(arguments):
    state, action = arguments
    return exercises.next_state(state, action)


def transitions_size(unused):
    """Ο πίνακας TRANSITIONS έχει επτά μεταβάσεις. Αν είναι ακόμη κενός, η άσκηση δεν έχει ξεκινήσει."""
    if len(exercises.TRANSITIONS) == 0:
        raise NotImplementedError
    return len(exercises.TRANSITIONS)


def next_state_type(arguments):
    state, action = arguments
    return type(exercises.next_state(state, action)).__name__


# ---- Άσκηση 2: Button

def make_button(arguments):
    text, center, action = arguments
    return exercises.Button(text, center, action)


def button_start(arguments):
    """Οι ιδιότητες text, action, hovered και το κέντρο και το μέγεθος του rect αμέσως μετά τη δημιουργία."""
    button = make_button(arguments)
    return button.text, button.action, button.hovered, button.rect.center, button.rect.size


def button_corner(arguments):
    """Η πάνω αριστερή γωνία του rect."""
    return make_button(arguments).rect.topleft


def button_rect_type(unused):
    return type(make_button(("Παίξε", (320, 250), "play")).rect).__name__


def button_after_update(arguments):
    """Μετά από update στη θέση position: η τιμή της hovered."""
    center, position = arguments
    button = make_button(("Παίξε", center, "play"))
    button.update(position)
    return button.hovered


def button_update_twice(arguments):
    """Το hovered ακολουθεί την τελευταία θέση: πρώτα μέσα, μετά έξω."""
    button = make_button(("Παίξε", (320, 250), "play"))
    button.update((320, 250))
    first = button.hovered
    button.update((0, 0))
    return first, button.hovered


def button_update_returns(unused):
    """Η update δεν επιστρέφει τιμή."""
    button = make_button(("Παίξε", (320, 250), "play"))
    return button.update((320, 250))


def button_clicked(arguments):
    center, position = arguments
    return make_button(("Παίξε", center, "play")).is_clicked(position)


def button_clicked_keeps_hover(unused):
    """Η is_clicked δεν αλλάζει τη hovered: ύστερα από update έξω, η hovered μένει False ακόμη και αν ρωτήσουμε για ένα σημείο μέσα."""
    button = make_button(("Παίξε", (320, 250), "play"))
    button.update((0, 0))
    answer = button.is_clicked((320, 250))
    return answer, button.hovered


def button_clicked_type(unused):
    return type(make_button(("Παίξε", (320, 250), "play")).is_clicked((320, 250))).__name__


def buttons_independent(unused):
    """Δύο κουμπιά είναι ανεξάρτητα: το update του ενός δεν αλλάζει το άλλο."""
    first = make_button(("Παίξε", (320, 250), "play"))
    second = make_button(("Έξοδος", (320, 320), "quit"))
    first.update((320, 250))
    return first.hovered, second.hovered, second.is_clicked((320, 250))


def button_color_at(arguments):
    """Το χρώμα του pixel που βρίσκεται 6 pixel μέσα από την πάνω αριστερή γωνία του κουμπιού, ύστερα από την draw.
    Το pixel είναι μέσα στο γέμισμα, μακριά από το περίγραμμα και το κείμενο."""
    hover = arguments
    pygame.font.init()
    surface = pygame.Surface((640, 480))
    surface.fill((0, 0, 0))
    button = make_button(("Παίξε", (320, 250), "play"))
    if hover:
        button.update((320, 250))
    button.draw(surface, pygame.font.Font(None, 36))
    left, top = button.rect.topleft
    return tuple(surface.get_at((left + 6, top + 6)))[:3]


def button_draws_text(unused):
    """Το κουμπί ζωγραφίζει το κείμενό του: υπάρχουν pixel με το χρώμα του κειμένου μέσα στο ορθογώνιο."""
    pygame.font.init()
    surface = pygame.Surface((640, 480))
    surface.fill((0, 0, 0))
    button = make_button(("Παίξε", (320, 250), "play"))
    button.draw(surface, pygame.font.Font(None, 36))
    count = 0
    for x in range(button.rect.left + 3, button.rect.right - 3):
        for y in range(button.rect.top + 3, button.rect.bottom - 3):
            if tuple(surface.get_at((x, y)))[:3] == exercises.WHITE:
                count += 1
    return count > 30


# ---- Άσκηση 3: change_volume και volume_text

def call_change_volume(arguments):
    volume, step = arguments
    return exercises.change_volume(volume, step)


def change_volume_type(arguments):
    volume, step = arguments
    return type(exercises.change_volume(volume, step)).__name__


def call_volume_text(arguments):
    volume, muted = arguments
    return exercises.volume_text(volume, muted)


def volume_text_type(arguments):
    volume, muted = arguments
    return type(exercises.volume_text(volume, muted)).__name__


# ---- Άσκηση 4: read_record και update_record

def with_file(content, function):
    """Φτιάχνει ένα αρχείο record.txt με το περιεχόμενο content (ή χωρίς αρχείο, αν content είναι None) σε προσωρινό φάκελο
    και καλεί τη function με τη διαδρομή του."""
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "record.txt")
        if content is not None:
            with open(path, "w", encoding="utf-8", newline="") as file:
                file.write(content)
        return function(path)


def read_file(path):
    """Το περιεχόμενο του αρχείου path, ή None αν δεν υπάρχει."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", newline="") as file:
        return file.read()


def call_read_record(content):
    return with_file(content, exercises.read_record)


def read_record_type(content):
    return type(with_file(content, exercises.read_record)).__name__


def call_update_record(arguments):
    """Το αποτέλεσμα της update_record και το περιεχόμενο του αρχείου μετά από αυτήν: (αποτέλεσμα, περιεχόμενο)."""
    content, score = arguments

    def action(path):
        answer = exercises.update_record(path, score)
        return answer, read_file(path)

    return with_file(content, action)


def update_record_type(arguments):
    content, score = arguments

    def action(path):
        return type(exercises.update_record(path, score)).__name__

    return with_file(content, action)


def update_record_twice(arguments):
    """Δύο διαδοχικά παιχνίδια με τους πόντους της λίστας: (αποτελέσματα, τελικό περιεχόμενο)."""
    scores = arguments

    def action(path):
        answers = []
        for score in scores:
            answers.append(exercises.update_record(path, score))
        return tuple(answers), read_file(path)

    return with_file(None, action)


print("Άσκηση 1 (κύκλος 1): next_state")
run_check("ο πίνακας TRANSITIONS έχει 7 μεταβάσεις", transitions_size, None, 7)
for arguments, expected in (
        ((exercises.MENU, "play"), exercises.PLAYING),
        ((exercises.PLAYING, "pause"), exercises.PAUSED),
        ((exercises.PLAYING, "lose"), exercises.GAME_OVER),
        ((exercises.PAUSED, "resume"), exercises.PLAYING),
        ((exercises.PAUSED, "menu"), exercises.MENU),
        ((exercises.GAME_OVER, "play"), exercises.PLAYING),
        ((exercises.GAME_OVER, "menu"), exercises.MENU),
):
    run_check(f"next_state{arguments} -> {expected!r}", call_next_state, arguments, expected)
for state in STATES:
    for action in ("play", "pause", "resume", "menu", "lose"):
        valid = (state, action) in (
            (exercises.MENU, "play"), (exercises.PLAYING, "pause"), (exercises.PLAYING, "lose"), (exercises.PAUSED, "resume"),
            (exercises.PAUSED, "menu"), (exercises.GAME_OVER, "play"), (exercises.GAME_OVER, "menu"))
        if not valid:
            run_check(f"η ενέργεια {action!r} δεν αλλάζει την κατάσταση {state!r}", call_next_state, (state, action), state)
for state in STATES:
    run_check(f"άγνωστη ενέργεια στην κατάσταση {state!r}", call_next_state, (state, "jump"), state)
run_check("το αποτέλεσμα της next_state είναι συμβολοσειρά", next_state_type, (exercises.MENU, "play"), "str")

print("Άσκηση 2 (κύκλος 2): Button")
for arguments, expected in (
        (("Παίξε", (320, 250), "play"), ("Παίξε", "play", False, (320, 250), (260, 50))),
        (("Έξοδος", (320, 320), "quit"), ("Έξοδος", "quit", False, (320, 320), (260, 50))),
        (("Ξανά", (100, 80), "play"), ("Ξανά", "play", False, (100, 80), (260, 50))),
):
    run_check(f"Button{arguments}: text, action, hovered, κέντρο και μέγεθος του rect", button_start, arguments, expected)
run_check("Button στο (320, 250): η πάνω αριστερή γωνία του rect είναι (190, 225)", button_corner, ("Παίξε", (320, 250), "play"), (190, 225))
run_check("Button στο (100, 80): η πάνω αριστερή γωνία του rect είναι (-30, 55)", button_corner, ("Ξανά", (100, 80), "play"), (-30, 55))
run_check("το rect είναι Rect της pygame", button_rect_type, None, "Rect")
for arguments, expected in (
        (((320, 250), (320, 250)), True),
        (((320, 250), (190, 225)), True),         # η πάνω αριστερή γωνία είναι μέσα
        (((320, 250), (449, 274)), True),         # το τελευταίο pixel μέσα (κάτω δεξιά)
        (((320, 250), (189, 250)), False),        # ένα pixel αριστερά από το ορθογώνιο
        (((320, 250), (450, 250)), False),        # η δεξιά πλευρά δεν ανήκει στο ορθογώνιο
        (((320, 250), (320, 224)), False),        # ένα pixel πάνω
        (((320, 250), (320, 275)), False),        # η κάτω πλευρά δεν ανήκει στο ορθογώνιο
        (((320, 250), (0, 0)), False),
        (((320, 250), (639, 479)), False),
):
    center, position = arguments
    run_check(f"update: κουμπί με κέντρο {center}, ποντίκι στο {position}: hovered -> {expected}", button_after_update, arguments, expected)
run_check("η hovered ακολουθεί την τελευταία θέση του ποντικιού: πρώτα μέσα, μετά έξω", button_update_twice, None, (True, False))
run_check("η update δεν επιστρέφει τιμή", button_update_returns, None, None)
for arguments, expected in (
        (((320, 250), (320, 250)), True),
        (((320, 250), (190, 225)), True),
        (((320, 250), (449, 274)), True),
        (((320, 250), (189, 250)), False),
        (((320, 250), (450, 250)), False),
        (((320, 250), (320, 224)), False),
        (((320, 250), (320, 275)), False),
        (((100, 80), (-30, 55)), True),
        (((100, 80), (230, 80)), False),
):
    center, position = arguments
    run_check(f"is_clicked: κουμπί με κέντρο {center}, κλικ στο {position} -> {expected}", button_clicked, arguments, expected)
run_check("η is_clicked δεν αλλάζει τη hovered", button_clicked_keeps_hover, None, (True, False))
run_check("η is_clicked επιστρέφει True ή False (bool)", button_clicked_type, None, "bool")
run_check("δύο κουμπιά είναι ανεξάρτητα", buttons_independent, None, (True, False, False))
run_check("η draw: pixel μέσα στο γέμισμα όταν το ποντίκι δεν είναι πάνω στο κουμπί", button_color_at, False, exercises.BUTTON_COLOR)
run_check("η draw: pixel μέσα στο γέμισμα όταν το ποντίκι είναι πάνω στο κουμπί", button_color_at, True, exercises.BUTTON_HOVER_COLOR)
run_check("η draw ζωγραφίζει το κείμενο του κουμπιού", button_draws_text, None, True)

print("Άσκηση 3 (κύκλος 3): change_volume και volume_text")
for arguments, expected in (
        ((0.5, 0.1), 0.6),
        ((0.2, 0.1), 0.3),         # 0.2 + 0.1 είναι 0.30000000000000004
        ((0.7, 0.1), 0.8),         # 0.7 + 0.1 είναι 0.7999999999999999
        ((0.6, 0.3), 0.9),
        ((0.8, 0.1), 0.9),
        ((0.9, 0.1), 1.0),
        ((1.0, 0.1), 1.0),         # δεν ξεπερνά το 1.0
        ((0.95, 0.1), 1.0),
        ((0.5, -0.1), 0.4),
        ((0.3, -0.1), 0.2),
        ((0.1, -0.1), 0.0),
        ((0.0, -0.1), 0.0),        # δεν πέφτει κάτω από το 0.0
        ((0.5, -0.7), 0.0),
        ((0.5, 0.0), 0.5),
        ((0.5, 0.5), 1.0),
        ((0.26, 0.0), 0.3),        # στρογγυλοποιείται στο ένα δεκαδικό ψηφίο
):
    run_check(f"change_volume{arguments} -> {expected}", call_change_volume, arguments, expected)
run_check("το αποτέλεσμα της change_volume είναι δεκαδικός (float)", change_volume_type, (0.5, 0.1), "float")
for arguments, expected in (
        ((1.0, False), "Ήχος: 100%"),
        ((0.5, False), "Ήχος: 50%"),
        ((0.7, False), "Ήχος: 70%"),
        ((0.3, False), "Ήχος: 30%"),
        ((0.0, False), "Ήχος: 0%"),
        ((0.29, False), "Ήχος: 29%"),     # το int(0.29 * 100) θα έδινε 28
        ((0.05, False), "Ήχος: 5%"),
        ((0.7, True), "Ήχος: κλειστός"),
        ((0.0, True), "Ήχος: κλειστός"),
        ((1.0, True), "Ήχος: κλειστός"),
):
    run_check(f"volume_text{arguments} -> {expected!r}", call_volume_text, arguments, expected)
run_check("το αποτέλεσμα της volume_text είναι συμβολοσειρά", volume_text_type, (0.5, False), "str")

print("Άσκηση 4 (κύκλος 4): read_record και update_record")
for content, expected in (
        (None, 0),                  # το αρχείο δεν υπάρχει
        ("25", 25),
        ("25\n", 25),
        (" 7 ", 7),
        ("007", 7),
        ("0", 0),
        ("1000000", 1000000),
        ("", 0),
        ("abc", 0),
        ("12.5", 0),
        ("3 4", 0),
        ("-3", 0),
):
    description = "το αρχείο λείπει" if content is None else f"το αρχείο έχει το κείμενο {content!r}"
    run_check(f"read_record: {description} -> {expected}", call_read_record, content, expected)
run_check("το αποτέλεσμα της read_record είναι ακέραιος (int)", read_record_type, "25", "int")
for arguments, expected in (
        ((None, 5), (True, "5")),               # δεν υπάρχει ρεκόρ: το αρχείο δημιουργείται
        ((None, 0), (False, None)),             # το 0 δεν είναι ρεκόρ και το αρχείο δεν δημιουργείται
        (("10", 12), (True, "12")),
        (("10", 10), (False, "10")),            # ισοπαλία: δεν είναι νέο ρεκόρ
        (("10", 7), (False, "10")),
        (("10\n", 12), (True, "12")),           # το νέο αρχείο δεν έχει αλλαγή γραμμής
        (("abc", 3), (True, "3")),              # άκυρο περιεχόμενο: ισχύει το 0
        (("-3", 1), (True, "1")),
        (("25", 0), (False, "25")),
        (("5", 1000), (True, "1000")),
):
    content, score = arguments
    description = "χωρίς αρχείο" if content is None else f"αρχείο με το κείμενο {content!r}"
    run_check(f"update_record: {description}, πόντοι {score}: (αποτέλεσμα, περιεχόμενο αρχείου) -> {expected}", call_update_record, arguments, expected)
run_check("το αποτέλεσμα της update_record είναι True ή False (bool)", update_record_type, ("10", 12), "bool")
run_check("δύο παιχνίδια με 4 και 9 πόντους: το ρεκόρ γίνεται 9", update_record_twice, (4, 9), ((True, True), "9"))
run_check("τρία παιχνίδια με 9, 4 και 9 πόντους: μόνο το πρώτο είναι ρεκόρ", update_record_twice, (9, 4, 9), ((True, False, False), "9"))

passed = results.count("passed")
failed = results.count("failed")
pending = results.count("pending")
print()
if failed == 0 and pending == 0:
    print(f"ΟΛΑ ΟΚ: {passed} από {len(results)} δοκιμές.")
    sys.exit(0)
print(f"Πέρασαν {passed} από {len(results)} δοκιμές. Λάθος: {failed}. Δεν είναι έτοιμες ακόμη: {pending}.")
sys.exit(1)
