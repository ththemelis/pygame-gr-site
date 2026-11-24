"""Στάδιο 4 — Τελική έκδοση: ο παίκτης διαλέγει τους πόντους νίκης.

Στην αρχή το πρόγραμμα ρωτά πόσους πόντους χρειάζεται ο νικητής (1 έως 5). Η είσοδος
ελέγχεται: γράμματα και αριθμοί εκτός ορίων δεν γίνονται δεκτά και ο παίκτης ρωτιέται ξανά.

Συμπλήρωσε τα πέντε κενά (____).
"""

import random

CHOICES = ["πέτρα", "ψαλίδι", "χαρτί"]

print("Πέτρα, ψαλίδι, χαρτί")

while True:
    answer = input("Πόντοι για τη νίκη (1-5): ")
    # TODO 1: δοκίμασε τη μετατροπή σε ακέραιο (η λέξη-κλειδί που ανοίγει το μπλοκ)
    ____:
        win_score = int(answer)
    # TODO 2: πιάσε το σφάλμα που προκαλεί η int() όταν το κείμενο δεν είναι αριθμός
    except ____:
        print("Γράψε έναν ακέραιο αριθμό.")
        # TODO 3: γύρνα στην αρχή του βρόχου και ρώτα ξανά
        ____
    # TODO 4: αλυσιδωτή σύγκριση: win_score από 1 έως 5 (με τα δύο όρια μέσα)
    if 1 <= win_score <= ____:
        break
    print("Ο αριθμός πρέπει να είναι από 1 έως 5.")

player_score, computer_score = 0, 0
round_number = 1

while player_score < win_score and computer_score < win_score:
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
        player_score += 1
    else:
        print("Κέρδισε ο υπολογιστής τον γύρο.")
        computer_score += 1

    print(f"Σκορ: {player_score} - {computer_score}")
    round_number += 1

print()
# TODO 5: ποιος έφτασε τους πόντους νίκης; Συμπλήρωσε τη μεταβλητή του παίκτη
if ____ == win_score:
    print(f"Κέρδισες τον αγώνα με {player_score}-{computer_score}.")
else:
    print(f"Κέρδισε ο υπολογιστής με {computer_score}-{player_score}.")
