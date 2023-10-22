import pygame
import math
import sys
from random import randint
import time
# pygame setup
pygame.init()
monitor_size = (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
# screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

clock = pygame.time.Clock()
running = True
dt = 0
acc = 5
v = 0
vX = 0
vY = 0
theta = 0
vY_collided = 1
vX_collided = 1

collision_tolerance = 50

player_x = screen.get_width()/2
player_y = screen.get_height()/2

is_dragged = False

level = 0
level_start = True
level_label = pygame.image.load("title.png")


def show_level(x, y):
    match level:
        case 0:
            levelLabel = level_label
            screen.blit(levelLabel, (x, y))
        case 1:
            levelLabel = pygame.image.load(
                "level1.png")
            screen.blit(levelLabel, (x, y))
        case 2:
            levelLabel = pygame.image.load(
                "level2.png")
            screen.blit(levelLabel, (x, y))
        case 3:
            levelLabel = pygame.image.load(
                "level3.png")
            screen.blit(levelLabel, (x, y))
        case 4:
            levelLabel = pygame.image.load(
                "level4.png")
            screen.blit(levelLabel, (x, y))
        case 5:
            levelLabel = pygame.image.load(
                "level5.png")
            screen.blit(levelLabel, (x, y))
        case 6:
            time.sleep(10000)


start_img = pygame.image.load(
    'start_btn.png').convert_alpha()
exit_img = pygame.image.load(
    'exit_btn.png').convert_alpha()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


start_button = Button(screen.get_width(
) / 2 - start_img.get_width() / 2, screen.get_height() / 3, start_img)
# start_button = Button(screen.get_width()//2 - start_img.get_width() // 2, screen.get_height()//3 - start_img.get_height()//2, start_img)
exit_button = Button(screen.get_width(
) / 2 - exit_img.get_width() / 2, screen.get_height() / 2 + exit_img.get_height() / 2, exit_img)
# exit_button = Button(screen.get_width()//2 - start_img.get_width() //
#                      2, (screen.get_height()*2)//3 - start_img.get_height()//2, exit_img)


class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitBox = pygame.draw.rect(
            screen, (0, 0, 0, 0), (x-5, y-5, 10, 10))
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 10)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 5)


class Obstacle():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.inside = pygame.draw.rect(
            screen, (255, 0, 0), (pos[0], pos[1], size[0], size[1]))
        self.border = pygame.draw.rect(
            screen, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 5)


class Water():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.inside = pygame.draw.rect(
            screen, (0, 0, 255), (pos[0], pos[1], size[0], size[1]))
        self.border = pygame.draw.rect(
            screen, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 5)


class SpeedUp():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.inside = pygame.draw.rect(
            screen, (255, 165, 165), (pos[0], pos[1], size[0], size[1]))
        self.border = pygame.draw.rect(
            screen, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 5)


class Rotate():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.inside = pygame.draw.rect(
            screen, (255, 0, 255), (pos[0], pos[1], size[0], size[1]))
        self.border = pygame.draw.rect(
            screen, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 5)


class Sand():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.inside = pygame.draw.rect(
            screen, (255, 255, 0), (pos[0], pos[1], size[0], size[1]))
        self.border = pygame.draw.rect(
            screen, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 5)


class Hole():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitBox = pygame.draw.rect(
            screen, (0, 0, 0, 0), (x-5, y-5, 10, 10))
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 15)
        pygame.draw.circle(screen, (100, 100, 100), (x, y), 15, 5)


