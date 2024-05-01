import pygame
import sys
import copy
from board import boards
import math
from button import Button

pygame.init()

height = 770
width = 900
font = pygame.font.Font('freesansbold.ttf', 25)
window = pygame.display.set_mode((width, height))

level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi

player_x = 438
player_y = 521
player_speed = 2
direction = 0
direction_command = 0
counter = 0
flicker = False
turns_allowed = [False, False, False, False]
score = 0
powerup = False
powerup_count = 0
eaten_ghosts = [False, False, False, False]
moving = False
startup_counter = 0
lives = 2
run = True

with open("hiscore.txt", "r") as f:
    hiscore = f.readline()

blue_x = 480
blue_y = 340
blue_direction = 2
orange_x = 400
orange_y = 340
orange_direction = 2
pink_x = 440
pink_y = 340
pink_direction = 2
red_x = 435
red_y = 257
red_direction = 0
blue_dead = False
red_dead = False
pink_dead = False
orange_dead = False
blue_box = False
red_box = False
pink_box = False
orange_box = False
ghost_speeds = [2, 2, 2, 2]

targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

game_over = False
game_won = False


bg_image = pygame.transform.scale(pygame.image.load('assets/bg.png'), (width, height))

player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png"), (32, 32)))

# Ghost images
blue_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (32, 32))
orange_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/orange.png'), (32, 32))
red_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/red.png'), (32, 32))
pink_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/pink.png'), (32, 32))
dead_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (32, 32))
powerup_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (32, 32))

# Game sounds
eating_fruit = pygame.mixer.Sound("assets/pacman-eatfruit/pacman_eatfruit.wav")
eating_ghost = pygame.mixer.Sound("assets/pacman-eatghost/pacman_eatghost.wav")
bg_music = pygame.mixer.Sound("assets/pacman-beginning/pacman_beginning.wav")
death = pygame.mixer.Sound("assets/pacman-death/pacman_death.wav")
eating_points = pygame.mixer.Sound("assets/pacman-chomp/pacman_chomp.wav")
intermission = pygame.mixer.Sound("assets/pacman_intermission.wav")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


