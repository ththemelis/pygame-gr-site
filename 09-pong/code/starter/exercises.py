"""Ασκήσεις του Μαθήματος 9 (δύο συναρτήσεις, μια κλάση και μια συνάρτηση).

Γράψε τον κώδικα στη θέση κάθε γραμμής `raise NotImplementedError`.
Έλεγχος:  python check_exercises.py

Οι ασκήσεις δεν χρειάζονται pygame: δουλεύεις με αριθμούς, λογικές τιμές και μια κλάση.
"""


def key_direction(up_pressed, down_pressed):
    """Κύκλος 1. Επιστρέφει την κατεύθυνση κίνησης που ζητούν δύο πλήκτρα.

    -1 αν πατιέται ΜΟΝΟ το πάνω πλήκτρο, 1 αν πατιέται ΜΟΝΟ το κάτω, και 0 σε κάθε άλλη περίπτωση
    (κανένα πλήκτρο ή και τα δύο μαζί).
    Παραδείγματα: key_direction(True, False) -> -1,  key_direction(False, True) -> 1,  key_direction(True, True) -> 0
    """
    raise NotImplementedError


class Paddle:
    """Κύκλος 2. Μια ρακέτα του Pong.

    Paddle(x, y, width, height, speed, top, bottom)
        x, y           η θέση της πάνω αριστερής γωνίας
        width, height  το μέγεθος
        speed          η ταχύτητα, σε pixel το δευτερόλεπτο
        top, bottom    τα όρια κίνησης: η πάνω πλευρά της ρακέτας δεν ανεβαίνει πάνω από το top, και η κάτω πλευρά της
                       δεν κατεβαίνει κάτω από το bottom
    Ιδιότητες: x, y, width, height, speed, top, bottom και score (οι πόντοι, με αρχική τιμή 0).
    Κάθε αντικείμενο έχει τις δικές του τιμές.

    Μέθοδοι:
        move(direction, dt)  αλλάζει το y κατά direction * speed * dt (direction: -1 πάνω, 0 ακίνητη, 1 κάτω)
                             και μετά κρατά τη ρακέτα μέσα στα όρια. Δεν επιστρέφει τίποτα.
        center_y()           επιστρέφει το y του κέντρου της ρακέτας (y + height / 2).
        box()                επιστρέφει την πλειάδα (x, y, width, height), με το y στρογγυλοποιημένο στον πλησιέστερο ακέραιο.
        add_point()          αυξάνει το score κατά 1. Δεν επιστρέφει τίποτα.
    """

    def __init__(self, x, y, width, height, speed, top, bottom):
        raise NotImplementedError

    def move(self, direction, dt):
        raise NotImplementedError

    def center_y(self):
        raise NotImplementedError

    def box(self):
        raise NotImplementedError

    def add_point(self):
        raise NotImplementedError


def rebound_vy(ball_y, paddle_center, paddle_height, max_vy):
    """Κύκλος 3. Η κάθετη ταχύτητα της μπάλας μετά το χτύπημα σε ρακέτα.

    Στο κέντρο της ρακέτας δίνει 0. Στην πάνω άκρη δίνει -max_vy και στην κάτω άκρη max_vy. Ανάμεσα, η τιμή αλλάζει
    ανάλογα με την απόσταση από το κέντρο. Αν η μπάλα χτυπά πέρα από τις άκρες, δίνει πάλι -max_vy ή max_vy.
    Παραδείγματα: rebound_vy(270, 270, 80, 280) -> 0.0,  rebound_vy(250, 270, 80, 280) -> -140.0,
    rebound_vy(310, 270, 80, 280) -> 280.0,  rebound_vy(500, 270, 80, 280) -> 280.0
    """
    raise NotImplementedError


def scorer(ball_x, radius, width):
    """Κύκλος 4. Ποιος παίρνει πόντο, όταν η μπάλα (κέντρο ball_x, ακτίνα radius) βγαίνει από παράθυρο πλάτους width.

    Αν η μπάλα έχει βγει ΟΛΟΚΛΗΡΗ από την αριστερή πλευρά (το κέντρο της είναι μικρότερο από -radius), πόντο παίρνει ο
    δεξιός παίκτης: επιστρέφει "right". Αν έχει βγει ολόκληρη από τη δεξιά πλευρά (το κέντρο της είναι μεγαλύτερο από
    width + radius), επιστρέφει "left". Σε κάθε άλλη περίπτωση επιστρέφει None.
    Παραδείγματα: scorer(320, 10, 640) -> None,  scorer(-11, 10, 640) -> "right",  scorer(651, 10, 640) -> "left"
    """
    raise NotImplementedError
