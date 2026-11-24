"""Στάδιο 3 — Αποτελέσματα με πλειάδα και λεξικά.

Η play παίζει όλες τις ερωτήσεις και επιστρέφει τρεις τιμές μαζί (πλειάδα): πόσες ήταν σωστές
και δύο λεξικά που μετρούν τις ερωτήσεις και τις σωστές απαντήσεις ανά θέμα. Οι ask_number,
ask_question, percentage και verdict δίνονται έτοιμες.

Συμπλήρωσε τα έξι κενά (____).
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
        # TODO 1: η μέθοδος του λεξικού που δίνει την τιμή ενός κλειδιού, ή μια προεπιλογή αν το κλειδί λείπει
        asked[topic] = asked.____(topic, 0) + 1
        if ask_question(number + 1, question):
            print("Σωστά.")
            correct += 1
            # TODO 2: μια ακόμη σωστή απάντηση σε αυτό το θέμα
            right[topic] = right.get(topic, 0) + ____
        else:
            answer_text = question["choices"][question["answer"]]
            print(f"Λάθος. Η σωστή απάντηση ήταν: {answer_text}")
    # TODO 3: η συνάρτηση επιστρέφει τρεις τιμές. Λείπει η τελευταία (το λεξικό των σωστών ανά θέμα)
    return correct, asked, ____


# TODO 4: κάλεσε τη συνάρτηση που παίζει όλες τις ερωτήσεις
correct, asked, right = ____(QUESTIONS)
total = len(QUESTIONS)
percent = percentage(correct, total)
print()
print(f"Σωστές απαντήσεις: {correct} από {total} ({percent:.1f}%)")
print(verdict(percent))
print("Σωστές ανά θέμα:")
# TODO 5: η μέθοδος που δίνει ζεύγη (κλειδί, τιμή) ενός λεξικού
for topic, count in asked.____():
    # TODO 6: αν σε ένα θέμα δεν υπάρχει καμία σωστή απάντηση, πόσες θεωρούμε ότι είναι;
    print(f"  {topic}: {right.get(topic, ____)} από {count}")
