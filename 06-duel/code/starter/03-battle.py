"""Στάδιο 3 — Η μάχη γύρων.

Σε κάθε γύρο παίζει πρώτα ο παίκτης (επίθεση ή θεραπεία) και μετά ο αντίπαλος, μέχρι να πέσει ο ένας από τους
δύο. Η κλάση Fighter και η ask_number δίνονται έτοιμες. Εσύ γράφεις τις συναρτήσεις των γύρων και της μάχης.

Συμπλήρωσε τα οκτώ κενά (____). Τα TODO 2 και 7 είναι ολόκληρες γραμμές.
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
    print(fighter.describe())


def player_turn(player, enemy):
    """Ο παίκτης διαλέγει επίθεση ή θεραπεία. Αν η θεραπεία δεν γίνεται, ρωτά ξανά."""
    print("1) Επίθεση   2) Θεραπεία")
    while True:
        choice = ask_number("Τι κάνεις; ", 1, 2)
        # TODO 1: η επιλογή 1 είναι η επίθεση
        if choice == ____:
            # TODO 2: ο παίκτης επιτίθεται στον αντίπαλο και κρατάς τη ζημιά στη μεταβλητή damage
            ____
            print(f"Επίθεση. {enemy.name}: -{damage} ζωή.")
            return
        # TODO 3: η μέθοδος του μαχητή που θεραπεύει και επιστρέφει πόση ζωή πήρε
        healed = player.____()
        # TODO 4: αν δεν πήρε καθόλου ζωή, η θεραπεία δεν έγινε
        if healed == ____:
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
        # TODO 5: ο αντίπαλος επιτίθεται στον παίκτη
        damage = enemy.attack(____)
        print(f"{enemy.name} επιτίθεται. {player.name}: -{damage} ζωή.")


def battle(player, enemy):
    """Μάχη γύρων μέχρι να πέσει ένας από τους δύο. Επιστρέφει True αν νικήσει ο παίκτης."""
    print()
    print(f"Νέος αντίπαλος: {enemy.describe()}")
    # TODO 6: η μάχη συνεχίζεται όσο ζουν και οι δύο
    while player.is_alive() and ____:
        print()
        show_status(player)
        show_status(enemy)
        # TODO 7: παίζει ο παίκτης (κάλεσε τη συνάρτηση player_turn)
        ____
        if enemy.is_alive():
            enemy_turn(enemy, player)
    # TODO 8: νικητής είναι ο παίκτης αν ζει ακόμη
    return ____


def main():
    print("ΜΟΝΟΜΑΧΙΑ")
    player = Fighter("Ήρωας", 60, 9, 3)
    enemy = Fighter("Γκόμπλιν", 25, 5, 1)
    if battle(player, enemy):
        print()
        print(f"Νίκησες: {enemy.name}.")
    else:
        print()
        print(f"Έχασες από: {enemy.name}.")


main()
