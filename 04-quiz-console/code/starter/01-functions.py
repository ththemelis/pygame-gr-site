"""Στάδιο 1 — Συναρτήσεις του κουίζ.

Τρεις συναρτήσεις: ποσοστό σωστών, μήνυμα κρίσης και έγκυρη είσοδος. Το πρόγραμμα στο τέλος τις
χρησιμοποιεί για να δείξει το αποτέλεσμα ενός κουίζ 8 ερωτήσεων.

Συμπλήρωσε τα πέντε κενά (____).
"""

def percentage(correct, total):
    """Επιστρέφει το ποσοστό των σωστών απαντήσεων."""
    # TODO 1: ποσοστό = σωστές × 100 / (ποιο μέγεθος;)
    return correct * 100 / ____


# TODO 2: δώσε όνομα στην παράμετρο. Το σώμα της συνάρτησης τη χρησιμοποιεί ως percent
def verdict(____):
    """Επιστρέφει ένα μήνυμα ανάλογα με το ποσοστό."""
    if percent >= 90:
        return "Άριστα."
    elif percent >= 70:
        return "Πολύ καλά."
    elif percent >= 50:
        return "Καλά."
    else:
        return "Χρειάζεσαι λίγη ακόμη μελέτη."


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
            # TODO 3: η έγκυρη τιμή πρέπει να επιστραφεί στον καλούντα· ποια εντολή το κάνει;
            ____ number
        print(f"Ο αριθμός πρέπει να είναι από {low} έως {high}.")


TOTAL = 8
# TODO 4: ποια είναι η μικρότερη επιτρεπτή τιμή (low);
correct = ask_number(f"Πόσες απαντήσεις ήταν σωστές (0-{TOTAL}); ", ____, TOTAL)
percent = percentage(correct, TOTAL)
print(f"Ποσοστό: {percent:.1f}%")
# TODO 5: δώσε στη verdict το ποσοστό που υπολογίστηκε παραπάνω
print(verdict(____))
