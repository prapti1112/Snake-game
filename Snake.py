import pygame
import random

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake")
# Used to update the screen every time there is a change on the screen
pygame.display.update()

# Initializing the font of the score displayed on the screen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def wellcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        text_screen("Welcome to Snakes", black, 250, 150)
        text_screen("Press Spacebar to Play", black, 220, 220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()

        pygame.display.update()
        clock.tick(60)


# Game loop
def gameLoop():

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1
    with open("HighScore.txt", "r") as f:
        highScore = f.read()

    score = 0
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    snake_size = 15
    fps = 30

    while not exit_game:
        if game_over:
            with open("HighScore.txt", "w") as f:
                f.write(str(highScore))
            gameWindow.fill(white)
            text_screen("GAME OVER!!! Please Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wellcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:  # gives true when a key is pressed
                    if event.key == pygame.K_RIGHT:  # moves the head of the snake on the right when the right arrow key is pressed
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:  # moves the head of the snake on the left when the left arrow key is pressed
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:  # moves the head of the snake on the up when the up arrow key is pressed
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:  # moves the head of the snake on the down when the down arrow key is pressed
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_s:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            gameWindow.fill(white)
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                snake_length += 5
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                if score > int(highScore):
                    highScore = score

            text_screen("Score: " + str(score) +
                        "    High Score: " + str(highScore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [
                             food_x, food_y, snake_size+10, snake_size+10])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            pygame.draw.rect(gameWindow, black, [
                             snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


wellcome()
gameLoop()
