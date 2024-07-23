# Author: Chin Zheng Dong, Tan Wai Hong, Chin Jun Ming
# Version: 5 (official code)
# Date: 12/2/2023


# importing
import numpy as np
import pygame
import math
import random


# class initialization

class HongSABot:
    def __init__(self, player):
        self.turn = 0
        self.reset_temperature = 8
        self.turn_record = 0
        self.gather_duration = 50
        self.attack_duration = 100
        self.temperature = self.reset_temperature
        self.min_temperature = 3
        self.cooling_rate = 0.03
        self.player = player
        self.mode = "take_land"  # take_land, attack, take_tower, aim_base, gather
        self.enemy_base = []
        self.base = []
        self.lowest_tower = []
        self.collect_army = []
        if self.player == Square.RED:
            self.enemy = Square.BLUE
        else:
            self.enemy = Square.RED

    def play(self, the_game_gird, stack):

        if len(stack) != 0:
            return
        n1 = len(the_game_gird[0])
        neutral_count = 0
        neutral_center_y = 0
        neutral_center_x = 0

        army_position = []
        army_center_y = 0
        army_center_x = 0
        army_space_count = 0

        bot_vision = np.zeros((n1, n1))
        for x in range(n1):
            for y in range(n1):
                if the_game_gird[y, x].territory != self.player:
                    neutral_count += 1
                    neutral_center_x += x
                    neutral_center_y += y
                elif the_game_gird[y, x].territory == self.player:
                    for aa in range(-1, 2):
                        for bb in range(-1, 2):
                            if 0 <= x + aa < n1 and 0 <= y + bb < n1:
                                bot_vision[y + bb, x + aa] = 1
                    if the_game_gird[y, x].value > 1:
                        army_position.append([y, x, the_game_gird[y, x].value])
                    army_center_y += y
                    army_center_x += x
                    army_space_count += 1

        if len(army_position) == 0:
            return

        coordinates = [[coord[0], coord[1]] for coord in army_position]
        weights = [coord[2] for coord in army_position]

        exp_weights = np.exp((weights - np.max(weights)) / 3)  # for numerical stability
        probabilities = exp_weights / np.sum(exp_weights)

        # Randomly choose a coordinate based on softmax probabilities
        chosen_index = np.random.choice(len(coordinates), p=probabilities)
        chosen_coordinate = coordinates[chosen_index]
        y0 = chosen_coordinate[0]
        x0 = chosen_coordinate[1]

        enemy_position = []
        highest_enemy = 0
        self.lowest_tower = []
        for x in range(n1):
            for y in range(n1):
                if bot_vision[y, x] == 1:
                    if the_game_gird[y, x].territory == self.enemy:
                        if the_game_gird[y, x].value > highest_enemy:
                            enemy_position = [y, x]
                            highest_enemy = the_game_gird[y, x].value
                        if self.mode == "take_land" or self.mode == "take_tower":
                            self.mode = "gather"
                            self.turn_record = self.turn
                        if the_game_gird[y, x].type == 'base':
                            self.mode = "aim_base"
                            self.enemy_base = [y, x]
                    if the_game_gird[y, x].territory == Square.NEUTRAL and the_game_gird[y, x].type == "tower":
                        if len(self.lowest_tower) == 0:
                            self.lowest_tower = [0, 0]
                            self.lowest_tower[0] = the_game_gird[y, x].value
                            self.lowest_tower[1] = [y, x]
                        elif self.lowest_tower[0] > the_game_gird[y, x].value:
                            self.lowest_tower[1] = [y, x]
                    if the_game_gird[y, x].territory == self.player and the_game_gird[y, x].type == 'base':
                        self.base = [y, x]

        if len(enemy_position) > 0:
            chosen_coordinate = enemy_position

        aiming_y = 0
        aiming_x = 0
        if self.mode == "aim_base":
            aiming_y = self.enemy_base[0]
            aiming_x = self.enemy_base[1]

        elif self.mode == "attack":
            aiming_y = chosen_coordinate[0]
            aiming_x = chosen_coordinate[1]
            if self.turn - self.turn_record > self.attack_duration:
                self.mode = "gather"
                self.turn_record = self.turn

        elif self.mode == "take_tower":
            if len(self.lowest_tower) == 0:
                self.turn = 100
                self.mode = "take_land"
                aiming_y = army_center_y
                aiming_x = army_center_x
            else:
                aiming_y = self.lowest_tower[1][0]
                aiming_x = self.lowest_tower[1][1]
        elif self.mode == "gather":
            aiming_y = self.base[0]
            aiming_x = self.base[1]
            if self.turn - self.turn_record > self.gather_duration:
                self.mode = "attack"
                self.turn_record = self.turn
        else:
            neutral_center_y = neutral_center_y / neutral_count
            neutral_center_x = neutral_center_x / neutral_count
            army_center_y = army_center_y / army_space_count
            army_center_x = army_center_x / army_space_count
            if -1 < self.turn < 50 or 100 < self.turn < 150:
                aiming_y = army_center_y
                aiming_x = army_center_x
            else:
                aiming_y = neutral_center_y
                aiming_x = neutral_center_x
            if self.turn > 200 and self.mode and len(self.lowest_tower) > 0:
                self.mode = "take_tower"
                aiming_y = self.lowest_tower[1][0]
                aiming_x = self.lowest_tower[1][1]

        if self.mode == "take_land":
            while True:
                pick = random.randint(1, 4)
                if pick == 1:  # up
                    direction_x0 = 0
                    direction_y0 = -1
                elif pick == 2:  # down
                    direction_x0 = 0
                    direction_y0 = 1
                elif pick == 3:  # left
                    direction_x0 = -1
                    direction_y0 = 0
                else:  # right
                    direction_x0 = 1
                    direction_y0 = 0
                y1 = y0 + direction_y0
                x1 = x0 + direction_x0

                delta_c = ((y1 - aiming_y) ** 2 + (x1 - aiming_x) ** 2) ** 0.5 - (
                        (y0 - aiming_y) ** 2 + (x0 - aiming_x) ** 2) ** 0.5
                q = random.uniform(0, 1)

                if 0 <= y1 < n1 and 0 <= x1 < n1 and the_game_gird[y1, x1].type != 'wall':
                    if the_game_gird[y1, x1].type == 'tower':
                        continue
                    elif -1 < self.turn < 50 or 100 < self.turn < 150:
                        delta_c = -delta_c

                if q < 2.71828 ** (-delta_c * 10 / self.temperature):
                    move_to(self.player, x0, y0, x1, y1)
                    self.turn += 1

                    if self.temperature > self.min_temperature:
                        self.temperature = self.temperature * (1 - self.cooling_rate)
                    else:
                        self.temperature = self.reset_temperature
                    return
        else:
            if self.mode == "gather":
                army_position = []
                for x in range(n1):
                    for y in range(n1):
                        if the_game_gird[y, x].territory == self.player:
                            if the_game_gird[y, x].value > 1 and not (y == self.base[0] and x == self.base[1]):
                                army_position.append([y, x, the_game_gird[y, x].value])
                if len(army_position) == 0:
                    self.mode = "attack"
                    self.turn_record = self.turn
                    return
                coordinates = [[coord[0], coord[1]] for coord in army_position]
                weights = [coord[2] for coord in army_position]
                exp_weights = np.exp((weights - np.max(weights)) / 2)  # for numerical stability
                probabilities = exp_weights / np.sum(exp_weights)
                # Randomly choose a coordinate based on softmax probabilities
                chosen_index = np.random.choice(len(coordinates), p=probabilities)
                chosen_coordinate = coordinates[chosen_index]
                y0 = chosen_coordinate[0]
                x0 = chosen_coordinate[1]

            solution = None
            searching = True
            went_map = np.zeros((n1, n1))
            move_list = [[[0, ((aiming_y - y0) ** 2 + (aiming_x - x0) ** 2) ** 0.5, y0, x0]]]
            while searching:
                min_value = 100000
                the_move = None
                for moving in move_list:
                    if moving[-1][0] + moving[-1][1] < min_value:
                        min_value = moving[-1][0] + moving[-1][1]
                        the_move = moving
                for pick in range(4):
                    if pick == 1:  # up
                        direction_x0 = 0
                        direction_y0 = -1
                    elif pick == 2:  # down
                        direction_x0 = 0
                        direction_y0 = 1
                    elif pick == 3:  # left
                        direction_x0 = -1
                        direction_y0 = 0
                    else:  # right
                        direction_x0 = 1
                        direction_y0 = 0
                    the_y0 = the_move[-1][2]
                    the_x0 = the_move[-1][3]
                    the_y1 = the_y0 + direction_y0
                    the_x1 = the_x0 + direction_x0
                    if 0 <= the_y1 < 20 and 0 <= the_x1 < 20:
                        a = Square()
                        if went_map[the_y1, the_x1] != 1 and the_game_gird[the_y1, the_x1].type != "wall" \
                                and (self.mode == "take_tower" or not (the_game_gird[the_y1, the_x1].type == "tower" and
                                                                       the_game_gird[
                                                                           the_y1, the_x1
                                                                       ].territory == Square.NEUTRAL)):
                            new_move = the_move.copy()
                            new_move.append(
                                [the_move[-1][0] + 1, ((aiming_y - the_y1) ** 2 + (aiming_x - the_x1) ** 2) ** 0.5,
                                 the_y1, the_x1])
                            went_map[the_y1, the_x1] = 1
                            if the_y1 == aiming_y and the_x1 == aiming_x:
                                solution = new_move
                                searching = False
                                break
                            else:
                                move_list.append(new_move)
                move_list.remove(the_move)
            self.turn += 1
            move_to(self.player, x0, y0, solution[1][3], solution[1][2])


