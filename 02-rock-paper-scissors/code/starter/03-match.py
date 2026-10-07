"""Στάδιο 3 — Αγώνας μέχρι τους 3 πόντους.

Ο έλεγχος της επιλογής από το Στάδιο 2 δίνεται έτοιμος, μέσα σε εξωτερικό βρόχο που
παίζει γύρους. Πρόσθεσε τα σκορ και τον τερματισμό του αγώνα.

Συμπλήρωσε τα έξι κενά (____).
"""

import random

CHOICES = ["πέτρα", "ψαλίδι", "χαρτί"]
WIN_SCORE = 3

# TODO 1: δώσε την τιμή 0 και στις δύο μεταβλητές με μία πολλαπλή εκχώρηση
player_score, computer_score = ____
round_number = 1

print(f"Πέτρα, ψαλίδι, χαρτί. Νικητής όποιος φτάσει πρώτος τους {WIN_SCORE} πόντους.")

# TODO 2: συνέχισε όσο ΚΑΝΕΝΑΣ δεν έχει φτάσει τους WIN_SCORE πόντους
while ____:
    print()
    print(f"Γύρος {round_number}")
    print(f"1 = {CHOICES[0]}, 2 = {CHOICES[1]}, 3 = {CHOICES[2]}")

    while True:
        answer = input("Η επιλογή σου: ").strip()
        if answer in ["1", "2", "3"]:
            break
        print("Η επιλογή πρέπει να είναι 1, 2 ή 3.")

    player = CHOICES[int(answer) - 1]
    computer = random.choice(CHOICES)
    print(f"Εσύ: {player} | Υπολογιστής: {computer}")

    if player == computer:
        print("Ισοπαλία.")
    elif (
        (player == "πέτρα" and computer == "ψαλίδι")
        or (player == "ψαλίδι" and computer == "χαρτί")
        or (player == "χαρτί" and computer == "πέτρα")
    ):
        print("Κέρδισες τον γύρο.")
        # TODO 3: πρόσθεσε έναν πόντο στον παίκτη
        ____ += 1
    else:
        print("Κέρδισε ο υπολογιστής τον γύρο.")
        # TODO 4: πρόσθεσε έναν πόντο στον υπολογιστή
        ____ += 1

    print(f"Σκορ: {player_score} - {computer_score}")
    # TODO 5: ο επόμενος γύρος έχει αριθμό κατά 1 μεγαλύτερο
    round_number ____ 1

print()
# TODO 6: ο αγώνας τελείωσε. Ο παίκτης νίκησε αν έφτασε τους WIN_SCORE πόντους
if ____ == WIN_SCORE:
    print("Κέρδισες τον αγώνα.")
else:
    print("Κέρδισε ο υπολογιστής τον αγώνα.")
