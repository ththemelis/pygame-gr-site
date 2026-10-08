"""Στάδιο 3 — Συγκρούσεις, γωνία αναπήδησης, πόντοι και σερβίς.

Συμπλήρωσε τα οκτώ κενά (____). Η μπάλα αναπηδά στις ρακέτες με γωνία που εξαρτάται από το σημείο που χτύπησε, και όταν
βγει ολόκληρη από το παράθυρο ο αντίπαλος παίρνει πόντο. Το SPACE σερβίρει την μπάλα.
"""
import random

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
BALL_START_SPEED = 300     # οριζόντια ταχύτητα της μπάλας στην αρχή κάθε πόντου
SPEED_UP = 1.08            # πολλαπλασιαστής της ταχύτητας σε κάθε χτύπημα ρακέτας
MAX_BALL_SPEED = 600
MAX_VY = 280               # κάθετη ταχύτητα όταν η μπάλα χτυπά την άκρη της ρακέτας
SERVE_VY = 150             # η κάθετη ταχύτητα του σερβίς είναι τυχαία από -SERVE_VY έως SERVE_VY
PADDLE_START_Y = HUD_HEIGHT + (HEIGHT - HUD_HEIGHT - PADDLE_HEIGHT) / 2
MIDDLE_Y = (HUD_HEIGHT + HEIGHT) / 2
MAX_DT = 0.05

SERVE = "serve"
PLAYING = "playing"

