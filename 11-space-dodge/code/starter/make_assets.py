"""Φτιάχνει με κώδικα τις εικόνες του Μαθήματος 11 και τις αποθηκεύει στον φάκελο assets.

Τρέξε το μία φορά, από τον φάκελο του μαθήματος:  python make_assets.py

Δεν χρειάζεται να καταλάβεις πώς δουλεύει. Δείχνει όμως ότι μια εικόνα είναι απλώς pixel και ότι τα pixel μπορεί να τα
φτιάξει ένας κώδικας. Κάθε εικόνα ζωγραφίζεται τέσσερις φορές μεγαλύτερη και μετά μικραίνει, ώστε οι ακμές να βγουν ομαλές.
Μπορείς να αλλάξεις χρώματα και σχήματα και να τρέξεις το πρόγραμμα ξανά. Κράτα τα ονόματα και τα μεγέθη των αρχείων.
"""
import math
import os
import random

import pygame

BIG = 4                        # πόσες φορές μεγαλύτερη ζωγραφίζεται κάθε εικόνα, πριν μικρύνει
FOLDER = "assets"


def big_points(points):
    """Μεγεθύνει μια λίστα σημείων κατά BIG."""
    result = []
    for x, y in points:
        result.append((x * BIG, y * BIG))
    return result


def mirror(points, width):
    """Το κατοπτρικό είδωλο μιας λίστας σημείων ως προς τον κατακόρυφο άξονα μιας εικόνας πλάτους width."""
    result = []
    for x, y in points:
        result.append((width - x, y))
    return result


def transparent_canvas(width, height, edge_color):
    """Διάφανη επιφάνεια τετραπλάσιου μεγέθους. Τα διάφανα pixel παίρνουν το χρώμα της ακμής, ώστε να μη μαυρίζουν τα άκρα."""
    canvas = pygame.Surface((width * BIG, height * BIG), pygame.SRCALPHA)
    canvas.fill((edge_color[0], edge_color[1], edge_color[2], 0))
    return canvas


def finish(canvas, width, height):
    """Μικραίνει την επιφάνεια στο τελικό μέγεθος, με εξομάλυνση."""
    return pygame.transform.smoothscale(canvas, (width, height))


def make_ship():
    """Το διαστημόπλοιο, 128 x 96 pixel, με τη μύτη προς τα πάνω."""
    outline = (40, 50, 80)
    canvas = transparent_canvas(128, 96, outline)

    flame_outer = [(56, 78), (72, 78), (64, 95)]
    flame_inner = [(60, 78), (68, 78), (64, 88)]
    pygame.draw.polygon(canvas, (255, 150, 40), big_points(flame_outer))
    pygame.draw.polygon(canvas, (255, 232, 130), big_points(flame_inner))

    left_wing = [(53, 44), (8, 72), (8, 86), (30, 80), (53, 74)]
    right_wing = mirror(left_wing, 128)
    for wing in (left_wing, right_wing):
        pygame.draw.polygon(canvas, (70, 110, 205), big_points(wing))
        pygame.draw.polygon(canvas, outline, big_points(wing), 2 * BIG)

    left_stripe = [(10, 74), (18, 69), (18, 84), (10, 84)]
    right_stripe = mirror(left_stripe, 128)
    for stripe in (left_stripe, right_stripe):
        pygame.draw.polygon(canvas, (225, 70, 70), big_points(stripe))

    body = [(64, 3), (74, 22), (78, 58), (74, 80), (54, 80), (50, 58), (54, 22)]
    pygame.draw.polygon(canvas, (205, 215, 232), big_points(body))
    pygame.draw.polygon(canvas, outline, big_points(body), 2 * BIG)
    pygame.draw.polygon(canvas, (240, 245, 255), big_points([(64, 8), (68, 24), (66, 70), (60, 70), (60, 24)]))

    pygame.draw.ellipse(canvas, (105, 220, 255), (56 * BIG, 22 * BIG, 16 * BIG, 26 * BIG))
    pygame.draw.ellipse(canvas, outline, (56 * BIG, 22 * BIG, 16 * BIG, 26 * BIG), 2 * BIG)
    pygame.draw.ellipse(canvas, (225, 250, 255), (60 * BIG, 26 * BIG, 5 * BIG, 9 * BIG))

    pygame.draw.rect(canvas, (225, 70, 70), (54 * BIG, 70 * BIG, 20 * BIG, 5 * BIG))
    return finish(canvas, 128, 96)


def rock_outline(generator, center_x, center_y, radius_x, radius_y, corners, roughness):
    """Τα σημεία ενός ακανόνιστου βράχου γύρω από το κέντρο, σε μονάδες της τελικής εικόνας."""
    points = []
    for index in range(corners):
        angle = 2 * math.pi * index / corners + generator.uniform(-0.12, 0.12)
        factor = 1 - roughness * generator.random()
        points.append((center_x + radius_x * factor * math.cos(angle), center_y + radius_y * factor * math.sin(angle)))
    return points


