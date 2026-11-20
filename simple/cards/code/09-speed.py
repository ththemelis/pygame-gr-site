"""Breakout, Κάρτα 9: η μπάλα επιταχύνει όσο ανεβαίνει το σκορ."""
import pygame

pygame.init()

# ===== 1. ΡΥΘΜΙΣΕΙΣ: οι σταθερές. Εδώ αλλάζεις μεγέθη, χρώματα και ταχύτητες =====
WIDTH = 640
HEIGHT = 480
HUD_HEIGHT = 60            # πάνω από τη γραμμή αυτή είναι ο χώρος των κειμένων
PADDLE_WIDTH = 90
PADDLE_HEIGHT = 14
PADDLE_SPEED = 7           # pixel ανά καρέ για τη ρακέτα
BALL_SIZE = 14
BALL_SPEED = 4             # pixel ανά καρέ για την μπάλα, σε κάθε άξονα
BRICK_COLUMNS = 8          # πόσα τούβλα έχει κάθε σειρά
BRICK_ROWS = 4             # πόσες σειρές τούβλων υπάρχουν
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_GAP = 6              # το κενό ανάμεσα στα τούβλα
BRICK_TOP = 90             # πόσο χαμηλά ξεκινά η πρώτη σειρά
POINTS = 10                # οι πόντοι για κάθε τούβλο που σπάει
LIVES = 3                  # οι ζωές με τις οποίες ξεκινά ο παίκτης
MAX_BALL_SPEED = 8         # η μεγαλύτερη ταχύτητα της μπάλας
LEVEL_SCORE = 50           # κάθε τόσους πόντους η μπάλα επιταχύνει κατά 1

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
YELLOW = (250, 220, 90)
RED = (220, 60, 60)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
def make_paddle():
    """Φτιάχνει το ορθογώνιο της ρακέτας, κάτω στη μέση του παραθύρου."""
    return pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)


def make_ball():
    """Φτιάχνει το ορθογώνιο της μπάλας, πάνω από τη μέση της ρακέτας."""
    return pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT - 40 - BALL_SIZE, BALL_SIZE, BALL_SIZE)


def make_bricks():
    """Φτιάχνει τη λίστα με τα τούβλα: BRICK_ROWS σειρές των BRICK_COLUMNS τούβλων, κάτω από τη γραμμή HUD_HEIGHT."""
    bricks = []
    left = (WIDTH - (BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP)) // 2
    for row in range(BRICK_ROWS):
        for column in range(BRICK_COLUMNS):
            x = left + column * (BRICK_WIDTH + BRICK_GAP)
            y = BRICK_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
            bricks.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks


def draw_text(surface, font, text, color, position):
    """Ζωγραφίζει το κείμενο, με την πάνω αριστερή γωνία του στο position."""
    image = font.render(text, True, color)
    surface.blit(image, position)


def draw_centered_text(surface, font, text, color, center):
    """Ζωγραφίζει το κείμενο, με το κέντρο του στο center."""
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def draw_watch(surface, font, lines):
    """Δείχνει κάτω αριστερά τις τιμές που παρακολουθούμε (λίστα από ζεύγη όνομα-τιμή) και πάνω δεξιά τα πλήκτρα του βοηθού."""
    hint = font.render("P: παύση    N: ένα καρέ", True, GREY)
    surface.blit(hint, (WIDTH - hint.get_width() - 10, 8))
    y = HEIGHT - 28 * len(lines) - 6
    for name, value in lines:
        image = font.render(f"{name} = {value}", True, WHITE)
        surface.blit(image, (10, y))
        y += 28


# ===== 3. ΔΕΔΟΜΕΝΑ: οι μεταβλητές που αλλάζουν όσο τρέχει το παιχνίδι =====
paddle = make_paddle()
ball = make_ball()
ball_dx = BALL_SPEED       # πόσα pixel μετακινείται η μπάλα οριζόντια σε κάθε καρέ (αρνητικό: προς τα αριστερά)
ball_dy = -BALL_SPEED      # πόσα pixel μετακινείται η μπάλα κάθετα σε κάθε καρέ (αρνητικό: προς τα πάνω)
bricks = make_bricks()
score = 0
lives = LIVES
launched = False          # True: η μπάλα έχει φύγει από τη ρακέτα· False: περιμένει πάνω της
ball_speed = BALL_SPEED   # η ταχύτητα της μπάλας σε αυτό το καρέ: εξαρτάται από το σκορ
state = "playing"          # η κατάσταση του παιχνιδιού: "playing", "game over" ή "won"
frame = 0
paused = False             # True: το πρόγραμμα ξεκινά σταματημένο και προχωρά με το N
step_once = False

