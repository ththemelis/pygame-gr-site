"""Στάδιο 2 — Οι ερωτήσεις ως λίστα από λεξικά.

Κάθε ερώτηση είναι ένα λεξικό με κλειδιά "text", "choices", "answer" και "topic". Το πρόγραμμα
κάνει όλες τις ερωτήσεις και λέει αν κάθε απάντηση ήταν σωστή. Η ask_number δίνεται έτοιμη.

Συμπλήρωσε τα τέσσερα κενά (____).
"""

QUESTIONS = [
    {
        "text": "Ποια εντολή εμφανίζει κείμενο στην οθόνη;",
        "choices": ["input", "print", "len"],
        "answer": 1,
        "topic": "Python",
    },
    {
        "text": "Τι τύπο έχει η τιμή 3.5;",
        "choices": ["int", "str", "float"],
        "answer": 2,
        "topic": "Python",
    },
    {
        "text": "Ποιο από τα παρακάτω είναι λίστα;",
        "choices": ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}"],
        "answer": 1,
        "topic": "Python",
    },
    {
        "text": "Τι σημαίνει η συντομογραφία RAM;",
        "choices": ["Μνήμη τυχαίας προσπέλασης", "Μόνιμη αποθήκευση δεδομένων", "Κάρτα γραφικών"],
        "answer": 0,
        "topic": "Υλικό",
    },
    {
        "text": "Σε ποια μονάδα μετριέται η συχνότητα ενός επεξεργαστή;",
        "choices": ["Watt", "Hertz", "Byte"],
        "answer": 1,
        "topic": "Υλικό",
    },
    {
        "text": "Ποιο κλασικό παιχνίδι του 1972 μιμείται το πινγκ-πονγκ;",
        "choices": ["Tetris", "Pong", "Snake"],
        "answer": 1,
        "topic": "Παιχνίδια",
    },
    {
        "text": "Τι σημαίνει FPS σε ένα παιχνίδι;",
        "choices": ["Καρέ ανά δευτερόλεπτο", "Πόντοι ανά παίκτη", "Ταχύτητα επεξεργαστή"],
        "answer": 0,
        "topic": "Παιχνίδια",
    },
    {
        "text": "Ποια βιβλιοθήκη της Python θα χρησιμοποιήσουμε για παιχνίδια με γραφικά;",
        "choices": ["tkinter", "pygame", "random"],
        "answer": 1,
        "topic": "Παιχνίδια",
    },
]


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


def ask_question(number, question):
    """Εμφανίζει μια ερώτηση και επιστρέφει True αν η απάντηση του παίκτη είναι σωστή."""
    print()
    # TODO 1: πάρε το κείμενο της ερώτησης από το λεξικό. Μέσα σε f-string με διπλά εισαγωγικά, το κλειδί γράφεται με μονά
    print(f"Ερώτηση {number}: {question[____]}")
    for i in range(len(question["choices"])):
        print(f"  {i + 1}) {question['choices'][i]}")
    # TODO 2: ο παίκτης διαλέγει από 1 μέχρι το πλήθος των επιλογών της ερώτησης
    choice = ask_number("Η απάντησή σου: ", 1, ____)
    # TODO 3: ποιο κλειδί κρατά τον δείκτη της σωστής επιλογής;
    return choice - 1 == question[____]


for number in range(len(QUESTIONS)):
    question = QUESTIONS[number]
    if ask_question(number + 1, question):
        print("Σωστά.")
    else:
        # TODO 4: το κείμενο της σωστής επιλογής: λίστα επιλογών, με δείκτη το ίδιο κλειδί
        right = question["choices"][question[____]]
        print(f"Λάθος. Η σωστή απάντηση ήταν: {right}")
