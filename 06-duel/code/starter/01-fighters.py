"""Στάδιο 1 — Η κλάση Fighter και τα πρώτα αντικείμενα.

Η κλάση Fighter είναι το «καλούπι» ενός μαχητή: ορίζει ποιες ιδιότητες έχει (όνομα, ζωή, δύναμη, θεραπείες) και τι
μπορεί να κάνει. Από το ίδιο καλούπι φτιάχνουμε όσα αντικείμενα θέλουμε, καθένα με τις δικές του ιδιότητες.

Συμπλήρωσε τα επτά κενά (____).
"""

# TODO 1: η λέξη-κλειδί class ακολουθείται από το όνομα της κλάσης: Fighter
class ____:
    """Ένας μαχητής: όνομα, ζωή, δύναμη επίθεσης και θεραπείες που του απομένουν."""

    # TODO 2: η ειδική μέθοδος που καλείται αυτόματα όταν δημιουργείται ένα αντικείμενο (μέθοδος αρχικοποίησης)
    def ____(self, name, health, power, potions):
        # TODO 3: η ιδιότητα name παίρνει την τιμή της παραμέτρου name
        self.name = ____
        self.health = health
        # TODO 4: η μέγιστη ζωή είναι η ζωή με την οποία ξεκινά ο μαχητής
        self.max_health = ____
        self.power = power
        self.potions = potions

    def describe(self):
        # TODO 5: η ιδιότητα της ζωής του ίδιου του αντικειμένου (self)
        return f"{self.name}: ζωή {self.____}/{self.max_health}, δύναμη {self.power}, θεραπείες {self.potions}"


# TODO 6: δημιουργία αντικειμένου: γράφεις το όνομα της κλάσης και τις τιμές για τη μέθοδο αρχικοποίησης
hero = ____("Ήρωας", 60, 9, 3)
goblin = Fighter("Γκόμπλιν", 25, 5, 1)

print(hero.describe())
print(goblin.describe())

# TODO 7: αλλαγή της ζωής του goblin, χωρίς να αλλάξει ο ήρωας
goblin.____ = 10
print()
print("Μετά την αλλαγή της ζωής του Γκόμπλιν:")
print(hero.describe())
print(goblin.describe())

same_goblin = goblin
same_goblin.health = 1
print()
print(f"Η ζωή του goblin μετά την αλλαγή μέσω του same_goblin: {goblin.health}")
