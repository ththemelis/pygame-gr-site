"""Στάδιο 2 — Οι κλάσεις Paddle και Ball: δύο ρακέτες και μια μπάλα που αναπηδά.

Συμπλήρωσε τα έξι κενά (____). Η κλάση Paddle δίνεται έτοιμη· τη δική σου εκδοχή της τη γράφεις στην άσκηση του κύκλου.
Η μπάλα προς το παρόν αναπηδά και στις τέσσερις πλευρές.
"""
import pygame

pygame.init()

WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 80
PADDLE_SPEED = 360         # pixel το δευτερόλεπτο
MARGIN = 24                # απόσταση της ρακέτας από την άκρη του παραθύρου
BALL_RADIUS = 10
PADDLE_START_Y = HUD_HEIGHT + (HEIGHT - HUD_HEIGHT - PADDLE_HEIGHT) / 2
MIDDLE_Y = (HUD_HEIGHT + HEIGHT) / 2
MAX_DT = 0.05

BACKGROUND = (25, 35, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)
BLUE = (110, 170, 255)
ORANGE = (255, 170, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()


def bounce(position, speed, low, high):
    """Αν η θέση βγήκε από τα όρια, την επαναφέρει στο όριο και αντιστρέφει την ταχύτητα. Επιστρέφει (θέση, ταχύτητα)."""
    if position < low:
        return low, -speed
    if position > high:
        return high, -speed
    return position, speed


def key_direction(up_pressed, down_pressed):
    """-1 αν πατιέται μόνο το πάνω πλήκτρο, 1 αν πατιέται μόνο το κάτω, και 0 σε κάθε άλλη περίπτωση."""
    if up_pressed and not down_pressed:
        return -1
    if down_pressed and not up_pressed:
        return 1
    return 0


class Paddle:
    """Μια ρακέτα: θέση (πάνω αριστερή γωνία), μέγεθος, ταχύτητα, όρια κίνησης και πόντοι."""

    def __init__(self, x, y, width, height, speed, top, bottom):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.top = top
        self.bottom = bottom
        self.score = 0

    def move(self, direction, dt):
        """Μετακινεί τη ρακέτα (direction: -1 πάνω, 0 ακίνητη, 1 κάτω) και την κρατά μέσα στα όρια."""
        self.y += direction * self.speed * dt
        self.y = max(self.top, min(self.y, self.bottom - self.height))

    def center_y(self):
        """Το y του κέντρου της ρακέτας."""
        return self.y + self.height / 2

    def box(self):
        """Το ορθογώνιο της ρακέτας ως (x, y, πλάτος, ύψος), με το y στρογγυλοποιημένο."""
        return (self.x, round(self.y), self.width, self.height)

    def add_point(self):
        """Ένας πόντος παραπάνω."""
        self.score += 1


class Ball:
    """Η μπάλα: θέση του κέντρου, ακτίνα και ταχύτητα (σε pixel το δευτερόλεπτο)."""

    # TODO 1: κάθε μέθοδος παίρνει ως πρώτη παράμετρο το ίδιο το αντικείμενο
    def __init__(____, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 300
        self.vy = 180

    def update(self, dt):
        """Μετακινεί την μπάλα. Προς το παρόν αναπηδά και στις τέσσερις πλευρές της περιοχής του παιχνιδιού."""
        # TODO 2: ταχύτητα επί χρόνο ανά καρέ
        self.x += self.vx * ____
        self.y += self.vy * dt
        self.x, self.vx = bounce(self.x, self.vx, self.radius, WIDTH - self.radius)
        self.y, self.vy = bounce(self.y, self.vy, HUD_HEIGHT + self.radius, HEIGHT - self.radius)


def draw_paddle(surface, paddle, color):
    """Ζωγραφίζει τη ρακέτα με το χρώμα color."""
    pygame.draw.rect(surface, color, paddle.box())


def draw_ball(surface, ball):
    """Ζωγραφίζει την μπάλα."""
    pygame.draw.circle(surface, WHITE, (ball.x, ball.y), ball.radius)


left = Paddle(MARGIN, PADDLE_START_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, HUD_HEIGHT, HEIGHT)
right = Paddle(WIDTH - MARGIN - PADDLE_WIDTH, PADDLE_START_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, HUD_HEIGHT, HEIGHT)
# TODO 3: φτιάχνεις ένα αντικείμενο καλώντας το όνομα της κλάσης
ball = ____(WIDTH / 2, MIDDLE_Y, BALL_RADIUS)

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # TODO 4: η μέθοδος της ρακέτας που τη μετακινεί
    left.____(key_direction(keys[pygame.K_w], keys[pygame.K_s]), dt)
    # TODO 5: το κάτω βέλος
    right.move(key_direction(keys[pygame.K_UP], keys[pygame.____]), dt)
    # TODO 6: η μέθοδος της μπάλας που τη μετακινεί
    ball.____(dt)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_paddle(screen, left, BLUE)
    draw_paddle(screen, right, ORANGE)
    draw_ball(screen, ball)
    pygame.display.flip()

pygame.quit()
