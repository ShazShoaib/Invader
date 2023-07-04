import pygame
import math
import random

import helper
from settings import *
from helper import *

class img_obj:

    def __init__(self):                                     # Base class for all objects, values are configured for player class
        self.alive = True                                   # To keep track of when object is alive / destroyed
        self.type = PLAYER_TAG                              # To keep track of which object is which
        self.img_path = PLAYER_IMG_PATH                     # Set the image path for sprite
        self.x = 0                                          # Set the x coordinate on screen
        self.y = SCREEN_HEIGHT                              # Set the y coordinate on screen
        self.width = PLAYER_WIDTH                           # Set the width of the sprite rendered
        self.height = PLAYER_HEIGHT                         # Set the height of the sprite rendered
        self.angle = 90                                     # Set the angle offset from the image file and rendered sprite
        self.angle_velocity = 0                             # Set the rotational velocity of the object
        self.x_velocity = 0                                 # Set the velocity along the x axis
        self.y_velocity = 1                                 # Set the velocity along the y axis
        self.friction = True                                # Object will experience friction
        self.speedlim = True                                # Object will have a speed limit
        self.bound = True                                   # Object will be bounded within the screen space

    def render(self,window):
        window.blit(self.img, (self.x,self.y))              # Render the sprite to the window

    def update(self):

        self.x = self.x + self.x_velocity                                       # Update x coordinate based on the velocity along x axis
        self.y = self.y + self.y_velocity                                       # Update y coordinate based on the velocity along y axis
        self.angle = self.angle + self.angle_velocity                           # Update the angle based on the rotational velocity

        if self.friction:                                                       # If the object is set to experience friction
            self.x_velocity = self.x_velocity * (1-FRICTION)                    # Applying friction to x axis
            self.y_velocity = self.y_velocity * (1-FRICTION)                    # Applying friction to y axis
            self.angle_velocity = self.angle_velocity * (1-ANGULAR_FRICTION)    # Applying friction to the rotational velocity

        if self.speedlim:                                                       # if the object is set to experience a speed limit
            helper.limit_vector(self)                                           # limit the speed

        if self.bound:                                                          # if the object is set to be bound within the screenspace
            helper.bound_screen_space(self)                                     # keep the object within the screenspace

        scaler = 1 + (math.sqrt(2)-1)*abs(math.sin(2*helper.to_radian(self.angle)))           # A scaler to keep the scale constant after rotation

        self.img = pygame.image.load(self.img_path)                                           # Load the image again to minimize artifacting
        self.img = pygame.transform.rotate(self.img, self.angle)                              # Rotate the image according to its angle
        self.img = pygame.transform.scale(self.img, (self.width*scaler, self.height*scaler))  # Scale the image according to its width and height


class explosion(img_obj):
    def __init__(self,x,y):
        img_obj.__init__(self)
        self.type = EXPLOSION_TAG
        self.img_path = EXPLOSION_IMG_PATH
        self.width = EXPLOSION_SIZE
        self.height = EXPLOSION_SIZE
        self.x_velocity = 0
        self.y_velocity = 0
        self.angle = random.randint(0,360)
        self.x = x
        self.y = y
        self.angle_velocity = EXPLOSION_ROTATION
        self.alpha = 255

    def update(self):
        img_obj.update(self)
        self.alpha = self.alpha - EXPLOSION_DETERIORATION
        if self.width < 1:
            self.alive = False
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.rotate(self.img, self.angle)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.img.set_alpha(self.alpha)

class player(img_obj):

    def __init__(self):
        img_obj.__init__(self)
        self.warp_cooldown = WARP_COOLDOWN
        self.attack_cooldown = ATTACK_COOLDOWN
        self.x = SCREEN_WIDTH/2

    def brake(self):                                       # To reduce the velocity of the player
        self.x_velocity = 0.9*self.x_velocity
        self.y_velocity = 0.9*self.y_velocity

    def update(self):
        img_obj.update(self)

    def cooldown(self,cool):
        self.warp_cooldown = self.warp_cooldown + cool
        self.attack_cooldown = self.attack_cooldown + cool

    def warp(self):
        if self.warp_cooldown > WARP_COOLDOWN:
            self.x = self.x + WARP_SPEED * math.cos(helper.to_radian(self.angle))
            self.y = self.y - WARP_SPEED * math.sin(helper.to_radian(self.angle))
            self.warp_cooldown = 0

    def attack(self,obj_list):
        if self.attack_cooldown > ATTACK_COOLDOWN:
            laser = p_bullet(self)  # Create player bullet
            obj_list.append(laser)  # Add player bullet to object list
            self.attack_cooldown = 0

