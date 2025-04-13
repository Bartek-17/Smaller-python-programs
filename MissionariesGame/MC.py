"""
Missionaries and Cannibals Game
Three missionaries and three cannibals must cross a river using a boat which can carry 
at most two people,under the constraint that, for both banks, if there are missionaries
present on the bank, they cannot be outnumbered
by cannibals.

Controls:
- Mouse click: Select Missionary 1, 2, 3
- Mouse click: Select Cannibal 1, 2, 3
- Space: Move the boat
- R: Restart the game
"""

import os
import pygame


class Boat:
    """
    Boat class represents the boat in the game.

    Attributes:
    - x: X-coordinate of the boat
    - y: Y-coordinate of the boat
    - pos: Position of the boat (indicates left/right shore and left/right of the boat)
    - gameDisplay: Pygame display surface
    """

    def __init__(self, x, y, pos, gameDisplay):
        self.x = x
        self.y = y
        self.pos = pos  # boat position
        self.gameDisplay = gameDisplay


class Person:
    """
    Person class represents a person (Missionary or Cannibal) in the game.

    Attributes:
    - x: X-coordinate of the person
    - y: Y-coordinate of the person
    - x_change: X-axis movement
    - pos: Position of the person (indicates left/right shore and left/right of the boat)
    - char: Character representing Missionary ('M') or Cannibal ('C')
    - leftright: Indicates whether the person is on the left or right side
    - image: Pygame image representing the person
    - gameDisplay: Pygame display surface
    """
    width = 50
    height = 50

    def __init__(self, x, y, x_change, pos, char, leftright, image, gameDisplay):
        self.leftright = leftright
        self.x = x
        self.y = y
        self.x_change = x_change
        self.pos = pos
        self.char = char
        self.rect_x = self.x
        self.rect_y = self.y
        self.image = image
        self.gameDisplay = gameDisplay

    def display(self):
        """Display the person on the game display."""
        self.gameDisplay.blit(self.image, (self.x, self.y))


# Pygame Initialization
pygame.init()
display_width = 800  # Half of the original width
display_height = 400  # Half of the original height
gameDisplay = pygame.display.set_mode(
    (display_width, display_height), pygame.RESIZABLE)

# Loading and Adjusting Images
imageboat = pygame.image.load('images/boat.png')
imagebackground = pygame.image.load('images/background.png')
Mimg = pygame.image.load('images/missionary.png')
Cimg = pygame.image.load('images/cannibal.png')
game_over = pygame.image.load('images/game_over.png')
Wimg = pygame.image.load('images/winner.png')

boatImg = pygame.transform.scale(imageboat, (150, 100))
bgImg = pygame.transform.scale(imagebackground, (800, 400))
Missionary = pygame.transform.scale(Mimg, (75, 75))
Cannibal = pygame.transform.scale(Cimg, (50, 75))
Game_Over = pygame.transform.scale(game_over, (200, 200))
Victory = pygame.transform.scale(Wimg, (200, 200))


