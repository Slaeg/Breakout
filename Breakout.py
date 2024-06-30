import os
import pygame
import random

# Initialize Pygame
pygame.init()

# Center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game constants
WIDTH = 1024
HEIGHT = 768
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_INITIAL_OFFSET = 10

BALL_START_SPEED = 5
BALL_MIN_SPEED = 4
BALL_MAX_SPEED = 11

BALL_SPEED_UP_INTERVAL = 10 * 60        # Normal ball speed up interval (10 seconds at 60 frames per second)
BALL_SPEED_UP_INTERVAL_FAST = 15 * 60   # Speed up interval for when the ball is above a speed threshold
BALL_FAST_SPEED_THRESHOLD = 7

BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_ROWS = 16
BRICK_COLS = (WIDTH // BRICK_WIDTH - 2)
BRICK_START_X = BRICK_WIDTH  # Start one brick width in from the left
BRICK_START_Y = BRICK_HEIGHT  # Start one brick height down from the top
MAX_BOUNCE_ANGLE = 60  # Max bounce angle in degrees
MIN_BALL_SPEED_Y = 2  # Minimum vertical speed of the ball

# Game objects
paddle = pygame.Rect((WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30), (PADDLE_WIDTH, PADDLE_HEIGHT))
ball = pygame.Rect((paddle.centerx - BALL_SIZE // 2, paddle.top - BALL_SIZE - 1), (BALL_SIZE, BALL_SIZE))
ball_speed = [BALL_START_SPEED if random.choice([True, False]) else -BALL_START_SPEED, -BALL_START_SPEED]  # Ball moves upwards initially

# Bricks
bricks = [pygame.Rect((BRICK_START_X + col * BRICK_WIDTH, BRICK_START_Y + row * BRICK_HEIGHT), (BRICK_WIDTH, BRICK_HEIGHT)) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]

# Speed up timer
speed_up_timer = 0

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Main game loop
running = True
clock = pygame.time.Clock()

def draw():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)

    for brick in bricks:
        pygame.draw.rect(screen, (255, 255, 255), brick)
    
    pygame.display.flip()

def update():
    global speed_up_timer

    update_paddle()
    update_ball()
    check_ball_brick_collision()
    
    # Update speed up timer and ball speed
    speed_up_timer += 1
    if ball_speed[1] > BALL_FAST_SPEED_THRESHOLD:
        if speed_up_timer >= BALL_SPEED_UP_INTERVAL_FAST:
            increase_ball_speed()
            speed_up_timer = 0
    else:
        if speed_up_timer >= BALL_SPEED_UP_INTERVAL:
            increase_ball_speed()
            speed_up_timer = 0

def update_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

def update_ball():
    global ball_speed

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with left/right walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]

    # Ball collision with the top wall
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with the paddle
    if ball.colliderect(paddle):
        bounce_ball_off_paddle()

    # Ball goes out of bounds (bottom)
    if ball.bottom >= HEIGHT:
        reset_ball()

def check_ball_brick_collision():
    global bricks, ball_speed
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            break

def bounce_ball_off_paddle():
    global ball_speed
    offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH / 2)
    bounce_angle = offset * MAX_BOUNCE_ANGLE
    ball_speed[0] = BALL_START_SPEED * offset
    ball_speed[1] = -abs(ball_speed[1])  # Ensure the ball bounces upwards

    # Ensure the ball speed respects the minimum vertical speed
    if abs(ball_speed[1]) < MIN_BALL_SPEED_Y:
        ball_speed[1] = MIN_BALL_SPEED_Y if ball_speed[1] > 0 else -MIN_BALL_SPEED_Y

def reset_ball():
    global ball_speed
    # Set the ball's position to be just above the paddle
    ball.x = paddle.centerx - BALL_SIZE // 2
    ball.y = paddle.top - BALL_SIZE - 1  # Ensure the ball is not intersecting the paddle
    # Ensure the ball moves upwards towards the bricks
    ball_speed[0] = BALL_START_SPEED if random.choice([True, False]) else -BALL_START_SPEED
    ball_speed[1] = -abs(BALL_START_SPEED)  # Ensure the vertical speed is directed upwards

    # Reset the speed up timer
    speed_up_timer = 0

def increase_ball_speed():
    global ball_speed
    speed_multiplier = 1.1  # Define how much to increase the speed by (10% in this case)

    ball_speed[0] = max(min(ball_speed[0] * speed_multiplier, BALL_MAX_SPEED), -BALL_MAX_SPEED)
    ball_speed[1] = max(min(ball_speed[1] * speed_multiplier, BALL_MAX_SPEED), -BALL_MAX_SPEED)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    update()
    draw()
    clock.tick(60)

pygame.quit()
