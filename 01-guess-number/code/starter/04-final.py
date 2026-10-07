"""Στάδιο 4 — Σπάσε τον κωδικό: τελική έκδοση.

Ο κωδικός επιλέγεται τυχαία, ο παίκτης έχει όριο προσπαθειών και το πρόγραμμα
ελέγχει αν ο αριθμός είναι μέσα στα όρια.

Συμπλήρωσε τα πέντε κενά (____).
"""

import random

MIN_NUMBER = 1
MAX_NUMBER = 20
MAX_ATTEMPTS = 5

# TODO 1: διάλεξε τυχαίο ακέραιο από το MIN_NUMBER έως το MAX_NUMBER (και τα δύο περιλαμβάνονται)
secret = random.____(MIN_NUMBER, MAX_NUMBER)
attempts = 0
found = False

print(f"Η θυρίδα κλειδώθηκε με κωδικό από το {MIN_NUMBER} έως το {MAX_NUMBER}.")
print(f"Έχεις {MAX_ATTEMPTS} προσπάθειες.")

# TODO 2: συνέχισε όσο απομένουν προσπάθειες ΚΑΙ ο κωδικός δεν έχει βρεθεί
while ____:
    guess = int(input("Ο κωδικός σου: "))
    attempts += 1

    # TODO 3: ο αριθμός είναι μικρότερος από το ελάχιστο Ή μεγαλύτερος από το μέγιστο
    if ____:
        print(f"Εκτός ορίων. Ο κωδικός είναι από {MIN_NUMBER} έως {MAX_NUMBER}.")
    elif guess == secret:
        found = True
    elif guess < secret:
        print("Ο κωδικός είναι μεγαλύτερος.")
    else:
        print("Ο κωδικός είναι μικρότερος.")

    if not found:
        # TODO 4: πόσες προσπάθειες απομένουν; (όλες μείον όσες έγιναν)
        remaining = ____ - attempts
        print(f"Προσπάθειες που απομένουν: {remaining}")

# TODO 5: ποια μεταβλητή δείχνει ότι ο παίκτης νίκησε;
if ____:
    print(f"Η θυρίδα άνοιξε. Προσπάθειες: {attempts}")
else:
    print(f"Η θυρίδα κλειδώθηκε οριστικά. Ο κωδικός ήταν {secret}.")