player = Ball(player_x, player_y)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    screen.fill((144, 238, 144))
    # screen.fill((198, 252, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # RENDER YOUR GAME HERE

    if True in pygame.mouse.get_pressed():
        dx = player_x - pygame.mouse.get_pos()[0]
        dy = player_y - pygame.mouse.get_pos()[1]
        is_dragged = True
        v = 0.05*math.sqrt(dx**2+dy**2)
        if v > 15:
            # Original v was 25
            v = 15
        if dx == 0:
            continue
        theta = math.atan(dy/dx)
        if dx < 0:
            theta += math.pi
        vX_collided = 1
        vY_collided = 1

        # Box Velocity Meter
        pygame.draw.rect(screen, (255-15*int(v), 15*int(v), 0),
                         (player_x+25, player_y, 15, 2*abs(v)))
        pygame.draw.rect(screen, (0, 0, 0), (player_x +
                         25, player_y, 15, 2*abs(v)), 5)

    if is_dragged == True and pygame.mouse.get_pressed()[0] == False:
        if player_x <= 0 or player_x >= screen.get_width():
            vX_collided *= -1

        if player_y <= 0 or player_y >= screen.get_height():
            vY_collided *= -1

        vX = vX_collided*v*math.cos(theta)
        vY = vY_collided*v*math.sin(theta)

        player_x += vX
        player_y += vY
        v -= dt*acc

        if v < 0:
            is_dragged = False
            v = 0
            vX = 0
            vY = 0

    levelObstacles = []
    levelSand = []
    levelWater = []
    levelSpeed = []
    levelRotate = []

    if level == 0:
        start_button.draw()

        if start_button.rect.collidepoint(pygame.mouse.get_pos()) and True in pygame.mouse.get_pressed():
            level += 1
        exit_button.draw()
        if exit_button.rect.collidepoint(pygame.mouse.get_pos()) and True in pygame.mouse.get_pressed():
            pygame.quit()

        global goal
        goal = Hole(0, 0)

    if level == 1:
        if level_start == True:
            player_y = 3*(screen.get_height()/4)
            player_x = screen.get_width()/2
            level_start = False

        goal = Hole(screen.get_width()/2, 200)

    if level == 2:
        if level_start == True:
            player_y = 50
            player_x = screen.get_width()-150
            level_start = False

        goal = Hole(50, screen.get_height()-50)

        levelObstacles = [Obstacle((screen.get_width()-250, 0), (50, 400)),
                          Obstacle((50, 400), (screen.get_width()-250, 50)),
                          Obstacle((350, 450), (75, 500)),
                          Obstacle((750, 600), (75, 500)),
                          Obstacle((1150, 450), (75, 500)),
                          Obstacle((1550, 600), (75, 500))]

        if player.hitBox.colliderect(goal.hitBox):
            level += 1
            level_start = True
            v = 0
    if level == 3:
        if level_start == True:
            player_y = screen.get_height()-50
            player_x = 50
            level_start = False

        goal = Hole(screen.get_width()-50, 50)

        levelObstacles = [
            Obstacle((0, 0), (screen.get_width()/2, screen.get_height()/2))]
        levelSand = [Sand((screen.get_width()/2 - 250, screen.get_height()/2), (250, screen.get_height()/2)),
                     Sand((screen.get_width()-450, screen.get_height()/2-350), (450, 450))]
        levelWater = [Water((screen.get_width()/2, 0), (350, 350))]
        levelSpeed = []
        levelRotate = []

        if player.hitBox.colliderect(goal.hitBox):
            level += 1
            level_start = True
            v = 0
    if level == 4:
        if level_start == True:
            player_y = 100
            player_x = 100
            level_start = False

        goal = Hole(screen.get_width()/2+150, 75)

        levelObstacles = [
            Obstacle((screen.get_width()/2-50, 0), (100, 2*screen.get_height()/3))]
        levelSand = []
        levelWater = []
        levelSpeed = [SpeedUp((0, screen.get_height()/2),
                              (screen.get_width()/2-50, 50))]
        levelRotate = [Rotate((screen.get_width()/2-75, 5*screen.get_height()/6), (150, 150)),
                       Rotate((screen.get_width()-250, screen.get_height()/2-75), (250, 250))]

    if level == 5:
        if level_start == True:
            player_y = screen.get_height()//2
            player_x = screen.get_width()//2
            level_start = False

        goal = Hole(screen.get_width()/2, screen.get_height()/2+175)

        levelObstacles = [
            Obstacle((screen.get_width()/2-350, screen.get_height()/2+50), (700, 50))]
        levelSand = [Sand((screen.get_width()/9, 0), (screen.get_width()/9, screen.get_height())),
                     Sand((7*screen.get_width()/9, 0), (screen.get_width()/9, screen.get_height()))]
        levelWater = [Water((0, 0), (screen.get_width()/9, screen.get_height())),
                      Water((8*screen.get_width()/9, 0), (screen.get_width()/9, screen.get_height()))]
        levelSpeed = [
            SpeedUp((screen.get_width()/2-350, screen.get_height()-50), (700, 50))]
        levelRotate = [Rotate((screen.get_width()/9+25, screen.get_height()/2), (150, 150)),
                       Rotate((7*screen.get_width()/9+25, screen.get_height()/2), (150, 150))]

    for speed in levelSpeed:
        if player.hitBox.colliderect(speed.inside):
            v += 0.35

    for rotate in levelRotate:
        if player.hitBox.colliderect(rotate.inside):
            theta += 0.15

    for sand in levelSand:
        if player.hitBox.colliderect(sand.inside) and v > 0:
            v -= 0.35
    for water in levelWater:
        if player.hitBox.colliderect(water.inside):
            level_start = True
    for obstacles in levelObstacles:
        if player.hitBox.colliderect(obstacles.inside):
            if abs(obstacles.inside.top - player.hitBox.bottom) <= collision_tolerance and vY >= 0:
                vY_collided *= -1
            if abs(obstacles.inside.bottom - player.hitBox.top) <= collision_tolerance and vY <= 0:
                vY_collided *= -1
            if abs(obstacles.inside.right - player.hitBox.left) <= collision_tolerance and vX <= 0:
                vX_collided *= -1
            if abs(obstacles.inside.left - player.hitBox.right) <= collision_tolerance and vX >= 0:
                vX_collided *= -1
    if player.hitBox.colliderect(goal.hitBox):
        level += 1
        level_start = True
        v = 0

    if level == 0:
        show_level((screen.get_width() / 2) -
                   level_label.get_width() / 2, level_label.get_height() / 3)
    elif level == 6:
        end_label = pygame.image.load("endScreen.png").convert_alpha()
        # end_label.draw()
        # show_level((screen.get_width() / 2) -
        #            level_label.get_width() / 2, level_label.get_height() / 3)
        # endImage = pygame.image.load("endScreen.png")
        screen.blit(end_label, ((screen.get_width() - end_label.get_width())/2,
                                (screen.get_height() - end_label.get_height())/2))

    else:
        show_level(10, 10)

    player = Ball(player_x, player_y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Delta time
    dt = clock.tick(60) / 1000  # limits FPS to 60

# pygame.quit()
