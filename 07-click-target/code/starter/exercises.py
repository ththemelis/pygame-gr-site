"""Ασκήσεις του Μαθήματος 7 (τέσσερις συναρτήσεις).

Γράψε τον κώδικα κάθε συνάρτησης στη θέση της γραμμής `raise NotImplementedError`.
Έλεγχος:  python check_exercises.py

Οι ασκήσεις δεν χρειάζονται pygame: δουλεύεις με αριθμούς και πλειάδες.
"""
import random


def brighter(color, amount):
    """Κύκλος 1. Επιστρέφει νέο χρώμα (πλειάδα R, G, B) με κάθε κανάλι αυξημένο κατά amount, χωρίς να ξεπερνά το 255.

    Παραδείγματα: brighter((200, 50, 20), 60) -> (255, 110, 80),  brighter((0, 0, 0), 30) -> (30, 30, 30)
    """
    raise NotImplementedError


def inside_rect(x, y, left, top, width, height):
    """Κύκλος 2. True αν το σημείο (x, y) είναι μέσα στο ορθογώνιο, όπως κάνει η collidepoint.

    Η αριστερή και η πάνω πλευρά ανήκουν στο ορθογώνιο. Η δεξιά και η κάτω πλευρά δεν ανήκουν.
    Παραδείγματα: inside_rect(5, 5, 0, 0, 10, 10) -> True,  inside_rect(10, 5, 0, 0, 10, 10) -> False
    """
    raise NotImplementedError


def random_position(width, height, size, top=0):
    """Κύκλος 3. Επιστρέφει (x, y): τυχαία θέση για τετράγωνο πλευράς size που χωρά ολόκληρο μέσα στο παράθυρο.

    Το x είναι από 0 έως width - size. Το y είναι από top έως height - size (το top αφήνει χώρο
    για την περιοχή πληροφοριών). Χρησιμοποίησε την random.randint.
    """
    raise NotImplementedError


def accuracy(hits, misses):
    """Κύκλος 4. Επιστρέφει την ακρίβεια ως ποσοστό: τα hits προς όλα τα κλικ (hits + misses), από 0 έως 100.

    Αν δεν έγινε κανένα κλικ, επιστρέφει 0.
    Παραδείγματα: accuracy(5, 0) -> 100.0,  accuracy(5, 5) -> 50.0,  accuracy(0, 0) -> 0
    """
    raise NotImplementedError
