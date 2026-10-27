"""Η λογική του παιχνιδιού χωρίς pygame: οι καταστάσεις, ο πίνακας μεταβάσεων και μικρές συναρτήσεις.

Ό,τι γράφετε εδώ δοκιμάζεται χωρίς παράθυρο με το check_logic.py. Όσα περισσότερα από τα «πρέπει να ισχύει κάτι» του
παιχνιδιού σας βάλετε σε συναρτήσεις αυτού του αρχείου (αντί μέσα στον βρόχο του game.py), τόσο πιο εύκολα τα δοκιμάζετε."""

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game over"

# Ο πίνακας μεταβάσεων: (κατάσταση, ενέργεια) -> νέα κατάσταση. Ό,τι δεν υπάρχει εδώ δεν αλλάζει την κατάσταση.
TRANSITIONS = {
    (MENU, "play"): PLAYING,
    (PLAYING, "lose"): GAME_OVER,
    (PLAYING, "menu"): MENU,
    (GAME_OVER, "play"): PLAYING,
    (GAME_OVER, "menu"): MENU,
}


def next_state(state, action):
    """Η νέα κατάσταση μετά από μια ενέργεια. Αν η ενέργεια δεν αλλάζει κάτι σε αυτή την κατάσταση, επιστρέφει την ίδια."""
    return TRANSITIONS.get((state, action), state)


def clamp(value, low, high):
    """Η τιμή value, αλλά όχι μικρότερη από το low και όχι μεγαλύτερη από το high."""
    return max(low, min(high, value))


def move(value, direction, speed, dt, low, high):
    """Η νέα τιμή μιας συντεταγμένης: κινείται κατά direction (-1, 0 ή 1) με ταχύτητα speed για χρόνο dt, αλλά μένει ανάμεσα στο low και στο high."""
    return clamp(value + direction * speed * dt, low, high)


def new_game(x, y):
    """Τα δεδομένα ενός νέου παιχνιδιού: ο παίκτης στη θέση (x, y), ο χρόνος και οι πόντοι στο μηδέν."""
    return {"x": x, "y": y, "time": 0.0, "score": 0}
