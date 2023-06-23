import pygame.time
from object import *
from settings import *
import math

keys = {                                    # The list of keys for input
    "up": False,                            # UP arrow key
    "down": False,                          # DOWN arrow key
    "left": False,                          # LEFT arrow key
    "right": False,                         # RIGHT arrow key
    "enter": False,                         # ENTER key
    "space": False,                         # SPACEBAR key
    "f": False                              # F key
}

def sign(num):                              # returns +1 or -1 depending on whether the number is positive or negative
    if num > 0:                             # if 0 or greater
        return 1                            # return 1
    else:                                   # otherwise
        return -1                           # return -1

def limit_vector2(game_object):
    if abs(game_object.y_velocity) > PLAYER_SPEED:
        game_object.y_velocity = sign(game_object.y_velocity) * PLAYER_SPEED / 2
    if abs(game_object.x_velocity) > PLAYER_SPEED:
        game_object.x_velocity = sign(game_object.x_velocity) * PLAYER_SPEED / 2

def limit_vector(game_object):
    velocity = math.sqrt(game_object.y_velocity * game_object.y_velocity + game_object.x_velocity * game_object.x_velocity)
    if abs(velocity) > PLAYER_SPEED:
        game_object.x_velocity = sign(game_object.x_velocity) * PLAYER_SPEED * game_object.x_velocity * game_object.x_velocity / (velocity * velocity)
        game_object.y_velocity = sign(game_object.y_velocity) * PLAYER_SPEED * game_object.y_velocity * game_object.y_velocity / (velocity * velocity)


def bound_check(game_object,X_UB,Y_UB,X_LB=0,Y_LB=0):
    if (game_object.x + game_object.width >= X_UB):
        return False
    elif (game_object.x <= X_LB):
        return False
    if (game_object.y + game_object.height >= Y_UB):
        return False
    elif (game_object.y <= Y_LB):
        return False
    return True

def bound_screen_space(game_object):
    if (game_object.x + game_object.width >= SCREEN_WIDTH):
        game_object.x = SCREEN_WIDTH - game_object.width
        game_object.x_velocity = -game_object.x_velocity
    elif (game_object.x <= 0):
        game_object.x = 0
        game_object.x_velocity = -game_object.x_velocity

    if (game_object.y + game_object.height >= SCREEN_HEIGHT):
        game_object.y = SCREEN_HEIGHT - game_object.height
        game_object.y_velocity = -game_object.y_velocity
    elif (game_object.y <= 0):
        game_object.y = 0
        game_object.y_velocity = -game_object.y_velocity

def set_input(event):                                       # Set the keys as pressed or no pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            keys['up'] = True
        elif event.key == pygame.K_DOWN:
            keys['down'] = True
        elif event.key == pygame.K_LEFT:
            keys['left'] = True
        elif event.key == pygame.K_RIGHT:
            keys['right'] = True
        elif event.key == pygame.K_SPACE:
            keys['space'] = True
        elif event.key == pygame.K_f:
            keys['f'] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            keys['up'] = False
        elif event.key == pygame.K_DOWN:
            keys['down'] = False
        elif event.key == pygame.K_LEFT:
            keys['left'] = False
        elif event.key == pygame.K_RIGHT:
            keys['right'] = False
        elif event.key == pygame.K_SPACE:
            keys['space'] = False
        elif event.key == pygame.K_f:
            keys['f'] = False

def manage_input(player,obj_list):
    if(not player.alive):
        return
                                                            # MOVEMENT CONTROLS
    if keys['up']:
        player.y_velocity = player.y_velocity - 1
        player.angle = 90
    if keys['down']:
        player.y_velocity = player.y_velocity + 1
        player.angle = 270
    if keys['left']:
        player.x_velocity = player.x_velocity - 1
        player.angle = 180
    if keys['right']:
        player.x_velocity = player.x_velocity + 1
        player.angle = 0
                                                            # COMPOUND MOVEMENT CONTROLS, MULTIPLE KEYS PRESSED
    if keys['up']:
        if keys['left']:
            player.angle = 135
        if keys['right']:
            player.angle = 45
    if keys['down']:
        if keys['left']:
            player.angle = 225
        if keys['right']:
            player.angle = 315
                                                            # ATTACKS AND SPECIAL ACTIONS
    if keys['space']:
        player.warp()                                       # trigger player special
    if keys['f']:
        player.attack(obj_list)

def to_radian(angle):                                       # converts degree to radian units
    return math.pi*angle/180

def collide_check(object1,object2):                         # checks whether two objects are colliding with each other

    if (abs(object1.x + object1.width * 0.5 - object2.x - object2.width * 0.5)) < 0.5*(object1.width + object2.width) and \
       (abs(object1.y + object1.height * 0.5 - object2.y - object2.height * 0.5)) < 0.5 * (object1.height + object2.height):
            return True
    return False