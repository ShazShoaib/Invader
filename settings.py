import pygame

FPS = 30                                                    # linked to game speed
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
MENU_ENABLED = True

FRICTION = 0.01
ANGULAR_FRICTION = 0.01
BACKGROUND_IMG_PATH = 'sprites/background.png'

PLAYER_TAG = 0
ENEMY_TAG = 1
P_BULLET_TAG = 2
BACKGROUND_TAG = 3
STAR_TAG = 4
TEXT_TAG = 5
EXPLOSION_TAG = 6
HIGHSCORE_TAG = 7


PLAYER_IMG_PATH = 'sprites/player.png'
PLAYER_SPEED = 5
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 30
ATTACK_COOLDOWN = 15
WARP_SPEED = 150
WARP_COOLDOWN = 150

BULLET_IMG_PATH = 'sprites/player_attack.png'
BULLET_SPEED = 10
BULLET_HEIGHT = 10
BULLET_WIDTH = 10

ENEMY_IMG_PATH = 'sprites/enemy.png'
ENEMY_DELAY = 30
ENEMY_SPEED = 2

EXPLOSION_IMG_PATH = 'sprites/explosion.png'
EXPLOSION_SIZE = 25
EXPLOSION_ROTATION = 3
EXPLOSION_DETERIORATION = 3

STAR_IMG_PATH = 'sprites/Star.png'
STAR_DELAY = 5