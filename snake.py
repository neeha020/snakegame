import pygame
import random

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
dark_green = (0, 155, 0)
blue = (50, 153, 213)
orange = (255, 165, 0)
purple = (138, 43, 226)

# Display size
width = 600
height = 400

# Game window
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('🐍 Snake Game - Enhanced')

# Clock and snake block size
clock = pygame.time.Clock()
snake_block = 10
base_snake_speed = 10

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)
small_font = pygame.font.SysFont("comicsansms", 20)

# High Score
high_score = 0
session_scores = []

# Level backgrounds
level_colors = [
    (50, 153, 213),
    (100, 149, 237),
    (72, 61, 139),
    (0, 100, 0),
    (123, 104, 238),
    (220, 20, 60)
]

def get_level_color(level):
    return level_colors[min(level - 1, len(level_colors) - 1)]

# Show current score and level
def score_display(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, white)
    display.blit(value, [10, 10])

# Show high score
def high_score_display(score):
    value = score_font.render("High Score: " + str(score), True, white)
    display.blit(value, [400, 10])

# Draw snake segments
def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = dark_green if i == len(snake_list) - 1 else green
        pygame.draw.rect(display, color, [x[0], x[1], snake_block, snake_block])

# Display message
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    rect = mesg.get_rect(center=(width / 2, height / 2 + y_offset))
    display.blit(mesg, rect)

# Display achievement badge
def draw_achievement(score):
    if score >= 15:
        label = "🔥 Master!"
    elif score >= 10:
        label = "🐍 Pro!"
    elif score >= 5:
        label = "⭐ Nice Start!"
    else:
        return
    badge = small_font.render(label, True, orange)
    display.blit(badge, [width // 2 - 50, height - 30])

# Milestone alert
def flash_milestone(score):
    if score in [5, 10, 15]:
        display.fill(black)
        message(f"🎉 Milestone Reached: {score}!", yellow, 0)
        pygame.display.update()
        pygame.time.delay(1200)

# Show mini leaderboard
def show_leaderboard():
    session_scores.sort(reverse=True)
    display.fill(black)
    message("🏆 Top Scores This Session", yellow, -100)
    for i, s in enumerate(session_scores[:3]):
        score_text = font_style.render(f"{i+1}. Score: {s}", True, white)
        display.blit(score_text, [width // 2 - 100, height // 2 - 30 + i * 40])
    pygame.display.update()
    pygame.time.delay(3000)

# Main game loop
def game_loop():
    global high_score, session_scores
    game_over = False
    pause = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Bonus food logic
    bonus_food = False
    bonus_timer = 0
    bonusx, bonusy = 0, 0

    while not game_over:
        level = max(1, length_of_snake // 5)
        snake_speed = base_snake_speed + (level - 1) * 2

        while pause:
            display.fill(black)
            message("Game Paused. Press R to Resume or Q to Quit.", yellow)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pause = False
                    elif event.key == pygame.K_q:
                        game_over = True
                        pause = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause = True

        # Check for hitting walls
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        display.fill(get_level_color(level))

        # Draw food
        pygame.draw.rect(display, yellow, [foodx, foody, snake_block, snake_block])

        # Bonus food generation
        if not bonus_food and random.randint(1, 50) == 1:
            bonusx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            bonusy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            bonus_food = True
            bonus_timer = pygame.time.get_ticks()

        if bonus_food:
            pygame.draw.rect(display, red, [bonusx, bonusy, snake_block, snake_block])
            if pygame.time.get_ticks() - bonus_timer > 5000:
                bonus_food = False

        # Snake movement
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        draw_snake(snake_block, snake_list)
        score = length_of_snake - 1
        score_display(score, level)
        draw_achievement(score)
        high_score = max(high_score, score)
        high_score_display(high_score)
        pygame.display.update()

        # Eat food
        if x1 == foodx and y1 == foody:
            flash_milestone(length_of_snake)
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        # Eat bonus food
        if bonus_food and x1 == bonusx and y1 == bonusy:
            length_of_snake += 3
            bonus_food = False

        clock.tick(snake_speed)

    # Game Over Screen
    session_scores.append(length_of_snake - 1)
    display.fill(black)
    message("Game Over!", red, -30)
    message("Press C to Play Again or Q to Quit", white, 30)
    pygame.display.update()
    show_leaderboard()

    # Restart or Quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    game_loop()

# Start the game
game_loop()
