import pygame
import math
import random

import helper
from settings import *
from helper import *

class img_obj:

    def __init__(self):
        self.alive = True
        self.type = PLAYER_TAG
        self.img_path = PLAYER_IMG_PATH
        self.x = SCREEN_WIDTH/2 - PLAYER_WIDTH/2
        self.y = SCREEN_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.angle = 90
        self.angle_velocity = 0
        self.x_velocity = 0
        self.y_velocity = 1
        self.friction = True
        self.speedlim = True
        self.bound = True

    def render(self,window):
        window.blit(self.img, (self.x,self.y))

    def update(self):

        self.x = self.x + self.x_velocity
        self.y = self.y + self.y_velocity
        self.angle = self.angle + self.angle_velocity
        if self.friction:
            self.x_velocity = self.x_velocity * (1-FRICTION)
            self.y_velocity = self.y_velocity * (1-FRICTION)
            self.angle_velocity = self.angle_velocity * (1-ANGULAR_FRICTION)

        if self.speedlim:
            helper.limit_vector(self)

        if self.bound:
            helper.bound_screen_space(self)

        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.rotate(self.img, self.angle)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))  # Scale the image to fit the window

    def brake(self):
        self.x_velocity = 0.9*self.x_velocity
        self.y_velocity = 0.9*self.y_velocity

class enemy(img_obj):
    def __init__(self):
        img_obj.__init__(self)
        self.img_path = ENEMY_IMG_PATH
        self.type = ENEMY_TAG
        self.friction = False
        self.x = random.randint(0,SCREEN_WIDTH)
        self.y = 10
        self.angle = 270
        self.y_velocity = ENEMY_SPEED
        self.bound = False

    def update(self):
        img_obj.update(self)
        self.alive = helper.bound_check(self,SCREEN_WIDTH,SCREEN_HEIGHT)

class bullet(img_obj):
    def __init__(self, player):
        img_obj.__init__(self)
        self.type = P_BULLET_TAG
        self.img_path = BULLET_IMG_PATH
        self.friction = False
        self.speedlim = False
        self.bound = False
        self.angle = player.angle+90
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
        self.text_surface = self.font.render(self.text, True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text_surface.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 20

    def update(self):
        self.text_surface = self.font.render(self.text, True, (255, 255, 255), (0, 0, 0))
        self.rect = self.text_surface.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.w = self.width
        self.rect.height = self.height

    def render(self,window):
        window.blit(self.text_surface, self.rect)