BACKGROUND = (25, 35, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)
BLUE = (110, 170, 255)
ORANGE = (255, 170, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.Font(None, 36)
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


def rebound_vy(ball_y, paddle_center, paddle_height, max_vy):
    """Η κάθετη ταχύτητα μετά το χτύπημα: 0 στο κέντρο της ρακέτας, ±max_vy στις άκρες της (και πέρα από αυτές)."""
    offset = (ball_y - paddle_center) / (paddle_height / 2)
    offset = max(-1, min(offset, 1))
    return offset * max_vy


def scorer(ball_x, radius, width):
    """Ποιος παίρνει πόντο: "left" αν η μπάλα βγήκε ολόκληρη από τη δεξιά πλευρά, "right" αν βγήκε από την αριστερή."""
    if ball_x < -radius:
        return "right"
    if ball_x > width + radius:
        return "left"
    return None


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
    """Η μπάλα: θέση του κέντρου, ακτίνα, ταχύτητα και συνιστώσες ταχύτητας (σε pixel το δευτερόλεπτο)."""

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = BALL_START_SPEED
        self.vx = 0
        self.vy = 0

    def reset(self):
        """Η μπάλα γυρίζει ακίνητη στο κέντρο, με την αρχική ταχύτητα."""
        self.x = WIDTH / 2
        self.y = MIDDLE_Y
        self.speed = BALL_START_SPEED
        self.vx = 0
        self.vy = 0

    def serve(self, direction):
        """Ξεκινά την κίνηση προς την direction (-1 αριστερά, 1 δεξιά), με τυχαία κάθετη ταχύτητα."""
        self.vx = direction * self.speed
        # TODO 1: τυχαίος ακέραιος από -SERVE_VY έως SERVE_VY (και τα δύο άκρα περιλαμβάνονται)
        self.vy = random.____(-SERVE_VY, SERVE_VY)

    def update(self, dt):
        """Μετακινεί την μπάλα και την κάνει να αναπηδά στον πάνω και στον κάτω τοίχο."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.y, self.vy = bounce(self.y, self.vy, HUD_HEIGHT + self.radius, HEIGHT - self.radius)

    def box(self):
        """Το τετράγωνο που περικλείει την μπάλα, ως (x, y, πλάτος, ύψος)."""
        return (round(self.x - self.radius), round(self.y - self.radius), 2 * self.radius, 2 * self.radius)

    def touches(self, paddle):
        """True αν η μπάλα και η ρακέτα επικαλύπτονται."""
        # TODO 2: η μέθοδος του Rect που ελέγχει αν δύο ορθογώνια επικαλύπτονται
        return pygame.Rect(self.box()).____(paddle.box())

    def bounce_off(self, paddle, direction):
        """Αναπήδηση πάνω στη ρακέτα: η μπάλα φεύγει προς την direction, πιο γρήγορα, με γωνία που εξαρτάται από το
        σημείο της ρακέτας που χτύπησε."""
        # TODO 3: η ταχύτητα μεγαλώνει, αλλά ποτέ πάνω από το MAX_BALL_SPEED
        self.speed = ____(self.speed * SPEED_UP, MAX_BALL_SPEED)
        self.vx = direction * self.speed
        self.vy = rebound_vy(self.y, paddle.center_y(), paddle.height, MAX_VY)
        if direction == 1:
            self.x = paddle.x + paddle.width + self.radius
        else:
            self.x = paddle.x - self.radius


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def draw_paddle(surface, paddle, color):
    """Ζωγραφίζει τη ρακέτα με το χρώμα color."""
    pygame.draw.rect(surface, color, paddle.box())


def draw_ball(surface, ball):
    """Ζωγραφίζει την μπάλα."""
    pygame.draw.circle(surface, WHITE, (ball.x, ball.y), ball.radius)


left = Paddle(MARGIN, PADDLE_START_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, HUD_HEIGHT, HEIGHT)
right = Paddle(WIDTH - MARGIN - PADDLE_WIDTH, PADDLE_START_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, HUD_HEIGHT, HEIGHT)
ball = Ball(WIDTH / 2, MIDDLE_Y, BALL_RADIUS)
state = SERVE
serve_direction = random.choice([-1, 1])

running = True
while running:
    dt = min(clock.tick(60) / 1000, MAX_DT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and state == SERVE:
                ball.serve(serve_direction)
                state = PLAYING

    keys = pygame.key.get_pressed()
    left.move(key_direction(keys[pygame.K_w], keys[pygame.K_s]), dt)
    right.move(key_direction(keys[pygame.K_UP], keys[pygame.K_DOWN]), dt)

    if state == PLAYING:
        ball.update(dt)
        # TODO 4: η μπάλα χτυπά την αριστερή ρακέτα μόνο όσο κινείται προς τα αριστερά (vx αρνητικό)
        if ball.vx < 0 and ball.____(left):
            # TODO 5: μετά το χτύπημα η μπάλα φεύγει προς τα δεξιά
            ball.bounce_off(left, ____)
        elif ball.vx > 0 and ball.touches(right):
            ball.bounce_off(right, -1)
        scored_by = scorer(ball.x, ball.radius, WIDTH)
        if scored_by == "left":
            # TODO 6: ο αριστερός παίκτης παίρνει έναν πόντο
            left.____()
            # TODO 7: το επόμενο σερβίς πηγαίνει προς τον παίκτη που έχασε τον πόντο (δεξιά)
            serve_direction = ____
        elif scored_by == "right":
            right.add_point()
            serve_direction = -1
        if scored_by is not None:
            ball.reset()
            # TODO 8: η μπάλα περιμένει νέο σερβίς
            state = ____

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Παίκτης 1: {left.score}", BLUE, (20, 20))
    draw_text(screen, font, f"Παίκτης 2: {right.score}", ORANGE, (WIDTH - 190, 20))
    for y in range(HUD_HEIGHT + 10, HEIGHT, 30):
        pygame.draw.line(screen, GREY, (WIDTH // 2, y), (WIDTH // 2, y + 14), 2)
    draw_paddle(screen, left, BLUE)
    draw_paddle(screen, right, ORANGE)
    draw_ball(screen, ball)
    if state == SERVE:
        draw_centered_text(screen, font, "Πάτα SPACE για σερβίς.", WHITE, (WIDTH // 2, 180))
    pygame.display.flip()

pygame.quit()