running = True
while running:
    # ===== 4. Ο ΒΡΟΧΟΣ: ένα καρέ σε κάθε επανάληψη =====
    # ----- Α. ΣΥΜΒΑΝΤΑ: τι έκανε ο παίκτης -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_n:
                step_once = True
            elif state == "playing" and event.key == pygame.K_SPACE:
                launched = True
            elif state != "playing" and event.key == pygame.K_SPACE:
                # νέο παιχνίδι: όλα τα δεδομένα ξαναγυρίζουν στην αρχική τους τιμή
                paddle = make_paddle()
                ball = make_ball()
                ball_dx = BALL_SPEED
                ball_dy = -BALL_SPEED
                bricks = make_bricks()
                score = 0
                lives = LIVES
                launched = False
                state = "playing"
    keys = pygame.key.get_pressed()       # ποια πλήκτρα κρατιούνται πατημένα αυτή τη στιγμή

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if (not paused or step_once) and state == "playing":
        frame += 1
        # η ταχύτητα της μπάλας μεγαλώνει με το σκορ, αλλά έχει όριο· κρατάμε την κατεύθυνση του ball_dy
        ball_speed = BALL_SPEED + score // LEVEL_SCORE
        ball_speed = min(ball_speed, MAX_BALL_SPEED)
        if ball_dy > 0:
            ball_dy = ball_speed
        else:
            ball_dy = -ball_speed
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED
        # όρια: αν ένα άκρο της ρακέτας ξεπεράσει ένα όριο, τη βάζουμε ακριβώς πάνω στο όριο
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > WIDTH:
            paddle.right = WIDTH
        if launched:
            ball.x += ball_dx
            ball.y += ball_dy
        else:
            ball.centerx = paddle.centerx
            ball.bottom = paddle.top
        # τοίχοι: αν η μπάλα ξεπεράσει ένα όριο, τη βάζουμε ακριβώς πάνω στο όριο και αναποδογυρίζουμε την κατεύθυνσή της
        if ball.left < 0:
            ball.left = 0
            ball_dx = -ball_dx
        if ball.right > WIDTH:
            ball.right = WIDTH
            ball_dx = -ball_dx
        if ball.top < HUD_HEIGHT:
            ball.top = HUD_HEIGHT
            ball_dy = -ball_dy
        # η ρακέτα: αν η μπάλα πέφτει και ακουμπήσει τη ρακέτα, αναπηδά προς τα πάνω
        if ball.colliderect(paddle) and ball_dy > 0:
            ball.bottom = paddle.top
            ball_dy = -ball_dy
            ball_dx = (ball.centerx - paddle.centerx) // 10     # όσο πιο μακριά από το κέντρο, τόσο πιο λοξά
            if ball_dx == 0:
                ball_dx = 1
        # τα τούβλα: αν η μπάλα ακουμπήσει ένα, το σβήνουμε από τη λίστα, παίρνουμε πόντους και η μπάλα αναπηδά
        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)
                score += POINTS
                ball_dy = -ball_dy
                break                     # η λίστα άλλαξε μέσα στον βρόχο που τη διαβάζει: σταματάμε εδώ
        if len(bricks) == 0:
            state = "won"
        # αν η μπάλα βγει κάτω από το παράθυρο, χάνουμε μία ζωή και η μπάλα ξαναρχίζει
        if ball.top > HEIGHT:
            lives -= 1
            ball = make_ball()
            ball_dx = BALL_SPEED
            ball_dy = -BALL_SPEED
            launched = False
        if lives == 0:
            state = "game over"
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    draw_text(screen, font, f"Σκορ: {score}", WHITE, (20, 30))
    draw_text(screen, font, f"Ζωές: {lives}", WHITE, (220, 30))
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    pygame.draw.rect(screen, GREEN, paddle)
    pygame.draw.circle(screen, YELLOW, ball.center, BALL_SIZE // 2)
    if state == "game over":
        draw_centered_text(screen, font, "Τέλος παιχνιδιού", WHITE, (WIDTH // 2, HEIGHT // 2))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι", WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
    if state == "won":
        draw_centered_text(screen, font, "Κέρδισες", YELLOW, (WIDTH // 2, HEIGHT // 2))
        draw_centered_text(screen, font, "Πάτα SPACE για νέο παιχνίδι", WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
    draw_watch(screen, small_font, [("frame", frame), ("score", score), ("ball_speed", ball_speed), ("ball_dx", ball_dx), ("ball_dy", ball_dy)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