# game classes
class Square:
    # territory constants
    RED = (255, 0, 0)
    BLUE = (67, 99, 216)
    NEUTRAL = (220, 220, 220)

    # constructor
    def __init__(self):
        self.value = 0 # number of armies in each square
        self.territory = self.NEUTRAL # the square is owned by which player
        self.type = "land" # type of land, example: "land", "wall", "tower", "base"

    def set_square(self, value, territory, type):
        self.value = value
        self.territory = territory
        self.type = type

    def move_to(self, target_square):
        current_square_value = self.value - 1
        target_square_value = target_square.value

        if self.territory == target_square.territory:
            target_square.value = current_square_value + target_square_value
        else:
            if target_square_value - current_square_value < 0:
                target_square.territory = self.territory
                target_square.value = current_square_value - target_square_value
            else:
                target_square.value = target_square_value - current_square_value

        self.value = 1


class Move(): # helper class
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0

    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


# functions initialization
def get_square(game_grid, x, y): # helper function
    return game_grid[y][x]


def check_legal_move(game_grid, player, move):
    # check if selected square belongs to player or not
    if get_square(game_grid, move.x0, move.y0).territory != player:
        return False

    # check if target square is 1 square adjacent to current square
    if abs(move.x0 - move.x1) + abs(move.y0 - move.y1) != 1:
        return False

    # check if moves outside the grid
    if not (n > move.x1 >= 0 and n > move.y1 >= 0):
        return False

    # check if it hits a wall
    if get_square(game_grid, move.x1, move.y1).type == "wall":
        return False

    # check if there are sufficient amount of army
    if get_square(game_grid, move.x0, move.y0).value <= 1:
        return False

    return True


