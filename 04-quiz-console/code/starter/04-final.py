"""Στάδιο 4 — Κουίζ γνώσεων: τελική έκδοση.

Όλο το πρόγραμμα οργανώνεται σε συναρτήσεις, με μία κεντρική συνάρτηση main. Κάθε γύρος παίζει
5 τυχαίες ερωτήσεις από τις 8. Η show_title έχει προεπιλεγμένη τιμή για το πλάτος.

Συμπλήρωσε τα πέντε κενά (____).
"""

import random


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

QUESTIONS_PER_GAME = 5


# TODO 1: όνομα της παραμέτρου με προεπιλεγμένη τιμή 36 (χρησιμοποιείται στο σώμα ως width)
def show_title(title, ____=36):
    """Εμφανίζει τον τίτλο ανάμεσα σε γραμμές από «=». Το πλάτος έχει προεπιλεγμένη τιμή."""
    print("=" * width)
    print(title.center(width))
    print("=" * width)


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
    print(f"Ερώτηση {number}: {question['text']}")
    for i in range(len(question["choices"])):
        print(f"  {i + 1}) {question['choices'][i]}")
    choice = ask_number("Η απάντησή σου: ", 1, len(question["choices"]))
    return choice - 1 == question["answer"]


def percentage(correct, total):
    """Επιστρέφει το ποσοστό των σωστών απαντήσεων."""
    return correct * 100 / total


def verdict(percent):
    """Επιστρέφει ένα μήνυμα ανάλογα με το ποσοστό."""
    if percent >= 90:
        return "Άριστα."
    elif percent >= 70:
        return "Πολύ καλά."
    elif percent >= 50:
        return "Καλά."
    else:
        return "Χρειάζεσαι λίγη ακόμη μελέτη."


def play(questions):
    """Παίζει όλες τις ερωτήσεις. Επιστρέφει (σωστές, ερωτήσεις ανά θέμα, σωστές ανά θέμα)."""
    correct = 0
    asked = {}
    right = {}
    for number in range(len(questions)):
        question = questions[number]
        topic = question["topic"]
        asked[topic] = asked.get(topic, 0) + 1
        if ask_question(number + 1, question):
            print("Σωστά.")
            correct += 1
            right[topic] = right.get(topic, 0) + 1
        else:
            answer_text = question["choices"][question["answer"]]
            print(f"Λάθος. Η σωστή απάντηση ήταν: {answer_text}")
    return correct, asked, right


def main():
    """Παίζει έναν ολόκληρο γύρο κουίζ και εμφανίζει τα αποτελέσματα."""
    # TODO 2: κλήση με όρισμα με όνομα (keyword argument): δώσε πλάτος 30
    show_title("ΚΟΥΙΖ ΓΝΩΣΕΩΝ", ____=30)
    # TODO 3: διάλεξε τυχαία QUESTIONS_PER_GAME διαφορετικά στοιχεία από τη λίστα (χωρίς να την αλλάξεις)
    questions = random.____(QUESTIONS, QUESTIONS_PER_GAME)
    correct, asked, right = play(questions)
    total = len(questions)
    # TODO 4: το ποσοστό υπολογίζεται σε σχέση με το πλήθος των ερωτήσεων που παίχτηκαν
    percent = percentage(correct, ____)
    print()
    print(f"Σωστές απαντήσεις: {correct} από {total} ({percent:.1f}%)")
    print(verdict(percent))
    print("Σωστές ανά θέμα:")
    for topic, count in asked.items():
        print(f"  {topic}: {right.get(topic, 0)} από {count}")


# TODO 5: κάλεσε την κεντρική συνάρτηση, ώστε να ξεκινήσει το παιχνίδι
____()
