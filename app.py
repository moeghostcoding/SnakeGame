import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


# Set screen dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('MGC Snake Game')

# Snake parameters
snake_block = 10
snake_speed = 15

# Enemy parameters
enemy_block = 10
enemy_speed = 25
enemies = []

# Level parameters
level = 1
level_change_threshold = 5  # Increase level every 5 points

# Fonts and text
font_style = pygame.font.SysFont(None, 50)

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# Function to draw enemies
def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(dis, black, [enemy[0], enemy[1], enemy_block, enemy_block])

# Function to display the score and level
def Your_score(score, level):
    value = font_style.render("Your Score: " + str(score) + "  Level: " + str(level), True, white)
    dis.blit(value, [0, 0])

# Function to run the game
def gameLoop():
    global snake_speed, enemy_speed, level
    game_over = False
    game_close = False
    level = 1

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Initial enemies
    for _ in range(5):
        enemyx = round(random.randrange(0, dis_width - enemy_block) / 10.0) * 10.0
        enemyy = round(random.randrange(0, dis_height - enemy_block) / 10.0) * 10.0
        enemies.append([enemyx, enemyy])

    snake_head = [x1, y1]  # Initialize snake_head

    while not game_over:

        while game_close:
            dis.fill(blue)
            Your_score(length_of_snake - 1, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > dis_height:
                enemy[1] = 0
                enemy[0] = round(random.randrange(0, dis_width - enemy_block) / 10.0) * 10.0

            # Check for collisions between snake and enemies
            if (
                snake_head[0] < enemy[0] + enemy_block
                and snake_head[0] + snake_block > enemy[0]
                and snake_head[1] < enemy[1] + enemy_block
                and snake_head[1] + snake_block > enemy[1]
            ):
                game_close = True

        draw_enemies(enemies)

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)

        Your_score(length_of_snake - 1, level)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

            if length_of_snake % level_change_threshold == 0:
                level += 1
                snake_speed += 5
                enemy_speed += 2

        pygame.display.update()

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
gameLoop()
