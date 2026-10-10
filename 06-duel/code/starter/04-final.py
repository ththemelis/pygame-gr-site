"""Στάδιο 4 — Το τουρνουά: λίστα από αντικείμενα.

Ο ήρωας παλεύει με μια σειρά αντιπάλων. Κάθε αντίπαλος είναι ένα αντικείμενο της ίδιας κλάσης Fighter, με
διαφορετικές τιμές. Η κλάση αποκτά τη μέθοδο bar (μπάρα ζωής). Οι υπόλοιπες συναρτήσεις δίνονται έτοιμες από τα
προηγούμενα στάδια.

Συμπλήρωσε τα έξι κενά (____). Το TODO 4 είναι ολόκληρη γραμμή.
"""
import random

POTION_HEAL = 15
REST_AFTER_WIN = 20
BAR_WIDTH = 20


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
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def restore(self, amount):
        gained = amount
        if self.health + gained > self.max_health:
            gained = self.max_health - self.health
        self.health += gained
        return gained

    def heal(self):
        if self.potions == 0 or self.health == self.max_health:
            return 0
        self.potions -= 1
        return self.restore(POTION_HEAL)

    def attack(self, other):
        damage = random.randint(self.power - 2, self.power + 2)
        other.take_damage(damage)
        return damage

    def bar(self):
        """Η ζωή ως μπάρα: # για τη ζωή που απομένει και . για αυτή που χάθηκε."""
        # TODO 1: το ποσοστό της ζωής επί το πλάτος της μπάρας, δια τη μέγιστη ζωή
        filled = self.health * BAR_WIDTH // ____
        # Ένας μαχητής που ζει έχει πάντα τουλάχιστον ένα # στην μπάρα
        if filled == 0 and self.health > 0:
            filled = 1
        # TODO 2: τα κενά κελιά είναι όσα το πλάτος μείον τα γεμάτα
        return "#" * filled + "." * (BAR_WIDTH - ____)


def ask_number(prompt, low, high):
    """Ζητά ακέραιο από low έως high και ρωτά ξανά μέχρι να είναι έγκυρος."""
    while True:
        answer = input(prompt)
        try:
            number = int(answer)
        except ValueError:
            print("Γράψε έναν ακέραιο αριθμό.")
            continue
        if low <= number <= high:
            return number
        print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")


def show_status(fighter):
    # TODO 3: η μέθοδος των συμβολοσειρών που συμπληρώνει με κενά δεξιά μέχρι να φτάσει το πλάτος 10
    print(f"{fighter.name.____(10)} [{fighter.bar()}] {fighter.health}/{fighter.max_health}  θεραπείες: {fighter.potions}")


def player_turn(player, enemy):
    """Ο παίκτης διαλέγει επίθεση ή θεραπεία. Αν η θεραπεία δεν γίνεται, ρωτά ξανά."""
    print("1) Επίθεση   2) Θεραπεία")
    while True:
        choice = ask_number("Τι κάνεις; ", 1, 2)
        if choice == 1:
            damage = player.attack(enemy)
            print(f"Επίθεση. {enemy.name}: -{damage} ζωή.")
            return
        healed = player.heal()
        if healed == 0:
            print("Δεν μπορείς να θεραπευτείς τώρα (δεν έχεις θεραπείες ή η ζωή σου είναι γεμάτη).")
        else:
            print(f"Θεραπεία. {player.name}: +{healed} ζωή.")
            return


def enemy_turn(enemy, player):
    """Ο αντίπαλος θεραπεύεται όταν η ζωή του είναι το πολύ το ένα τρίτο, αλλιώς επιτίθεται."""
    if enemy.health <= enemy.max_health // 3 and enemy.potions > 0:
        healed = enemy.heal()
        print(f"{enemy.name} θεραπεύεται. {enemy.name}: +{healed} ζωή.")
    else:
        damage = enemy.attack(player)
        print(f"{enemy.name} επιτίθεται. {player.name}: -{damage} ζωή.")


def battle(player, enemy):
    """Μάχη γύρων μέχρι να πέσει ένας από τους δύο. Επιστρέφει True αν νικήσει ο παίκτης."""
    print()
    print(f"Νέος αντίπαλος: {enemy.describe()}")
    while player.is_alive() and enemy.is_alive():
        print()
        show_status(player)
        show_status(enemy)
        player_turn(player, enemy)
        if enemy.is_alive():
            enemy_turn(enemy, player)
    return player.is_alive()


def make_enemies():
    """Φτιάχνει νέα λίστα αντιπάλων (νέα αντικείμενα) για κάθε παιχνίδι."""
    return [
        Fighter("Γκόμπλιν", 25, 5, 1),
        Fighter("Ορκ", 40, 7, 1),
        # TODO 4: ο τρίτος αντίπαλος: ο Δράκος, με ζωή 60, δύναμη 9 και μία θεραπεία
        ____
    ]


def main():
    print("ΜΟΝΟΜΑΧΙΑ")
    print(f"Νίκησε όλους τους αντιπάλους. Μετά από κάθε νίκη παίρνεις μέχρι {REST_AFTER_WIN} ζωή.")
    player = Fighter("Ήρωας", 60, 9, 3)
    # TODO 5: η μεταβλητή που παίρνει έναν αντίπαλο της λίστας σε κάθε επανάληψη
    for ____ in make_enemies():
        if not battle(player, enemy):
            print()
            print(f"Έχασες από: {enemy.name}.")
            return
        print()
        print(f"Νίκησες: {enemy.name}.")
        # TODO 6: η μέθοδος που δίνει ζωή στον παίκτη χωρίς να χρησιμοποιεί θεραπεία
        gained = player.____(REST_AFTER_WIN)
        print(f"Ξεκουράζεσαι: +{gained} ζωή.")
    print()
    print("Νίκησες όλους τους αντιπάλους. Είσαι ο πρωταθλητής.")


main()
