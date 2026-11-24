"""Στάδιο 4 — Κρεμάλα: τελική έκδοση με έλεγχο γράμματος και σχέδιο.

Προστίθενται: έλεγχος ότι η είσοδος είναι ένα ελληνικό γράμμα (με φωλιασμένες συνθήκες) και
το σχέδιο της κρεμάλας, που δίνεται έτοιμο στη λίστα STAGES (ένα σχέδιο για κάθε αριθμό λαθών).

Συμπλήρωσε τα πέντε κενά (____).
"""

import random

WORDS = [
    "ΠΡΟΓΡΑΜΜΑ", "ΜΕΤΑΒΛΗΤΗ", "ΣΥΝΑΡΤΗΣΗ", "ΠΛΗΚΤΡΟΛΟΓΙΟ", "ΒΡΟΧΟΣ",
    "ΛΙΣΤΑ", "ΟΘΟΝΗ", "ΠΟΝΤΙΚΙ", "ΕΠΕΞΕΡΓΑΣΤΗΣ", "ΛΕΙΤΟΥΡΓΙΚΟ",
]
ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
MAX_MISTAKES = 6

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

word = random.choice(WORDS)
guessed = set()
wrong = []
mistakes = 0
won = False

print("Κρεμάλα")
print(f"Η λέξη έχει {len(word)} γράμματα. Γράψε ένα ελληνικό γράμμα τη φορά, χωρίς τόνο.")

while mistakes < MAX_MISTAKES:
    # TODO 1: το σχέδιο που αντιστοιχεί στον αριθμό των λαθών μέχρι τώρα
    print(STAGES[____])

    display = ""
    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "
    print(display)
    print("Λάθη:", " ".join(wrong))

    if "_" not in display:
        won = True
        break

    guess = input("Γράμμα: ").strip().upper()

    # TODO 2: η είσοδος πρέπει να έχει ακριβώς ένα γράμμα
    if len(guess) != ____ or guess not in ALPHABET:
        print("Γράψε ένα ελληνικό γράμμα, χωρίς τόνο.")
    # TODO 3: το γράμμα έχει ήδη δοκιμαστεί (ελέγχεται σε ποια δομή;)
    elif guess in ____:
        print("Το έχεις ήδη δοκιμάσει.")
    else:
        guessed.add(guess)
        # TODO 4: το γράμμα ανήκει στη λέξη που μαντεύουμε
        if guess in ____:
            print("Σωστά.")
        else:
            print("Λάθος γράμμα.")
            wrong.append(guess)
            mistakes += 1

print()
# TODO 5: ποια μεταβλητή δείχνει ότι ο παίκτης νίκησε;
if ____:
    print(f"Κέρδισες. Η λέξη ήταν {word}.")
else:
    print(STAGES[mistakes])
    print("Λάθη:", " ".join(wrong))
    print(f"Έχασες. Η λέξη ήταν {word}.")
