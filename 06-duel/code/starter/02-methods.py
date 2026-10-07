"""Στάδιο 2 — Μέθοδοι που αλλάζουν το αντικείμενο και αντικείμενα που αλληλεπιδρούν.

Η κλάση Fighter αποκτά συμπεριφορά: ζει ή όχι, δέχεται ζημιά, ανακτά ζωή, θεραπεύεται και επιτίθεται σε άλλον
μαχητή. Το τελευταίο μέρος του αρχείου δοκιμάζει τις μεθόδους. Η __init__ και η describe δίνονται έτοιμες.

Συμπλήρωσε τα οκτώ κενά (____).
"""
import random

POTION_HEAL = 15


class Fighter:
    """Ένας μαχητής: όνομα, ζωή, δύναμη επίθεσης και θεραπείες που του απομένουν."""

    def __init__(self, name, health, power, potions):
        self.name = name
        self.health = health
        self.max_health = health
        self.power = power
        self.potions = potions

    def describe(self):
        return f"{self.name}: ζωή {self.health}/{self.max_health}, δύναμη {self.power}, θεραπείες {self.potions}"

    def is_alive(self):
        # TODO 1: ο μαχητής ζει όταν η ζωή του είναι μεγαλύτερη από το 0
        return self.health ____ 0

    def take_damage(self, amount):
        # TODO 2: η ζωή μειώνεται κατά τη ζημιά που δέχεται η μέθοδος
        self.health -= ____
        if self.health < 0:
            self.health = 0

    def restore(self, amount):
        gained = amount
        # TODO 3: δεν μπορεί να ξεπεραστεί η μέγιστη ζωή: το κέρδος είναι ό,τι λείπει για να φτάσει εκεί
        if self.health + gained > self.max_health:
            gained = self.max_health - ____
        self.health += gained
        return gained

    def heal(self):
        if self.potions == 0 or self.health == self.max_health:
            return 0
        self.potions -= 1
        # TODO 4: μια μέθοδος του ίδιου αντικειμένου καλείται με self. μπροστά
        return self.____(POTION_HEAL)

    def attack(self, other):
        # TODO 5: τυχαία ζημιά γύρω από τη δύναμη: από δύναμη - 2 έως δύναμη + 2
        damage = random.randint(self.power - 2, self.power + ____)
        # TODO 6: ο αντίπαλος (other) δέχεται τη ζημιά με τη δική του μέθοδο
        other.____(damage)
        # TODO 7: η μέθοδος επιστρέφει πόση ζημιά έκανε
        return ____


hero = Fighter("Ήρωας", 60, 9, 3)
goblin = Fighter("Γκόμπλιν", 25, 5, 1)
print(hero.describe())
print(goblin.describe())
print()

damage = hero.attack(goblin)
print(f"{hero.name} επιτίθεται. {goblin.name}: -{damage} ζωή.")
damage = goblin.attack(hero)
print(f"{goblin.name} επιτίθεται. {hero.name}: -{damage} ζωή.")
print()
print(hero.describe())
print(goblin.describe())
print()

healed = hero.heal()
print(f"{hero.name} θεραπεύεται: +{healed} ζωή.")
healed = hero.heal()
print(f"Δεύτερη θεραπεία, με γεμάτη ζωή: +{healed} ζωή.")
print(hero.describe())
print()

# TODO 8: μεγάλη ζημιά, για να δούμε ότι η ζωή δεν γίνεται αρνητική (χρησιμοποίησε τη μέθοδο take_damage)
goblin.take_damage(____)
print(goblin.describe())
print(f"Ζει ο {goblin.name}; {goblin.is_alive()}")
