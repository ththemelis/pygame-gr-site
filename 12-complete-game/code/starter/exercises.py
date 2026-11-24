"""Ασκήσεις του Μαθήματος 12 (καταστάσεις, κουμπιά, ένταση του ήχου και ρεκόρ).

Γράψε τον κώδικα στη θέση κάθε γραμμής `raise NotImplementedError` (και τον πίνακα TRANSITIONS).
Έλεγχος:  python check_exercises.py

Οι ασκήσεις δεν ανοίγουν παράθυρο. Η Button δουλεύει με ένα Rect της pygame και ζωγραφίζεται σε μια κανονική επιφάνεια (Surface),
που τη φτιάχνει ο έλεγχος. Οι συναρτήσεις του ρεκόρ δουλεύουν με πραγματικά αρχεία, σε έναν προσωρινό φάκελο.
"""
import pygame

MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game over"

BUTTON_WIDTH = 260
BUTTON_HEIGHT = 50
WHITE = (245, 245, 245)
BUTTON_COLOR = (36, 54, 104)
BUTTON_HOVER_COLOR = (62, 98, 176)
BUTTON_BORDER_COLOR = (200, 210, 235)

# Κύκλος 1. Ο πίνακας μεταβάσεων: (κατάσταση, ενέργεια) -> νέα κατάσταση. Γράψε εδώ τις επτά μεταβάσεις της προδιαγραφής.
TRANSITIONS = {}


def next_state(state, action):
    """Κύκλος 1. Η νέα κατάσταση μετά από μια ενέργεια, σύμφωνα με τον πίνακα TRANSITIONS.

    Οι καταστάσεις είναι MENU, PLAYING, PAUSED και GAME_OVER, και οι ενέργειες οι συμβολοσειρές «play», «pause», «resume», «menu» και «lose».
    Οι μεταβάσεις είναι επτά: από το MENU το «play» πηγαίνει στο PLAYING· από το PLAYING το «pause» στο PAUSED και το «lose» στο GAME_OVER·
    από το PAUSED το «resume» στο PLAYING και το «menu» στο MENU· από το GAME_OVER το «play» στο PLAYING και το «menu» στο MENU.
    Όποια ενέργεια δεν ισχύει στην κατάσταση που βρισκόμαστε (ή δεν υπάρχει καθόλου) αφήνει την κατάσταση ίδια.
    Παραδείγματα: next_state(MENU, "play") -> PLAYING,  next_state(MENU, "pause") -> MENU,  next_state(PAUSED, "menu") -> MENU
    """
    raise NotImplementedError


class Button:
    """Κύκλος 2. Ένα κουμπί του μενού.

    Η Button(text, center, action) δέχεται το κείμενο του κουμπιού, το κέντρο του (x, y) και την ενέργεια που ζητά όταν πατηθεί.
    Έχει τις ιδιότητες text, action, rect και hovered. Το rect είναι ένα Rect με πλάτος BUTTON_WIDTH, ύψος BUTTON_HEIGHT και
    κέντρο το center. Η hovered είναι στην αρχή False.
    """

    def __init__(self, text, center, action):
        raise NotImplementedError

    def update(self, position):
        """Θυμάται στη hovered αν το σημείο position = (x, y) είναι μέσα στο rect. Δεν επιστρέφει τιμή."""
        raise NotImplementedError

    def is_clicked(self, position):
        """True αν το σημείο position = (x, y) είναι μέσα στο rect, αλλιώς False. Δεν αλλάζει τη hovered."""
        raise NotImplementedError

    def draw(self, surface, font):
        """Ζωγραφίζει το κουμπί: γέμισμα (πιο φωτεινό όταν το ποντίκι είναι πάνω του), περίγραμμα και το κείμενο στο κέντρο. Είναι έτοιμη."""
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BUTTON_BORDER_COLOR, self.rect, 2)
        image = font.render(self.text, True, WHITE)
        surface.blit(image, image.get_rect(center=self.rect.center))


def change_volume(volume, step):
    """Κύκλος 3. Η νέα ένταση του ήχου: το άθροισμα volume + step, ανάμεσα στο 0.0 και στο 1.0, στρογγυλοποιημένο στο ένα
    δεκαδικό ψηφίο (για να μη μαζεύονται δεκαδικά σφάλματα, όπως το 0.30000000000000004).
    Παραδείγματα: change_volume(0.5, 0.1) -> 0.6,  change_volume(0.2, 0.1) -> 0.3,  change_volume(1.0, 0.1) -> 1.0,
    change_volume(0.0, -0.1) -> 0.0
    """
    raise NotImplementedError


def volume_text(volume, muted):
    """Κύκλος 3. Το κείμενο που δείχνει την ένταση του ήχου.

    Για volume = 0.7 είναι «Ήχος: 70%»: το ποσοστό στρογγυλοποιείται στον πλησιέστερο ακέραιο. Όταν ο ήχος είναι κλειστός
    (muted True), το κείμενο είναι «Ήχος: κλειστός», όποια κι αν είναι η ένταση.
    Παραδείγματα: volume_text(0.7, False) -> 'Ήχος: 70%',  volume_text(0.0, False) -> 'Ήχος: 0%',  volume_text(0.7, True) -> 'Ήχος: κλειστός'
    """
    raise NotImplementedError


def read_record(path):
    """Κύκλος 4. Το ρεκόρ που είναι γραμμένο στο αρχείο path, ως ακέραιος.

    Αν το αρχείο δεν υπάρχει, ή δεν περιέχει ακέραιο αριθμό, ή ο αριθμός είναι αρνητικός, επιστρέφει 0.
    Παραδείγματα (περιεχόμενο του αρχείου -> αποτέλεσμα): «25» -> 25,  «abc» -> 0,  «-3» -> 0,  αρχείο που λείπει -> 0
    """
    raise NotImplementedError


def update_record(path, score):
    """Κύκλος 4. Αν οι πόντοι score είναι περισσότεροι από το ρεκόρ του αρχείου path, γράφει το score στο αρχείο (σβήνοντας ό,τι
    υπήρχε) και επιστρέφει True. Αλλιώς δεν αλλάζει το αρχείο και επιστρέφει False. Για το ρεκόρ του αρχείου χρησιμοποίησε τη read_record.
    Παραδείγματα: αρχείο με «10» και score 12 -> γράφει «12» και επιστρέφει True·  αρχείο με «10» και score 10 -> επιστρέφει False
    """
    raise NotImplementedError