def move_to(player, x0, y0, x1, y1):
    if player == Square.BLUE:
        blue_move_queue.append(Move(x0, y0, x1, y1))
    if player == Square.RED:
        red_move_queue.append(Move(x0, y0, x1, y1))


def set_fog(x, y):
    if len(fog_grid) > x >= 0 and len(fog_grid) > y >= 0:
        fog_grid[y][x] = 1


def set_radial_fog(x, y):
    set_fog(x + 1, y + 1)
    set_fog(x + 1, y - 1)
    set_fog(x + 1, y)
    set_fog(x - 1, y + 1)
    set_fog(x - 1, y - 1)
    set_fog(x - 1, y)
    set_fog(x, y + 1)
    set_fog(x, y - 1)
    set_fog(x, y)


# graphic functions
def darken(colour):
    intensity = 60
    r = max(colour[0] - intensity, 0)
    g = max(colour[1] - intensity, 0)
    b = max(colour[2] - intensity, 0)
    new_colour = (r, g, b)
    return new_colour


def lighten(colour):
    intensity = 30
    r = min(colour[0] + intensity, 255)
    g = min(colour[1] + intensity, 255)
    b = min(colour[2] + intensity, 255)
    new_colour = (r, g, b)
    return new_colour


def draw_arrow(x0, y0, x1, y1):
    pygame.draw.line(game_display, (255, 255, 255), (x0, y0), (x1 + (x1 - x0) / 10, y1 + (y1 - y0) / 10), 1)
    x2 = ((-y0 + y1) / 2 + x0 - x1) / 8 + x1
    y2 = ((x0 - x1) / 2 + y0 - y1) / 8 + y1
    x3 = ((y0 - y1) / 2 + x0 - x1) / 8 + x1
    y3 = ((-x0 + x1) / 2 + y0 - y1) / 8 + y1
    pygame.draw.line(game_display, (255, 255, 255), (x1, y1), (x2, y2), 5)
    pygame.draw.line(game_display, (255, 255, 255), (x1, y1), (x3, y3), 5)


