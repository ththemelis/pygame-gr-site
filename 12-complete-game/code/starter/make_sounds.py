"""Φτιάχνει με κώδικα τους ήχους του Μαθήματος 12 και τους αποθηκεύει στον φάκελο assets.

Τρέξε το μία φορά, από τον φάκελο του μαθήματος:  python make_sounds.py

Δεν χρειάζεται να καταλάβεις πώς δουλεύει. Δείχνει όμως ότι ένας ήχος είναι απλώς μια μεγάλη λίστα αριθμών, τα δείγματα
(samples): κάθε αριθμός λέει πόσο έξω ή μέσα βρίσκεται το ηχείο εκείνη τη στιγμή. Εδώ υπάρχουν 22 050 δείγματα για κάθε
δευτερόλεπτο ήχου. Ένας καθαρός τόνος είναι ένα ημίτονο (sin) και οι νότες της μουσικής είναι τόνοι με διαφορετική συχνότητα.
Μπορείς να αλλάξεις νότες και διάρκειες και να τρέξεις το πρόγραμμα ξανά. Κράτα τα ονόματα των αρχείων.
"""
import math
import os
import random
import struct
import wave

RATE = 22050               # δείγματα το δευτερόλεπτο
FOLDER = "assets"

# Οι νότες: πόσοι ημιτόνιοι είναι πάνω ή κάτω από το Λα της τέταρτης οκτάβας (440 Hz)
SEMITONES = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}

# Οι συγχορδίες της μουσικής: η νότα του μπάσου και τρεις νότες που ανεβαίνουν. Λα ελάσσονα, Φα, Ντο, Σολ.
CHORDS = (
    (("A", 3), (("A", 4), ("C", 5), ("E", 5))),
    (("F", 3), (("F", 4), ("A", 4), ("C", 5))),
    (("C", 3), (("C", 5), ("E", 5), ("G", 5))),
    (("G", 3), (("G", 4), ("B", 4), ("D", 5))),
)
PATTERN = (0, 1, 2, 1, 0, 1, 2, 1, 0, 2, 1, 2, 0, 1, 2, 1)       # ποια νότα της συγχορδίας παίζει κάθε όγδοο


def pitch(letter, octave):
    """Η συχνότητα (Hz) μιας νότας, π.χ. pitch("A", 4) είναι 440."""
    steps = SEMITONES[letter] + 12 * (octave - 4)
    return 440 * 2 ** (steps / 12)


def shape_value(shape, phase):
    """Η τιμή (από -1 έως 1) ενός κύματος για μια φάση (ο αριθμός των κύκλων που έχει κάνει ο τόνος)."""
    position = phase % 1
    if shape == "square":
        return 1.0 if position < 0.5 else -1.0
    if shape == "triangle":
        return 4 * abs(position - 0.5) - 1
    return math.sin(2 * math.pi * phase)


def tone(frequency, seconds, shape="sine", decay=6.0, volume=1.0, end_frequency=None):
    """Μια νότα: λίστα δειγμάτων από -1 έως 1. Η ένταση μικραίνει με τον χρόνο (decay) και σβήνει ομαλά στην αρχή και στο τέλος.
    Αν δοθεί end_frequency, η συχνότητα αλλάζει σταδιακά από την αρχική σε αυτήν."""
    count = int(seconds * RATE)
    fade = int(0.01 * RATE)
    samples = []
    phase = 0.0
    for index in range(count):
        if end_frequency is None:
            current = frequency
        else:
            current = frequency + (end_frequency - frequency) * index / count
        phase += current / RATE
        level = volume * math.exp(-decay * index / RATE)
        level *= min(1.0, index / fade, (count - 1 - index) / fade)
        samples.append(shape_value(shape, phase) * level)
    return samples


def silence(seconds):
    """Σιωπή: λίστα με μηδενικά."""
    return [0.0] * int(seconds * RATE)


def add_at(track, notes, start):
    """Προσθέτει τη λίστα δειγμάτων notes στο track, ξεκινώντας start δευτερόλεπτα μετά την αρχή."""
    offset = int(start * RATE)
    for index in range(len(notes)):
        if offset + index < len(track):
            track[offset + index] += notes[index]


