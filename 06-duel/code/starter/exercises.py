"""Ασκήσεις του Μαθήματος 6.

Γράψε τον κώδικα στη θέση κάθε γραμμής `raise NotImplementedError`. Η κλάση Fighter δίνεται έτοιμη.
Έλεγχος:  python check_exercises.py
"""


class Fighter:
    """Δίνεται έτοιμη (όπως στο Στάδιο 4). Χρησιμοποιείται στις ασκήσεις 3 και 4."""

    def __init__(self, name, health, power, potions):
        self.name = name
        self.health = health
        self.max_health = health
        self.power = power
        self.potions = potions

    def describe(self):
        return f"{self.name}: ζωή {self.health}/{self.max_health}, δύναμη {self.power}, θεραπείες {self.potions}"

    def is_alive(self):
        return self.health > 0


class Point:
    """Κύκλος 1. Ένα σημείο (x, y).

    Point(x, y): αποθηκεύει τις ιδιότητες x και y.
    describe(): επιστρέφει κείμενο της μορφής "(3, 4)".
    Κάθε αντικείμενο έχει τα δικά του x και y.
    """

    def __init__(self, x, y):
        raise NotImplementedError

    def describe(self):
        raise NotImplementedError


class Stamina:
    """Κύκλος 2. Η αντοχή ενός μαχητή, από 0 έως maximum.

    Stamina(maximum): ιδιότητες maximum και value. Στην αρχή το value είναι ίσο με το maximum.
    spend(amount): αν το value είναι τουλάχιστον amount, το μειώνει κατά amount και επιστρέφει True.
        Αλλιώς δεν αλλάζει τίποτα και επιστρέφει False.
    rest(amount): αυξάνει το value κατά amount, χωρίς να ξεπεράσει το maximum. Δεν επιστρέφει τίποτα.
    is_empty(): επιστρέφει True αν το value είναι 0.
    """

    def __init__(self, maximum):
        raise NotImplementedError

    def spend(self, amount):
        raise NotImplementedError

    def rest(self, amount):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError


def make_monster(kind):
    """Κύκλος 3. Επιστρέφει ένα ΝΕΟ αντικείμενο Fighter για τον τύπο που ζητήθηκε.

    "goblin" -> Fighter("Γκόμπλιν", 25, 5, 1)
    "orc"    -> Fighter("Ορκ", 40, 7, 1)
    "dragon" -> Fighter("Δράκος", 60, 9, 1)
    Για οποιονδήποτε άλλο τύπο επιστρέφει None.
    """
    raise NotImplementedError


def alive_names(fighters):
    """Κύκλος 4. Επιστρέφει λίστα με τα ονόματα των μαχητών της λίστας που ζουν, με την ίδια σειρά.

    Δεν αλλάζει τη λίστα ούτε τους μαχητές. Παράδειγμα: για δύο ζωντανούς και έναν νεκρό επιστρέφει δύο ονόματα.
    """
    raise NotImplementedError