# helper math functions
def flr(x, a):
    return a * math.floor(x / a)


# adjustable variables initialization
game_width = 760  # screen is always square, so no need game height
n = 20  # number of squares each side
land_army_growth_interval = 25
base_army_growth_interval = 1
cooldown = 0.5
blue_timer = 0
red_timer = 0
number_of_walls = 60
number_of_towers = 11
tower_value = 30
human_player = Square.RED
bot1 = HongSABot(Square.BLUE)

# graphic variables
default_colour = (220, 220, 220)
grid_lines_colour = (0, 0, 0)
empty_square_colour = (220, 220, 220)
number_text_colour = (220, 220, 220)
fog_colour = (57, 57, 57)
grid_lines_thickness = 2
font_size = 22
fog_file = "game assets/mysterymountain.PNG"
wall_file = "game assets/mountain.PNG"
neutral_tower_file = "game assets/neutraltower.PNG"
blue_base_file = "game assets/bluebase.PNG"
blue_tower_file = "game assets/bluetower.PNG"
red_base_file = "game assets/redbase.PNG"
red_tower_file = "game assets/redtower.PNG"


# non adjustable variables initialization
game_grid = np.array([[Square] * n] * n)  # initialising grid
red_move_queue = []
blue_move_queue = []

for i in range(n):  # initialising squares
    for j in range(n):
        game_grid[i][j] = Square()

for i in range(number_of_walls):  # initialising walls
    r1 = int(random.random() * n)
    r2 = int(random.random() * n)

    game_grid[r1][r2].type = "wall"

for i in range(number_of_towers):  # initialising walls
    r1 = int(random.random() * n)
    r2 = int(random.random() * n)

    game_grid[r1][r2].type = "tower"
    game_grid[r1][r2].value = tower_value + random.randint(0, 4)

