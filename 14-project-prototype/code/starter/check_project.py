"""Αυτοέλεγχος παράδοσης του project.

Τρέξε στον φάκελο του project σας:  python check_project.py

Ελέγχει ότι υπάρχουν τα αρχεία, ότι ο κώδικας έχει σωστή σύνταξη, ότι το παιχνίδι τρέχει χωρίς σφάλμα (το δοκιμάζει με
πλήκτρα και κλικ, χωρίς να ανοίξει παράθυρο), ότι περνούν οι δοκιμές της λογικής, ότι το README έχει τις ενότητες του
και ότι δεν έμειναν προσωρινά κομμάτια του προτύπου. Δεν χρειάζεται να διαβάσεις ή να αλλάξεις αυτό το αρχείο.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

GAME_FILE = "game.py"
LOGIC_FILE = "logic.py"
TEST_FILE = "check_logic.py"
README_FILE = "README.md"
README_SECTIONS = ("Πώς παίζεται", "Χειρισμός", "Μέλη και ρόλοι", "Πηγές και βοήθεια")
DEFAULT_TITLE = "Το παιχνίδι μας"      # ο τίτλος του προτύπου
TEMPLATE_TESTS = 18                    # οι δοκιμές που έχει ήδη το check_logic.py του προτύπου
LEFTOVER = "# ΣΒΗΣΤΕ ΤΟ"               # το σχόλιο που έχουν τα προσωρινά κομμάτια του προτύπου
PLACEHOLDER = "ΣΥΜΠΛΗΡΩΣΤΕ"            # το κείμενο που έχει το πρότυπο του README εκεί που περιμένει δικό σας κείμενο
SCRIPT_FRAMES = 300                    # πόσα καρέ «παίζει» ο έλεγχος πριν κλείσει το παράθυρο
TIMEOUT = int(os.environ.get("CHECK_PROJECT_TIMEOUT", "40"))      # δευτερόλεπτα (ο διδάσκων μπορεί να το αλλάξει με τη μεταβλητή περιβάλλοντος CHECK_PROJECT_TIMEOUT)

# ---- Το παιχνίδι τρέχει μέσα σε δεύτερη διεργασία (τη δοκιμή την κάνει η συνάρτηση child)


def child(game_path):
    """Τρέχει το παιχνίδι χωρίς οθόνη και ήχο, με πλήκτρα που κρατιούνται, πλήκτρα που πατιούνται και κλικ του ποντικιού.

    Δεν την καλείς εσύ: τη χρησιμοποιεί ο έλεγχος. Τυπώνει γραμμές που αρχίζουν με @@ και τις διαβάζει ο έλεγχος.
    Κωδικός εξόδου: 0 όταν το παιχνίδι έκλεισε σωστά, 2 όταν σταμάτησε με σφάλμα, 3 όταν δεν έκλεισε ποτέ."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import runpy
    import traceback

    import pygame

    state = {"frame": 0, "after": 0, "flips": 0, "caption": "", "mouse": (320, 240)}
    timers = {}
    cycle_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,
                  pygame.K_p, pygame.K_m, pygame.K_q, pygame.K_r, pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3]
    held_keys = [(pygame.K_LEFT, pygame.K_a), (pygame.K_RIGHT, pygame.K_d), (pygame.K_UP, pygame.K_w), (pygame.K_DOWN, pygame.K_s),
                 (pygame.K_SPACE, pygame.K_RIGHT)]

    def key_event(kind, key):
        return pygame.event.Event(kind, key=key, mod=0, unicode=chr(key) if 32 <= key < 127 else "", scancode=0)

    def scripted_events(frame):
        events = []
        if frame % 25 in (4, 5):
            events.append(key_event(pygame.KEYDOWN, pygame.K_SPACE if frame % 25 == 4 else pygame.K_RETURN))
            events.append(key_event(pygame.KEYUP, pygame.K_SPACE if frame % 25 == 4 else pygame.K_RETURN))
        if frame % 3 == 0:
            key = cycle_keys[(frame // 3) % len(cycle_keys)]
            events.append(key_event(pygame.KEYDOWN, key))
            events.append(key_event(pygame.KEYUP, key))
        if frame == 6:
            state["mouse"] = (320, 240)
        elif frame % 7 == 3:
            index = frame // 7
            state["mouse"] = (40 + (index % 8) * 80, 60 + ((index // 8) % 4) * 70)
        if frame == 6 or frame % 7 == 3:
            events.append(pygame.event.Event(pygame.MOUSEMOTION, pos=state["mouse"], rel=(1, 1), buttons=(0, 0, 0)))
            events.append(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=state["mouse"], button=1))
            events.append(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=state["mouse"], button=1))
        now = frame * 16
        for event_type, timer in list(timers.items()):
            if now >= timer[1]:
                events.append(timer[2] if isinstance(timer[2], pygame.event.Event) else pygame.event.Event(event_type))
                timer[1] = now + timer[0]
        return events

    def fake_event_get(*arguments, **options):
        state["frame"] += 1
        if state["frame"] <= SCRIPT_FRAMES:
            return scripted_events(state["frame"])
        state["after"] += 1
        if state["after"] > 30:
            print("@@NOQUIT", flush=True)
            os._exit(3)
        return [pygame.event.Event(pygame.QUIT)]

    class Pressed:
        def __init__(self, keys):
            self.keys = keys

        def __getitem__(self, key):
            return key in self.keys

    def fake_get_pressed():
        return Pressed(held_keys[(state["frame"] // 20) % len(held_keys)])

    class FakeClock:
        def tick(self, framerate=0):
            return 16

        def tick_busy_loop(self, framerate=0):
            return 16

        def get_fps(self):
            return 60.0

        def get_time(self):
            return 16

        def get_rawtime(self):
            return 16

    def fake_set_timer(event, millis, loops=0):
        event_type = event.type if hasattr(event, "type") else event
        if millis <= 0:
            timers.pop(event_type, None)
        else:
            timers[event_type] = [millis, state["frame"] * 16 + millis, event]

    real_flip = pygame.display.flip
    real_update = pygame.display.update
    real_caption = pygame.display.set_caption

    def fake_flip(*arguments):
        state["flips"] += 1
        return real_flip()

    def fake_update(*arguments):
        state["flips"] += 1
        return real_update(*arguments)

    def fake_caption(title, *arguments):
        state["caption"] = str(title)
        return real_caption(title, *arguments)

    def fake_mouse_position():
        return state["mouse"]

    def fake_mouse_pressed(*arguments):
        return (state["frame"] % 10 < 3, False, False)

    def fake_ticks():
        return state["frame"] * 16

    pygame.event.get = fake_event_get
    pygame.key.get_pressed = fake_get_pressed
    pygame.mouse.get_pos = fake_mouse_position
    pygame.mouse.get_pressed = fake_mouse_pressed
    pygame.time.Clock = FakeClock
    pygame.time.get_ticks = fake_ticks
    pygame.time.set_timer = fake_set_timer
    pygame.display.flip = fake_flip
    pygame.display.update = fake_update
    pygame.display.set_caption = fake_caption

    folder = os.path.dirname(os.path.abspath(game_path))
    own_file = os.path.abspath(__file__)
    sys.path.insert(0, folder)
    os.chdir(folder)
    try:
        runpy.run_path(game_path, run_name="__main__")
    except SystemExit as request:
        if request.code not in (None, 0):
            print(f"@@ERROR\tSystemExit\tτο πρόγραμμα έκλεισε με sys.exit({request.code})\t\t0\t{state['frame']}", flush=True)
            os._exit(2)
    except BaseException as error:
        where_file = ""
        where_line = 0
        for item in traceback.extract_tb(error.__traceback__):
            path = os.path.abspath(item.filename)
            if os.path.isabs(item.filename) and os.path.dirname(path) == folder and path != own_file:
                where_file = os.path.basename(path)
                where_line = item.lineno
        message = str(error).replace("\n", " ").replace("\t", " ")
        print(f"@@ERROR\t{type(error).__name__}\t{message}\t{where_file}\t{where_line}\t{state['frame']}", flush=True)
        os._exit(2)
    print(f"@@DONE\t{state['frame']}\t{state['flips']}\t{state['caption']}")


# ---- Οι έλεγχοι

results = {"ok": 0, "wrong": 0, "warning": 0}
LABELS = {"ok": "[ΟΚ]", "wrong": "[ΛΑΘΟΣ]", "warning": "[ΠΡΟΣΟΧΗ]"}


def report(kind, text, details=()):
    """Τυπώνει το αποτέλεσμα ενός ελέγχου και το μετρά."""
    results[kind] += 1
    print(f"  {LABELS[kind]} {text}")
    for line in details:
        print(f"      {line}")


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def child_environment():
    """Το περιβάλλον των δεύτερων διεργασιών: με UTF-8, ώστε να διαβάζονται σωστά τα ελληνικά της εξόδου τους."""
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    return environment


def check_syntax(path):
    """Η σύνταξη ενός αρχείου. Επιστρέφει True αν είναι σωστή."""
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report("wrong", f"Το {path.name} δεν είναι αποθηκευμένο ως UTF-8", ["Άνοιξέ το σε έναν επεξεργαστή κώδικα και αποθήκευσέ το ξανά ως UTF-8."])
        return False
    try:
        compile(source, str(path), "exec")
    except SyntaxError as error:
        report("wrong", f"Σφάλμα σύνταξης στη γραμμή {error.lineno} του {path.name}: {error.msg}")
        return False
    report("ok", f"Το {path.name} έχει σωστή σύνταξη")
    return True


def check_leftovers(folder):
    """Δεν έμειναν προσωρινά κομμάτια του προτύπου και ο τίτλος άλλαξε."""
    found = []
    for name in (GAME_FILE, LOGIC_FILE):
        path = folder / name
        if not path.is_file():
            continue
        for number, line in enumerate(read_text(path).splitlines(), 1):
            if LEFTOVER in line:
                found.append(f"{name}, γραμμή {number}: {line.strip()}")
    if found:
        report("wrong", "Έμειναν προσωρινά κομμάτια του προτύπου (σχόλια «ΣΒΗΣΤΕ ΤΟ»)", found)
    else:
        report("ok", "Δεν έμειναν προσωρινά κομμάτια του προτύπου")


def section_text(text, name):
    """Το κείμενο της ενότητας «## name» του README μέχρι την επόμενη επικεφαλίδα, ή None αν δεν υπάρχει."""
    match = re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.M)
    if match is None:
        return None
    rest = text[match.end():]
    following = re.search(r"^#", rest, re.M)
    return rest[:following.start()] if following else rest


def check_readme(folder):
    path = folder / README_FILE
    if not path.is_file():
        report("wrong", f"Λείπει το {README_FILE}")
        return
    text = read_text(path)
    problems = []
    lines = text.splitlines()
    if len(lines) == 0 or not lines[0].startswith("# ") or len(lines[0].strip()) < 5:
        problems.append("Η πρώτη γραμμή πρέπει να είναι ο τίτλος του παιχνιδιού, με «# » μπροστά")
    for name in README_SECTIONS:
        body = section_text(text, name)
        if body is None:
            problems.append(f"Λείπει η ενότητα «## {name}»")
        elif len(body.strip()) < 10:
            problems.append(f"Η ενότητα «{name}» είναι κενή ή πολύ μικρή")
    if PLACEHOLDER in text:
        problems.append(f"Έμειναν κομμάτια «{PLACEHOLDER}» του προτύπου: γράψε εκεί το δικό σου κείμενο")
    if problems:
        report("wrong", f"Το {README_FILE} δεν είναι έτοιμο", problems)
    else:
        report("ok", f"Το {README_FILE} έχει τίτλο και όλες τις ενότητες")


def check_run(folder):
    """Τρέχει το παιχνίδι σε δεύτερη διεργασία και αναφέρει σφάλματα, παιχνίδι που δεν κλείνει και τίτλο που δεν άλλαξε."""
    environment = child_environment()
    command = [sys.executable, os.path.abspath(__file__), "--child", str(folder / GAME_FILE)]
    try:
        done = subprocess.run(command, cwd=str(folder), env=environment, stdin=subprocess.DEVNULL, capture_output=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        report("wrong", f"Το παιχνίδι δεν ανταποκρίθηκε σε {TIMEOUT} δευτερόλεπτα",
               ["Ψάξε βρόχο που δεν τελειώνει ποτέ, ή κάτι που περιμένει για πάντα (π.χ. input)."])
        return
    markers = []
    for line in done.stdout.splitlines():
        if line.startswith("@@"):
            markers.append(line.split("\t"))
    if len(markers) == 0:
        tail = done.stderr.strip().splitlines()[-6:]
        report("wrong", f"Το {GAME_FILE} δεν μπόρεσε να ξεκινήσει", tail)
        return
    marker = markers[-1]
    if marker[0] == "@@ERROR":
        kind, message, where_file, where_line, frame = marker[1], marker[2], marker[3], marker[4], marker[5]
        place = f"γραμμή {where_line} του {where_file}" if where_file else "άγνωστη γραμμή"
        moment = f"στο καρέ {frame}" if frame != "0" else "πριν ξεκινήσει ο βρόχος του παιχνιδιού"
        report("wrong", "Το παιχνίδι σταμάτησε με σφάλμα", [f"{kind}: {message}", f"{place}, {moment}"])
    elif marker[0] == "@@NOQUIT":
        report("wrong", "Το παιχνίδι δεν κλείνει όταν έρχεται το συμβάν pygame.QUIT",
               ["Ο βρόχος πρέπει να τελειώνει όταν ο παίκτης κλείνει το παράθυρο (η ενέργεια «quit»)."])
    elif marker[0] == "@@DONE":
        frames, flips, caption = int(marker[1]), int(marker[2]), marker[3]
        if flips == 0:
            report("wrong", "Το παιχνίδι δεν ζωγράφισε τίποτα (δεν κλήθηκε η pygame.display.flip)")
        else:
            report("ok", f"Το παιχνίδι έτρεξε {frames} καρέ με πλήκτρα και κλικ, χωρίς σφάλμα, και έκλεισε σωστά")
        if caption == DEFAULT_TITLE:
            report("wrong", f"Ο τίτλος του παραθύρου είναι ακόμη «{DEFAULT_TITLE}»: άλλαξε τη σταθερά TITLE")
        elif caption != "":
            report("ok", f"Ο τίτλος του παραθύρου είναι «{caption}»")


def check_logic(folder):
    """Περνούν οι δοκιμές του check_logic.py και έχετε προσθέσει δικές σας."""
    path = folder / TEST_FILE
    if not path.is_file():
        report("warning", f"Δεν υπάρχει το {TEST_FILE}: δεν δοκιμάστηκε η λογική του παιχνιδιού")
        return
    try:
        done = subprocess.run([sys.executable, str(path)], cwd=str(folder), env=child_environment(), stdin=subprocess.DEVNULL, capture_output=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        report("wrong", f"Το {TEST_FILE} δεν τελείωσε σε {TIMEOUT} δευτερόλεπτα")
        return
    if done.returncode != 0:
        failing = []
        for line in done.stdout.splitlines():
            if line.startswith("  [ΛΑΘΟΣ]"):
                failing.append(line.strip())
        report("wrong", f"Δεν περνούν όλες οι δοκιμές του {TEST_FILE}", failing[:6] or done.stdout.splitlines()[-4:] + done.stderr.splitlines()[-4:])
        return
    match = re.search(r"ΟΛΑ ΟΚ: (\d+) από", done.stdout)
    count = int(match.group(1)) if match else 0
    report("ok", f"Περνούν όλες οι δοκιμές του {TEST_FILE} ({count})")
    if count <= TEMPLATE_TESTS:
        report("warning", f"Το {TEST_FILE} έχει μόνο τις δοκιμές του προτύπου: πρόσθεσε παραδείγματα για τις δικές σας συναρτήσεις")


def main(folder):
    print(f"Έλεγχος του project στον φάκελο {folder}")
    game = folder / GAME_FILE
    logic = folder / LOGIC_FILE
    print("Αρχεία")
    syntax_ok = True
    for path in (game, logic):
        if not path.is_file():
            report("wrong", f"Λείπει το {path.name}")
            syntax_ok = False
        elif not check_syntax(path):
            syntax_ok = False
    check_leftovers(folder)
    print("Το παιχνίδι")
    if syntax_ok:
        check_run(folder)
    else:
        report("wrong", "Δεν δοκιμάστηκε η εκτέλεση, γιατί λείπει ή έχει σφάλμα σύνταξης κάποιο αρχείο")
    print("Η λογική")
    check_logic(folder)
    print("Το README")
    check_readme(folder)
    print()
    if results["wrong"] == 0:
        extra = f" ({results['warning']} προσοχές)" if results["warning"] else ""
        print(f"ΟΛΑ ΟΚ: {results['ok']} έλεγχοι πέρασαν{extra}.")
        return 0
    print(f"Πέρασαν {results['ok']} έλεγχοι. Λάθος: {results['wrong']}. Διόρθωσέ τα και τρέξε ξανά.")
    return 1


if len(sys.argv) > 2 and sys.argv[1] == "--child":
    child(sys.argv[2])
    sys.exit(0)
sys.exit(main(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()))