class Ghost:
    def __init__(self, x, y, target, speed, img, direct, dead, box, id):
        self.x = x
        self.y = y
        self.center_x = self.x + 15
        self.center_y = self.y + 15
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collision()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            window.blit(self.img, (self.x, self.y))
        elif powerup and not self.dead and not eaten_ghosts[self.id]:
            window.blit(powerup_img, (self.x, self.y))
        else:
            window.blit(dead_img, (self.x, self.y))
        ghost_rect = pygame.rect.Rect((self.center_x - 11, self.center_y - 11), (34, 34))
        return ghost_rect

    def check_collision(self):
        num1 = ((height - 50) // 32)
        num2 = (width // 30)
        num3 = 15
        self.turns = [False, False, False, False]

        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 8 <= self.center_x % num2 <= 15:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 15:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 8 <= self.center_x % num2 <= 15:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 15:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 335 < self.x < 535 and 270 < self.y < 360:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -50:
            self.x = 897
        elif self.x > 900:
            self.x = -47
        return self.x, self.y, self.direction

    def move_blinky(self):
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[2]:
                self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[3]:
                self.y += self.speed
        if self.x < -50:
            self.x = 897
        elif self.x > 900:
            self.x = -47
        return self.x, self.y, self.direction

    def move_inky(self):
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                self.y += self.speed
        if self.x < -50:
            self.x = 897
        elif self.x > 900:
            self.x = -47
        return self.x, self.y, self.direction

    def move_pinky(self):
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -50:
            self.x = 897
        elif self.x > 900:
            self.x = -47
        return self.x, self.y, self.direction


def draw_board():
    num1 = ((height - 50) // 32)
    num2 = (width // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(window, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(window, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if level[i][j] == 3:
                pygame.draw.line(window, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 1)
            if level[i][j] == 4:
                pygame.draw.line(window, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 1)
            if level[i][j] == 5:
                pygame.draw.arc(window, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 1)
            if level[i][j] == 6:
                pygame.draw.arc(window, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 1)
            if level[i][j] == 7:
                pygame.draw.arc(window, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 1)
            if level[i][j] == 8:
                pygame.draw.arc(window, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 1)
            if level[i][j] == 9:
                pygame.draw.line(window, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 1)


def draw_player():
    if direction == 0:
        window.blit(player_images[counter//5], (player_x, player_y))
    elif direction == 1:
        window.blit(pygame.transform.flip(player_images[counter//5], True, False), (player_x, player_y))
    elif direction == 2:
        window.blit(pygame.transform.rotate(player_images[counter//5], 90), (player_x, player_y))
    elif direction == 3:
        window.blit(pygame.transform.rotate(player_images[counter//5], 270), (player_x, player_y))


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    window.blit(score_text, (10, 740))
    for i in range(lives + 1):
        window.blit(pygame.transform.scale(player_images[0], (28, 28)), (650 + i * 30, 730))
    hiscore_text = font.render(f'Hiscore: {hiscore}', True, 'white')
    window.blit(hiscore_text, (400, 740))


def check_collision(scr, power, power_count, eaten_ghosts):
    num1 = (height-50)//32
    num2 = width//30

    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            eating_points.play()
            scr += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            eating_fruit.play()
            scr += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]

    return scr, power, power_count, eaten_ghosts


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (height - 50) // 32
    num2 = (width // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 8 <= centerx % num2 <= 15:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 15:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 8 <= centerx % num2 <= 15:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 15:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_target():
    if player_x < 438:
        run_x = 900
    else:
        run_x = 0
    if player_y < 450:
        run_y = 900
    else:
        run_y = 0
    return_target = (400, 340)
    if powerup:
        if not red.dead:
            red_target = (run_x, run_y)
        else:
            red_target = return_target
        if not blue.dead:
            blue_target = (run_x, run_y)
        else:
            blue_target = return_target
        if not pink.dead:
            pink_target = (run_x, run_y)
        else:
            pink_target = return_target
        if not orange.dead:
            orange_target = (run_x, run_y)
        else:
            orange_target = return_target
    else:
        if not red.dead:
            if red.in_box:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not blue.dead:
            if blue.in_box:
                blue_target = (400, 100)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = return_target
        if not pink.dead:
            if pink.in_box:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not orange.dead:
            if orange.in_box:
                orange_target = (400, 100)
            else:
                orange_target = (player_x, player_y)
        else:
            orange_target = return_target
    return [red_target, blue_target, pink_target, orange_target]


def main_menu():
    global run
    while run:
        window.blit(bg_image, (0, 0))
        intermission.play()
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(60).render("MAIN MENU", True, "orange")
        menu_rect = menu_text.get_rect(center=(450, 100))

        play_button = Button(image=pygame.transform.scale(pygame.image.load("assets/button.png"), (200, 60)),
                             pos=(450, 450), text_input="PLAY", font=get_font(20), base_color="white",
                             hovering_color="Green")
        help_button = Button(image=pygame.transform.scale(pygame.image.load("assets/button.png"), (200, 60)),
                             pos=(450, 550), text_input="HELP", font=get_font(20), base_color="white",
                             hovering_color="Green")
        quit_button = Button(image=pygame.transform.scale(pygame.image.load("assets/button.png"), (200, 60)),
                             pos=(450, 650), text_input="QUIT", font=get_font(20), base_color="white",
                             hovering_color="Green")

        window.blit(menu_text, menu_rect)
        for button in [play_button, help_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    intermission.fadeout(100)
                    run = False
                if help_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def options():
    while True:
        option_mouse_pos = pygame.mouse.get_pos()

        window.fill("black")

        options_text = get_font(20).render("Press the arrow keys to move.", True, "white")
        options_rect = options_text.get_rect(center=(450, 260))
        window.blit(options_text, options_rect)

        options_back = Button(image=pygame.transform.scale(pygame.image.load("assets/button.png"), (200, 60)),
                              pos=(150, 700), text_input="BACK", font=get_font(20), base_color="white",
                              hovering_color="Green")
        options_back.changeColor(option_mouse_pos)
        options_back.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(option_mouse_pos):
                    main_menu()

        pygame.display.update()


while True:
    main_menu()
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    if powerup and powerup_count < 600:
        powerup_count += 1
    elif powerup and powerup_count >= 600:
        powerup_count = 0
        powerup = False
        eaten_ghosts = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    window.fill('black')
    draw_board()
    center_x = player_x + 16
    center_y = player_y + 17

    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghosts[0]:
        ghost_speeds[0] = 2
    if eaten_ghosts[1]:
        ghost_speeds[1] = 2
    if eaten_ghosts[2]:
        ghost_speeds[2] = 2
    if eaten_ghosts[3]:
        ghost_speeds[3] = 2
    if red_dead:
        ghost_speeds[0] = 4
    if blue_dead:
        ghost_speeds[1] = 4
    if pink_dead:
        ghost_speeds[2] = 4
    if orange_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(window, 'black', (center_x, center_y), 17, 2)
    draw_player()

    red = Ghost(red_x, red_y, targets[0], ghost_speeds[0], red_img, red_direction, red_dead, red_box, 0)
    blue = Ghost(blue_x, blue_y, targets[1], ghost_speeds[1], blue_img, blue_direction, blue_dead, blue_box, 1)
    pink = Ghost(pink_x, pink_y, targets[2], ghost_speeds[2], pink_img, pink_direction, pink_dead, pink_box, 2)
    orange = Ghost(orange_x, orange_y, targets[3], ghost_speeds[3], orange_img, orange_direction, orange_dead,
                   orange_box, 3)

    draw_misc()
    targets = get_target()
    turns_allowed = check_position(center_x, center_y)

    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not red_dead and not red.in_box:
            red_x, red_y, red_direction = red.move_blinky()
        else:
            red_x, red_y, red_direction = red.move_clyde()

        if not blue_dead and not blue.in_box:
            blue_x, blue_y, blue_direction = blue.move_inky()
        else:
            blue_x, blue_y, blue_direction = blue.move_clyde()

        if not pink_dead and not pink.in_box:
            pink_x, pink_y, pink_direction = pink.move_pinky()
        else:
            pink_x, pink_y, pink_direction = pink.move_clyde()

        orange_x, orange_y, orange_direction = orange.move_clyde()
    score, powerup, powerup_count, eaten_ghost = check_collision(score, powerup, powerup_count, eaten_ghosts)

    if not powerup:
        if (player_circle.colliderect(red.rect) and not red.dead) or \
                (player_circle.colliderect(blue.rect) and not blue.dead) or \
                (player_circle.colliderect(pink.rect) and not pink.dead) or \
                (player_circle.colliderect(orange.rect) and not orange.dead):
            death.play()
            if lives > 0:
                lives -= 1
                powerup = False
                power_counter = 0
                startup_counter = 0
                player_x = 438
                player_y = 521
                direction = 0
                direction_command = 0
                blue_x = 480
                blue_y = 340
                blue_direction = 2
                orange_x = 400
                orange_y = 340
                orange_direction = 2
                pink_x = 440
                pink_y = 340
                pink_direction = 2
                red_x = 435
                red_y = 257
                red_direction = 0
                eaten_ghosts = [False, False, False, False]
                red_dead = False
                pink_dead = False
                orange_dead = False
                blue_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and eaten_ghosts[0] and not red.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 438
            player_y = 521
            direction = 0
            direction_command = 0
            blue_x = 480
            blue_y = 340
            blue_direction = 2
            orange_x = 400
            orange_y = 340
            orange_direction = 2
            pink_x = 440
            pink_y = 340
            pink_direction = 2
            red_x = 435
            red_y = 257
            red_direction = 0
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            blue = False
            orange = False
            pink_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blue.rect) and eaten_ghosts[1] and not blue.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 438
            player_y = 521
            direction = 0
            direction_command = 0
            blue_x = 480
            blue_y = 340
            blue_direction = 2
            orange_x = 400
            orange_y = 340
            orange_direction = 2
            pink_x = 440
            pink_y = 340
            pink_direction = 2
            red_x = 435
            red_y = 257
            red_direction = 0
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            pink_dead = False
            orange_dead = False
            blue_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pink.rect) and eaten_ghosts[2] and not pink.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 438
            player_y = 521
            direction = 0
            direction_command = 0
            blue_x = 480
            blue_y = 340
            blue_direction = 2
            orange_x = 400
            orange_y = 340
            orange_direction = 2
            pink_x = 440
            pink_y = 340
            pink_direction = 2
            red_x = 435
            red_y = 257
            red_direction = 0
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            pink_dead = False
            orange_dead = False
            blue_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(orange.rect) and eaten_ghosts[3] and not orange.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 438
            player_y = 521
            direction = 0
            direction_command = 0
            blue_x = 480
            blue_y = 340
            blue_direction = 2
            orange_x = 400
            orange_y = 340
            orange_direction = 2
            pink_x = 440
            pink_y = 340
            pink_direction = 2
            red_x = 435
            red_y = 257
            red_direction = 0
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            pink_dead = False
            orange_dead = False
            blue_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and not red.dead and not eaten_ghosts[0]:
        eating_ghost.play()
        red_dead = True
        eaten_ghosts[0] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(blue.rect) and not blue.dead and not eaten_ghosts[1]:
        eating_ghost.play()
        blue_dead = True
        eaten_ghosts[1] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(pink.rect) and not pink.dead and not eaten_ghosts[2]:
        eating_ghost.play()
        pink_dead = True
        eaten_ghosts[2] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(orange.rect) and not orange.dead and not eaten_ghosts[3]:
        eating_ghost.play()
        orange_dead = True
        eaten_ghosts[3] = True
        score += (2 ** eaten_ghosts.count(True)) * 100

    if game_won:
        win_text = get_font(20).render("You Win!! Press Space to Play Again!!!", True, "white")
        win_rect = win_text.get_rect(center=(450, 340))
        window.blit(win_text, win_rect)
        startup_counter = 0
    if game_over:
        loss_text = get_font(20).render("You Lose!! Press Space to Play Again!!!", True, "white")
        loss_rect = loss_text.get_rect(center=(450, 340))
        window.blit(loss_text, loss_rect)

    if score > int(hiscore):
        hiscore = score
        with open("hiscore.txt", "w") as f:
            f.write(str(hiscore))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 438
                player_y = 521
                direction = 0
                direction_command = 0
                blue_x = 480
                blue_y = 340
                blue_direction = 2
                orange_x = 400
                orange_y = 340
                orange_direction = 2
                pink_x = 440
                pink_y = 340
                pink_direction = 2
                red_x = 435
                red_y = 257
                red_direction = 0
                blue_dead = False
                red_dead = False
                pink_dead = False
                orange_dead = False
                blue_box = False
                red_box = False
                pink_box = False
                orange_box = False
                eaten_ghost = [False, False, False, False]
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    if player_x < -50:
        player_x = 897

    if red.in_box and red_dead:
        red_dead = False
    if blue.in_box and blue_dead:
        blue_dead = False
    if pink.in_box and pink_dead:
        pink_dead = False
    if orange.in_box and orange_dead:
        orange_dead = False

    pygame.time.Clock().tick(60)
    pygame.display.flip()