r1 = int(random.random() * n)  # initialising bases
r2 = int(random.random() * n)
game_grid[r1][r2].set_square(10, Square.RED, "base")
while True:
    k1 = int(random.random() * n)
    k2 = int(random.random() * n)
    if (k1 - r1) ** 2 + (k2 - r2) ** 2 > (n // 2) ** 2:
        break

game_grid[k1][k2].set_square(10, Square.BLUE, "base")

square_width = game_width / n
running = True
selected_x = 0
selected_y = 0
t = 0
t2 = 0
fog_grid = np.array([[0] * n] * n)
pygame.init()
game_over = False
game_display = pygame.display.set_mode((game_width, game_width))
text_font = pygame.font.SysFont('freesanbold.ttf', font_size)
start_time = pygame.time.get_ticks()
fog_image = pygame.image.load(fog_file).convert()
wall_image = pygame.image.load(wall_file).convert()
neutral_tower_image = pygame.image.load(neutral_tower_file).convert()
blue_base_image = pygame.image.load(blue_base_file).convert()
blue_tower_image = pygame.image.load(blue_tower_file).convert()
red_base_image = pygame.image.load(red_base_file).convert()
red_tower_image = pygame.image.load(red_tower_file).convert()


# game loop
while running and not game_over:
    fog_grid = np.array([[0] * n] * n)
    time = (pygame.time.get_ticks() - start_time) / 1000  # record time
    bot1.play(game_grid, blue_move_queue)  # bot plays each frame
    red_base_exists = False
    blue_base_exists = False

    if time - t >= land_army_growth_interval:  # army growth
        for i in range(n):
            for j in range(n):
                if game_grid[i][j].territory != Square.NEUTRAL:
                    game_grid[i][j].value += 1
        t += land_army_growth_interval
    if time - t2 >= base_army_growth_interval:
        for i in range(n):
            for j in range(n):
                if game_grid[i][j].territory != Square.NEUTRAL and (
                        game_grid[i][j].type == "base" or game_grid[i][j].type == "tower"):
                    game_grid[i][j].value += 1
        t2 += base_army_growth_interval

    game_display.fill((0, 0, 0))  # clear screen

    for i in range(n):  # initialise fog
        for j in range(n):
            if get_square(game_grid, j, i).territory == human_player:
                set_radial_fog(j, i)

    # execute queue
    if time - blue_timer >= cooldown and len(blue_move_queue) > 0:
        move = blue_move_queue[0]
        if check_legal_move(game_grid, Square.BLUE, move) == False:
            blue_move_queue.pop(0)
        else:
            get_square(game_grid, move.x0, move.y0).move_to(get_square(game_grid, move.x1, move.y1))
            blue_move_queue.pop(0)
            blue_timer = time

    if time - red_timer >= cooldown and len(red_move_queue) > 0:
        move = red_move_queue[0]
        if check_legal_move(game_grid, Square.RED, move) == False:
            red_move_queue.pop(0)
        else:
            get_square(game_grid, move.x0, move.y0).move_to(get_square(game_grid, move.x1, move.y1))
            red_move_queue.pop(0)
            red_timer = time

    for i in range(n):  # territory colour
        for j in range(n):
            pygame.draw.rect(game_display, game_grid[i][j].territory,
                             [j * square_width, i * square_width, square_width, square_width])

    for i in range(n): # base, wall and tower graphics
        for j in range(n):
            if game_grid[i][j].type == "base":
                if game_grid[i][j].territory == Square.RED:
                    game_display.blit(red_base_image, (j * square_width, i * square_width))
                    red_base_exists = True
                else:
                    game_display.blit(blue_base_image, (j * square_width, i * square_width))
                    blue_base_exists = True
            if game_grid[i][j].type == "wall":
                game_display.blit(wall_image, (j * square_width, i * square_width))
            if game_grid[i][j].type == "tower":
                if game_grid[i][j].territory == Square.NEUTRAL:
                    game_display.blit(neutral_tower_image, (j * square_width, i * square_width))
                if game_grid[i][j].territory == Square.RED:
                    game_display.blit(red_tower_image, (j * square_width, i * square_width))
                if game_grid[i][j].territory == Square.BLUE:
                    game_display.blit(blue_tower_image, (j * square_width, i * square_width))

    for i in range(n):  # number texts
        for j in range(n):
            if game_grid[i][j].territory != Square.NEUTRAL or game_grid[i][j].type == "tower":
                text = text_font.render(f"{game_grid[i][j].value}", True, number_text_colour)
                textRect = text.get_rect()
                textRect.center = (square_width / 2 + square_width * j, square_width / 2 + square_width * i)
                game_display.blit(text, textRect)

    for i in range(n + 1):  # grid lines
        pygame.draw.line(game_display, grid_lines_colour, (square_width * i, 0), (square_width * i, game_width),
                         grid_lines_thickness)
        pygame.draw.line(game_display, grid_lines_colour, (0, square_width * i), (game_width, square_width * i),
                         grid_lines_thickness)

    for i in range(n):  # fog
        for j in range(n):
            if fog_grid[i][j] == 0:
                if game_grid[i][j].type == "wall" or game_grid[i][j].type == "tower":
                    game_display.blit(fog_image, (j * square_width, i * square_width))
                else:
                    pygame.draw.rect(game_display, fog_colour,
                                     [j * square_width, i * square_width, square_width, square_width], 0)

    # selected box
    for i in range(int(selected_x * square_width), int((selected_x + 1) * square_width)):
        for j in range(int(selected_y * square_width), int((selected_y + 1) * square_width)):
            colour = game_display.get_at([i, j])
            if fog_grid[selected_y][selected_x] == 1:
                game_display.set_at([i, j], darken(colour))
            else:
                game_display.set_at([i, j], lighten(colour))

    # arrows
    for i in range(len(red_move_queue)):
        x0 = (red_move_queue[i].x0 + 0.5) * square_width
        y0 = (red_move_queue[i].y0 + 0.5) * square_width
        x1 = (red_move_queue[i].x1 + 0.5) * square_width
        y1 = (red_move_queue[i].y1 + 0.5) * square_width

        x2 = x0 + 3 * (x1 - x0) / 10
        y2 = y0 + 3 * (y1 - y0) / 10
        x3 = x0 + 7 * (x1 - x0) / 10
        y3 = y0 + 7 * (y1 - y0) / 10

        draw_arrow(x2, y2, x3, y3)

    if not (blue_base_exists and red_base_exists):  # check if the game is ended
        if blue_base_exists:
            print("blue won!")
        if red_base_exists:
            print("red won!")
        game_over = True

    pygame.display.update()  # update

    for event in pygame.event.get():  # event manager
        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse events
            mouse_index_x = int(flr(pygame.mouse.get_pos()[0], square_width) / square_width)
            mouse_index_y = int(flr(pygame.mouse.get_pos()[1], square_width) / square_width)
            selected_x = mouse_index_x
            selected_y = mouse_index_y

        if event.type == pygame.KEYDOWN:  # key events
            keys = pygame.key.get_pressed()
            direction_x = 0
            direction_y = 0
            if keys[pygame.K_w]:  # up
                direction_x = 0
                direction_y = -1
            elif keys[pygame.K_s]:  # down
                direction_x = 0
                direction_y = 1
            elif keys[pygame.K_a]:  # left
                direction_x = -1
                direction_y = 0
            elif keys[pygame.K_d]:  # right
                direction_x = 1
                direction_y = 0

            target_x = selected_x + direction_x
            target_y = selected_y + direction_y

            move_to(human_player, selected_x, selected_y, target_x, target_y)

            if n > target_x >= 0 and n > target_y >= 0:
                selected_x = target_x
                selected_y = target_y

        if event.type == pygame.QUIT:
            running = False

while running and game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()