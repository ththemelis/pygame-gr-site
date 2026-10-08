"""Στάδιο 1 — Το παράθυρο και ο βρόχος του παιχνιδιού.

Συμπλήρωσε τα πέντε κενά (____). Όταν το πρόγραμμα τρέξει, εμφανίζεται ένα παράθυρο με σκούρο μπλε
φόντο, που μένει ανοιχτό μέχρι να το κλείσεις με το X.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
BACKGROUND = (25, 35, 60)

# TODO 1: το μέγεθος του παραθύρου δίνεται ως ΜΙΑ πλειάδα (πλάτος, ύψος)
screen = pygame.display.set_mode(____)
pygame.display.set_caption("Πάτα τον στόχο")

running = True
while running:
    # TODO 2: πάρε όλα τα συμβάντα που έγιναν από το προηγούμενο καρέ
    for event in pygame.event.____():
        # TODO 3: το συμβάν που φτάνει όταν ο χρήστης πατά το X του παραθύρου
        if event.type == pygame.____:
            running = False

    # TODO 4: γέμισε ολόκληρο το παράθυρο με το χρώμα του φόντου
    screen.____(BACKGROUND)
    # TODO 5: εμφάνισε στην οθόνη ό,τι ζωγραφίστηκε σε αυτό το καρέ
    pygame.display.____()

pygame.quit()
