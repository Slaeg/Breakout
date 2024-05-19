import pgzrun
import random

# Game constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = WIDTH // BRICK_WIDTH - 2  # Two columns fewer to leave space on the sides
BRICK_START_X = BRICK_WIDTH  # Start one brick width in from the left
BRICK_START_Y = BRICK_HEIGHT  # Start one brick height down from the top
MAX_BOUNCE_ANGLE = 45  # Max bounce angle in degrees
MIN_BALL_SPEED_Y = 2  # Minimum vertical speed of the ball

# Game objects
paddle = Rect((WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30), (PADDLE_WIDTH, PADDLE_HEIGHT))  # type: ignore
ball = Rect((WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))  # type: ignore
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# Bricks
bricks = [Rect((BRICK_START_X + col * BRICK_WIDTH, BRICK_START_Y + row * BRICK_HEIGHT), (BRICK_WIDTH, BRICK_HEIGHT)) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]  # type: ignore

def draw():
    screen.clear()  # type: ignore
    screen.draw.rect(paddle, 'white')  # type: ignore
    screen.draw.filled_rect(ball, 'white')  # type: ignore

    for brick in bricks:
        screen.draw.filled_rect(brick, 'white')  # type: ignore

def update():
    update_paddle()
    update_ball()
    check_ball_brick_collision()

def update_paddle():
    if keyboard.left and paddle.left > 0:  # type: ignore
        paddle.x -= PADDLE_SPEED
    if keyboard.right and paddle.right < WIDTH:  # type: ignore
        paddle.x += PADDLE_SPEED

def update_ball():
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with left/right
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]

    # Ball collision with top
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddle
    if ball.colliderect(paddle):  # type: ignore
        bounce_ball_off_paddle()

    # Ball goes out of bounds (bottom)
    if ball.bottom >= HEIGHT:
        reset_ball()

def check_ball_brick_collision():
    global bricks
    for brick in bricks:
        if ball.colliderect(brick):  # type: ignore
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            break

def bounce_ball_off_paddle():
    offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH / 2)
    bounce_angle = offset * MAX_BOUNCE_ANGLE
    ball_speed[0] = BALL_SPEED_X * (1 if ball_speed[0] > 0 else -1)  # Maintain horizontal direction
    ball_speed[1] = -BALL_SPEED_Y

    # Adjust vertical speed based on offset but ensure it's above the minimum speed
    if offset != 0:
        ball_speed[0] = BALL_SPEED_X * offset

def reset_ball():
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed[0] = BALL_SPEED_X if random.choice([True, False]) else -BALL_SPEED_X
    ball_speed[1] = BALL_SPEED_Y

pgzrun.go()