def scaled(samples, peak):
    """Τα δείγματα πολλαπλασιασμένα, ώστε η μεγαλύτερη τιμή να γίνει peak (το 1.0 είναι η μέγιστη ένταση)."""
    biggest = 0.0
    for value in samples:
        biggest = max(biggest, abs(value))
    result = []
    for value in samples:
        result.append(value * peak / biggest)
    return result


def write_wave(path, samples):
    """Γράφει τα δείγματα σε αρχείο WAV: 16 bit, ένα κανάλι."""
    data = bytearray()
    for value in samples:
        value = max(-1.0, min(1.0, value))
        data += struct.pack("<h", int(value * 32767))
    with wave.open(path, "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(bytes(data))


def make_click():
    """Ένα σύντομο «τικ» για τα κουμπιά."""
    return scaled(tone(1200, 0.08, "sine", decay=40), 0.7)


def make_start():
    """Τέσσερις νότες που ανεβαίνουν: ξεκινά το παιχνίδι."""
    track = silence(0.6)
    notes = (("C", 5), ("E", 5), ("G", 5), ("C", 6))
    for index in range(len(notes)):
        letter, octave = notes[index]
        add_at(track, tone(pitch(letter, octave), 0.15, "square", decay=8), 0.15 * index)
    return scaled(track, 0.5)


def make_point():
    """Δύο γρήγορες νότες: ένας αστεροειδής πέρασε."""
    track = silence(0.15)
    add_at(track, tone(pitch("A", 5), 0.08, "triangle", decay=10), 0.0)
    add_at(track, tone(pitch("E", 6), 0.08, "triangle", decay=10), 0.07)
    return scaled(track, 0.5)


def make_hit():
    """Μια έκρηξη: θόρυβος και ένας χαμηλός τόνος που πέφτει."""
    generator = random.Random(7)
    boom = tone(180, 0.4, "square", decay=6, end_frequency=45)
    track = silence(0.4)
    for index in range(len(track)):
        noise = generator.uniform(-1, 1) * math.exp(-9 * index / RATE)
        track[index] = 0.6 * noise + 0.5 * boom[index]
    return scaled(track, 0.8)


def make_game_over():
    """Τέσσερις νότες που κατεβαίνουν: τέλος παιχνιδιού."""
    track = silence(1.4)
    notes = (("G", 4), ("E", 4), ("C", 4), ("G", 3))
    for index in range(len(notes)):
        letter, octave = notes[index]
        add_at(track, tone(pitch(letter, octave), 0.5, "triangle", decay=3), 0.3 * index)
    return scaled(track, 0.6)


def make_music():
    """Μουσική 16 δευτερολέπτων (120 παλμοί το λεπτό): κάθε συγχορδία διαρκεί 4 δευτερόλεπτα. Ξαναρχίζει ομαλά από την αρχή."""
    track = silence(16.0)
    for number in range(len(CHORDS)):
        bass, notes = CHORDS[number]
        start = 4.0 * number
        for step in range(len(PATTERN)):
            letter, octave = notes[PATTERN[step]]
            add_at(track, tone(pitch(letter, octave), 0.25, "triangle", decay=5, volume=0.5), start + 0.25 * step)
        for beat in range(4):
            add_at(track, tone(pitch(bass[0], bass[1]), 0.9, "sine", decay=2.5, volume=0.7), start + 1.0 * beat)
    return scaled(track, 0.6)


def main():
    os.makedirs(FOLDER, exist_ok=True)
    sounds = (
        ("click.wav", make_click()),
        ("start.wav", make_start()),
        ("point.wav", make_point()),
        ("hit.wav", make_hit()),
        ("game_over.wav", make_game_over()),
        ("music.wav", make_music()),
    )
    for name, samples in sounds:
        path = os.path.join(FOLDER, name)
        write_wave(path, samples)
        print(f"Γράφτηκε το {path} ({len(samples) / RATE:.2f} s)")


if __name__ == "__main__":
    main()