class enemy(img_obj):
    def __init__(self):
        img_obj.__init__(self)
        self.img_path = ENEMY_IMG_PATH
        self.type = ENEMY_TAG
        self.friction = False
        self.x = random.randint(0,SCREEN_WIDTH)
        self.y = -PLAYER_HEIGHT
        self.angle = 270
        self.y_velocity = ENEMY_SPEED
        self.bound = False

    def update(self):
        img_obj.update(self)
        self.alive = helper.bound_check(self,SCREEN_WIDTH,SCREEN_HEIGHT+PLAYER_HEIGHT,0,-5-PLAYER_HEIGHT)

class e_bullet(img_obj):
    def __init__(self, enemy):
        self.type = E_BULLET_TAG
        self.img_path = E_BULLET_IMG_PATH
        self.friction = False
        self.speedlim = False
        self.bound = False
        self.y_velocity = E_BULLET_SPEED
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = enemy.x + enemy.width / 2 - self.width / 2 + 2 * self.x_velocity
        self.y = enemy.y + enemy.height / 2 - self.height / 2 + 2 * self.y_velocity

    def update(self):
        img_obj.update(self)
        self.alive = helper.bound_check(self,SCREEN_WIDTH,SCREEN_HEIGHT)

class p_bullet(img_obj):
    def __init__(self, player):
        img_obj.__init__(self)
        self.type = P_BULLET_TAG
        self.img_path = BULLET_IMG_PATH
        self.friction = False
        self.speedlim = False
        self.bound = False
        self.x_velocity = player.x_velocity + BULLET_SPEED * math.cos(helper.to_radian(player.angle))
        self.y_velocity = player.y_velocity + BULLET_SPEED * -math.sin(helper.to_radian(player.angle))

        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = player.x + player.width / 2 - self.width / 2 + 2 * self.x_velocity
        self.y = player.y + player.height / 2 - self.height / 2 + 2 * self.y_velocity


    def update(self):
        img_obj.update(self)
        self.alive = helper.bound_check(self,SCREEN_WIDTH,SCREEN_HEIGHT)


class backdrop(img_obj):
    def __init__(self):
        img_obj.__init__(self)
        self.type = BACKGROUND_TAG
        self.img_path = BACKGROUND_IMG_PATH
        self.x = 0
        self.y = 0
        self.y_velocity = 0
        self.x_velocity = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

class txt_obj:

    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 32)

    def __init__(self,text):
        self.alive = True
        self.type = TEXT_TAG
        self.text = text
        self.color = (255, 255, 255), (0, 0, 0)
        self.text_surface = self.font.render(self.text, True, self.color[0], self.color[1])
        self.rect = self.text_surface.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.x = 0
        self.y = 0
        self.width = 25
        self.height = 30

    def clicked(self,x,y):
        if (x > self.x and x < self.x + self.width):
            if( y > self.y and y < self.y + self.height):
                return True
        return False

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.color[0], self.color[1])
        self.rect = self.text_surface.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.w = self.width
        self.rect.height = self.height

    def render(self,window):
        window.blit(self.text_surface, self.rect)

class star(img_obj):

    def __init__(self):
        img_obj.__init__(self)
        self.img_path = STAR_IMG_PATH
        self.type = STAR_TAG
        self.friction = False
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = -PLAYER_HEIGHT
        self.y_velocity = random.randint(1,25)
        self.width = random.randint(1,2)
        self.height = self.width
        self.bound = False

    def update(self):
        img_obj.update(self)
        self.alive = helper.bound_check(self, SCREEN_WIDTH, SCREEN_HEIGHT + PLAYER_HEIGHT, 0, -5 - PLAYER_HEIGHT)