def make_asteroid(width, height, seed, rock_color, shadow_color, light_color):
    """Ένας αστεροειδής με κρατήρες, width x height pixel. Το seed καθορίζει το σχήμα του και είναι πάντα το ίδιο."""
    generator = random.Random(seed)
    outline = (shadow_color[0] // 2, shadow_color[1] // 2, shadow_color[2] // 2)
    canvas = transparent_canvas(width, height, outline)
    center_x = width / 2
    center_y = height / 2
    rock = rock_outline(generator, center_x, center_y, width / 2 - 3, height / 2 - 3, 13, 0.22)
    pygame.draw.polygon(canvas, rock_color, big_points(rock))

    # Οι σκιές, οι φωτεινές περιοχές και οι κρατήρες ζωγραφίζονται χωριστά και κόβονται στο σχήμα του βράχου
    shading = pygame.Surface(canvas.get_size(), pygame.SRCALPHA)
    light = rock_outline(generator, center_x - width * 0.10, center_y - height * 0.10, width * 0.34, height * 0.34, 9, 0.2)
    pygame.draw.polygon(shading, light_color, big_points(light))
    shadow = rock_outline(generator, center_x + width * 0.20, center_y + height * 0.22, width * 0.34, height * 0.30, 9, 0.2)
    pygame.draw.polygon(shading, shadow_color, big_points(shadow))
    craters = ((0.34, 0.62, 0.13), (0.66, 0.34, 0.10), (0.58, 0.72, 0.08), (0.30, 0.32, 0.07))
    for relative_x, relative_y, relative_radius in craters:
        crater_x = int(relative_x * width * BIG)
        crater_y = int(relative_y * height * BIG)
        crater_radius = int(relative_radius * min(width, height) * BIG)
        pygame.draw.circle(shading, shadow_color, (crater_x, crater_y), crater_radius)
        pygame.draw.circle(shading, light_color, (crater_x - crater_radius // 4, crater_y - crater_radius // 4), crater_radius // 2)
    silhouette = pygame.Surface(canvas.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(silhouette, (255, 255, 255, 255), big_points(rock))
    shading.blit(silhouette, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    canvas.blit(shading, (0, 0))
    pygame.draw.polygon(canvas, outline, big_points(rock), 2 * BIG)
    return finish(canvas, width, height)


def make_background():
    """Το διάστημα: 640 x 480 pixel, χωρίς διαφάνεια. Ντεγκραντέ, δύο αχνά νεφελώματα και αστέρια."""
    width = 640
    height = 480
    generator = random.Random(11)
    surface = pygame.Surface((width, height))
    for y in range(height):
        mix = 1 - abs(2 * y / (height - 1) - 1)        # 0 στα δύο άκρα και 1 στη μέση, ώστε η εικόνα να ενώνεται με τον εαυτό της
        color = (int(6 + 18 * mix), int(8 + 10 * mix), int(26 + 34 * mix))
        pygame.draw.line(surface, color, (0, y), (width - 1, y))
    for center, radius, color in (((150, 330), 200, (110, 50, 170, 6)), ((520, 150), 170, (30, 120, 190, 5))):
        haze = pygame.Surface((width, height), pygame.SRCALPHA)
        for shift in (-height, 0, height):             # το νεφέλωμα συνεχίζεται από την κάτω άκρη στην πάνω
            for step in range(16):
                ring = int(radius * (1 - step / 16))
                pygame.draw.circle(haze, color, (center[0], center[1] + shift), ring)
        surface.blit(haze, (0, 0))
    for index in range(150):
        x = generator.randint(0, width - 1)
        y = generator.randint(0, height - 1)
        level = generator.randint(110, 255)
        surface.set_at((x, y), (level, level, min(255, level + 20)))
    for index in range(40):
        x = generator.randint(1, width - 3)
        y = generator.randint(1, height - 3)
        level = generator.randint(150, 255)
        pygame.draw.rect(surface, (level, level, 255), (x, y, 2, 2))
    for index in range(7):
        x = generator.randint(6, width - 7)
        y = generator.randint(6, height - 7)
        pygame.draw.line(surface, (210, 220, 255), (x - 4, y), (x + 4, y))
        pygame.draw.line(surface, (210, 220, 255), (x, y - 4), (x, y + 4))
        surface.set_at((x, y), (255, 255, 255))
    return surface


def main():
    os.makedirs(FOLDER, exist_ok=True)
    images = (
        ("background.png", make_background()),
        ("ship.png", make_ship()),
        ("asteroid-1.png", make_asteroid(96, 96, 1, (128, 112, 100), (92, 80, 72), (168, 152, 136))),
        ("asteroid-2.png", make_asteroid(120, 84, 2, (112, 118, 134), (80, 84, 100), (156, 162, 180))),
    )
    for name, surface in images:
        path = os.path.join(FOLDER, name)
        pygame.image.save(surface, path)
        print(f"Γράφτηκε το {path} ({surface.get_width()} x {surface.get_height()})")


if __name__ == "__main__":
    main()