def introduction_screen():
    """
    Display an introduction screen with the goal and controls.
    Press space to start the game.
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Display background image
        gameDisplay.blit(bgImg, (0, 0))

        # Display goal and controls
        font_large = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 30)

        goal_text = font_large.render(
            "Missionaries and Cannibals Game", True, (0, 0, 128))
        gameDisplay.blit(goal_text, (60, 50))

        goal_text = font_small.render(
            "Goal: Move all missionaries and cannibals to the right shore.", True, (0, 0, 0))
        gameDisplay.blit(goal_text, (100, 150))

        control_text = font_small.render("Controls:", True, (255, 160, 0))
        gameDisplay.blit(control_text, (100, 200))

        control_text = font_small.render(
            "Mouse click: Select Missionary 1, 2, 3 or Cannibal 1, 2, 3", True, (0, 0, 0))
        gameDisplay.blit(control_text, (100, 230))

        control_text = font_small.render(
            "Space: Move the boat", True, (0, 0, 0))
        gameDisplay.blit(control_text, (100, 260))

        control_text = font_small.render(
            "R: Restart the game", True, (0, 0, 0))
        gameDisplay.blit(control_text, (100, 290))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro = False

    # Clear the screen
    gameDisplay.fill((0, 0, 0))
    pygame.display.update()


def main():
    """
    Main function to run the game logic and display using Pygame.
    """
    # Initial boat coordinates
    x = 200
    y = 250
    x_change, y_change = 0, 0

    # Create instances of Person class for missionaries and cannibals
    mc = [
        Person(x - 200, y - 60, 0, 0, 'M', 'left', Missionary, gameDisplay),
        Person(x - 133, y - 60, 0, 0, 'M', 'left', Missionary, gameDisplay),
        Person(x - 70, y - 60, 0, 0, 'M', 'left', Missionary, gameDisplay),
        Person(x - 200, y, 0, 0, 'C', 'left', Cannibal, gameDisplay),
        Person(x - 133, y, 0, 0, 'C', 'left', Cannibal, gameDisplay),
        Person(x - 70, y, 0, 0, 'C', 'left', Cannibal, gameDisplay)
    ]

    # Create instances of Boat class for boat positions
    boats = [
        Boat(x + 20, y - 30, 2, Missionary),  # left shore left
        Boat(x + 200, y - 30, 3, Missionary),  # right shore left
        Boat(x + 100, y - 30, 4, Missionary),  # left shore right
        Boat(x + 280, y - 30, 5, Missionary)  # right shore right
    ]

    pygame.display.set_caption('MC GAME')
    clock = pygame.time.Clock()
    LOST = False
    boat_position = 0  # indicates boat at left shore
    a, b = 0, 0  # missionaries, cannibals
    InBoat = [a, b]  # number of missionaries and cannibals to move
    m, c, bt = 3, 3, 1  # indicates 3 missionaries, 3 cannibals and boat at left shore
    # indicates MCB of missionaries, cannibals and boat at left shore
    MCB = [m, c, bt]

    game_over = False
    game_overplayed, wonplayed = False, False
    left, right = False, False
    won = False

    # Initialize movement counter
    movement_count = 0

    while not LOST:
        # Loading background image and new game image
        gameDisplay.blit(bgImg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LOST = True

        # Loading the missionaries and cannibals image
        for i in range(6):
            mc[i].display()

        gameDisplay.blit(boatImg, (x, y))  # Display boat

        keys = pygame.key.get_pressed()  # Key input
        cursor = pygame.mouse.get_pos()  # Cursor position

        # Checking game over
        if (MCB[0] < MCB[1]) and MCB[0] > 0 or (MCB[0] > MCB[1]) and MCB[0] < 3:
            gameDisplay.blit(Game_Over, (300, 35))
            game_over = True
            if keys[pygame.K_r]:
                main()
                break

        # Checking game won
        if MCB == [0, 0, 0] and InBoat == [0, 0]:
            gameDisplay.blit(Victory, (300, 35))
            won = True

        if not game_over and not won:
            if InBoat != [0, 0]:
                if keys[pygame.K_SPACE]:
                    if boat_position == 0:
                        x_change = 10
                        for i in range(6):
                            if mc[i].pos == 2 or mc[i].pos == 4:
                                mc[i].x_change = 10  # boat movement right
                    elif boat_position == 1:
                        x_change = -10
                        for i in range(6):
                            if mc[i].pos == 3 or mc[i].pos == 5:
                                mc[i].x_change = -10  # boat movement left

            if keys[pygame.K_r]:
                main()
                break

            # Boat border
            if x >= 400 and boat_position == 0:  # Right limit
                x_change = 0
                for i in range(6):
                    mc[i].x_change = 0
                boat_position = 1
                movement_count += 1
                MCB[0], MCB[1], MCB[2] = MCB[0] - \
                    InBoat[0], MCB[1] - InBoat[1], 0
                for i in range(6):
                    if mc[i].pos == 2:
                        mc[i].pos = 3
                        mc[i].leftright = 'right'
                        mc[i].rect_x += 600

                    if mc[i].pos == 4:
                        mc[i].pos = 5
                        mc[i].leftright = 'right'
                        mc[i].rect_x += 600

            if x <= 200 and boat_position == 1:  # Left limit
                x_change = 0
                for i in range(6):
                    mc[i].x_change = 0
                boat_position = 0
                movement_count += 1
                MCB[0], MCB[1], MCB[2] = MCB[0] + \
                    InBoat[0], MCB[1] + InBoat[1], 1
                for i in range(6):
                    if mc[i].pos == 3:
                        mc[i].pos = 2
                        mc[i].rect_x -= 600
                        mc[i].leftright = 'left'

                    if mc[i].pos == 5:
                        mc[i].pos = 4
                        mc[i].leftright = 'left'
                        mc[i].rect_x -= 600

            # If boat is empty
            if InBoat != [1, 1] and InBoat != [0, 2] and InBoat != [2, 0]:
                for i in range(6):
                    # Cursor in the area of hitbox
                    if mc[i].rect_x + Person.width > cursor[0] > mc[i].rect_x and \
                            mc[i].rect_y + Person.height > cursor[1] > mc[i].rect_y:
                        if mc[i].pos == 0 and mc[i].leftright == 'left' and boat_position == 0:
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[i].char == 'M':
                                    a += 1
                                elif mc[i].char == 'C':
                                    b += 1
                                if InBoat == [0, 1] or InBoat == [1, 0]:
                                    for k in range(6):
                                        if mc[k].pos == 2:
                                            left = True
                                        if mc[k].pos == 4:
                                            right = True
                                    if left:
                                        mc[i].x, mc[i].y = x + 80, y - 30
                                        mc[i].pos = 4
                                    elif right:
                                        mc[i].x, mc[i].y = x + 10, y - 30
                                        mc[i].pos = 2
                                else:
                                    mc[i].x, mc[i].y = x + 10, y - 30
                                    mc[i].pos = 2

                        elif mc[i].pos == 1 and mc[i].leftright == 'right' and boat_position == 1:
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[i].char == 'M':
                                    a += 1
                                elif mc[i].char == 'C':
                                    b += 1
                                if InBoat == [0, 1] or InBoat == [1, 0]:
                                    for k in range(6):
                                        if mc[k].pos == 3:
                                            left = True
                                        if mc[k].pos == 5:
                                            right = True
                                    if left:
                                        mc[i].x, mc[i].y = x + 80, y - 30
                                        mc[i].pos = 5
                                    elif right:
                                        mc[i].x, mc[i].y = x + 10, y - 30
                                        mc[i].pos = 3
                                else:
                                    mc[i].x, mc[i].y = x + 10, y - 30
                                    mc[i].pos = 3

            # If 1 or more persons on the boat
            if InBoat != [0, 0]:
                for j in range(4):
                    if boats[j].x + 75 > cursor[0] > boats[j].x and boats[j].y + 75 > cursor[1] > \
                            boats[j].y:
                        k = 99
                        for i in range(6):
                            if mc[i].pos == boats[j].pos:
                                k = i
                        if k != 99:
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[k].char == 'M':
                                    a -= 1
                                elif mc[k].char == 'C':
                                    b -= 1
                                if mc[k].leftright == 'left':
                                    mc[k].x, mc[k].y = mc[k].rect_x - \
                                        10, mc[k].rect_y
                                    mc[k].pos = 0
                                elif mc[k].leftright == 'right':
                                    mc[k].x, mc[k].y = mc[k].rect_x - \
                                        10, mc[k].rect_y
                                    mc[k].pos = 1
                                if boats[j].pos == 2 or boats[j].pos == 3:
                                    left = False
                                elif boats[j].pos == 4 or boats[j].pos == 5:
                                    right = False
            # Boat movement
            x = x + x_change

            for i in range(6):
                mc[i].x += mc[i].x_change
            InBoat = [a, b]

        # Display movement count
        font = pygame.font.Font(None, 36)
        text = font.render(f"Moves: {movement_count}", True, (255, 255, 255))
        gameDisplay.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
    sys.exit()


if __name__ == "__main__":
    introduction_screen()
    main()
