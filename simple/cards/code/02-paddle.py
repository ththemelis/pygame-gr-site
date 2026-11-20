"""Breakout, Κάρτα 2: η μπάλα αναπηδά στη ρακέτα."""
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

BACKGROUND = (25, 35, 60)
GREEN = (90, 220, 150)
YELLOW = (250, 220, 90)
WHITE = (245, 245, 245)
GREY = (120, 130, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


# ===== 2. ΕΡΓΑΛΕΙΑ: έτοιμες συναρτήσεις. Μην τις πειράξεις =====
def make_paddle():
    """Φτιάχνει το ορθογώνιο της ρακέτας, κάτω στη μέση του παραθύρου."""
    return pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)


def make_ball():
    """Φτιάχνει το ορθογώνιο της μπάλας, πάνω από τη μέση της ρακέτας."""
    return pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT - 40 - BALL_SIZE, BALL_SIZE, BALL_SIZE)


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
state = "playing"          # η κατάσταση του παιχνιδιού: για τώρα μόνο "playing"
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
    keys = pygame.key.get_pressed()       # ποια πλήκτρα κρατιούνται πατημένα αυτή τη στιγμή

    # ----- Β. ΕΝΗΜΕΡΩΣΗ: αλλάζουμε τα δεδομένα -----
    if (not paused or step_once) and state == "playing":
        frame += 1
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED
        # όρια: αν ένα άκρο της ρακέτας ξεπεράσει ένα όριο, τη βάζουμε ακριβώς πάνω στο όριο
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > WIDTH:
            paddle.right = WIDTH
        ball.x += ball_dx
        ball.y += ball_dy
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
        if ball.bottom > HEIGHT:          # ΠΡΟΣΩΡΙΝΟ: μέχρι την κάρτα «Ζωές» η μπάλα αναπηδά και κάτω
            ball.bottom = HEIGHT
            ball_dy = -ball_dy
        # η ρακέτα: αν η μπάλα πέφτει και ακουμπήσει τη ρακέτα, αναπηδά προς τα πάνω
        if ball.colliderect(paddle) and ball_dy > 0:
            ball.bottom = paddle.top
            ball_dy = -ball_dy
        step_once = False

    # ----- Γ. ΣΧΕΔΙΑΣΗ: ζωγραφίζουμε τα δεδομένα -----
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, GREY, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 2)
    pygame.draw.rect(screen, GREEN, paddle)
    pygame.draw.circle(screen, YELLOW, ball.center, BALL_SIZE // 2)
    draw_watch(screen, small_font, [("frame", frame), ("ball", ball), ("ball_dx", ball_dx), ("ball_dy", ball_dy)])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
