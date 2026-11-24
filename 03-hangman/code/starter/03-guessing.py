"""Στάδιο 3 — Ο βρόχος του παιχνιδιού με σύνολο και λίστα.

Τα γράμματα που έχουν δοκιμαστεί μπαίνουν σε σύνολο (guessed). Τα λάθος γράμματα μπαίνουν
σε λίστα (wrong), για να εμφανίζονται με τη σειρά που δοκιμάστηκαν. Η αποκάλυψη της λέξης
δίνεται έτοιμη από το Στάδιο 2.

Συμπλήρωσε τα έξι κενά (____).

Γνωστός περιορισμός: αν γράψεις κενό (μόνο Enter) ή πολλά γράμματα, το πρόγραμμα
συμπεριφέρεται παράξενα. Θα το διορθώσεις στο Στάδιο 4.
"""

import random

WORDS = [
    "ΠΡΟΓΡΑΜΜΑ", "ΜΕΤΑΒΛΗΤΗ", "ΣΥΝΑΡΤΗΣΗ", "ΠΛΗΚΤΡΟΛΟΓΙΟ", "ΒΡΟΧΟΣ",
    "ΛΙΣΤΑ", "ΟΘΟΝΗ", "ΠΟΝΤΙΚΙ", "ΕΠΕΞΕΡΓΑΣΤΗΣ", "ΛΕΙΤΟΥΡΓΙΚΟ",
]
MAX_MISTAKES = 6

word = random.choice(WORDS)
# TODO 1: κενό σύνολο (προσοχή: το {} δεν είναι κενό σύνολο)
guessed = ____
# TODO 2: κενή λίστα
wrong = ____
mistakes = 0
won = False

print("Κρεμάλα")

while mistakes < MAX_MISTAKES:
    display = ""
    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "
    print()
    print(display)
    print("Λάθη:", " ".join(wrong))

    # TODO 3: αν δεν υπάρχει κανένα "_" στην display, η λέξη έχει συμπληρωθεί
    if "_" ____ display:
        won = True
        break

    guess = input("Γράμμα: ").strip().upper()

    if guess in guessed:
        print("Το έχεις ήδη δοκιμάσει.")
    else:
        # TODO 4: πρόσθεσε το γράμμα στο σύνολο guessed (μέθοδος συνόλου)
        guessed.____(guess)
        if guess in word:
            print("Σωστά.")
        else:
            print("Λάθος γράμμα.")
            # TODO 5: πρόσθεσε το γράμμα στο τέλος της λίστας wrong (μέθοδος λίστας)
            wrong.____(guess)
            # TODO 6: αύξησε τον μετρητή λαθών κατά 1
            mistakes ____ 1

print()
if won:
    print(f"Κέρδισες. Η λέξη ήταν {word}.")
else:
    print(f"Έχασες. Η λέξη ήταν {word}.")
