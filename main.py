import pygame

from helper import *
from object import *
from settings import *

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
obj_list = []
frames = 0
E_timer = 0

background = backdrop()
fps_text = txt_obj('60')
fps_text.width = 10

score = 0
score_text = txt_obj('SCORE '+str(score))
score_text.width = 10
score_text.y = SCREEN_HEIGHT - 50
player = img_obj()



obj_list.append(background)
obj_list.append(fps_text)
obj_list.append(score_text)
obj_list.append(player)
obj_list.append(enemy())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        set_input(event)
    manage_input(player,obj_list)

    if E_timer > ENEMY_DELAY:
        E = enemy()
        obj_list.append(E)
        E_timer = 0

    for game_obj in obj_list:
        game_obj.update()

    for i in range(len(obj_list)):
        fiend = obj_list[i]
        if fiend.type == ENEMY_TAG:
            for j in range(len(obj_list)):
                object = obj_list[j]
                if object.type == P_BULLET_TAG:
                    if collide_check(object, fiend):
                        object.alive = False
                        fiend.alive = False
                        score = score + 10
                        score_text.text = 'score ' + str(score)
                        break
                if object.type == PLAYER_TAG:
                    if collide_check(object, fiend):
                        print("END")
                        for obj in obj_list:
                            obj.alive = False
                        game_over_text = txt_obj("GAME OVER")
                        game_over_text.x = SCREEN_WIDTH/2 -100
                        game_over_text.y = 50
                        score_text.x = SCREEN_WIDTH/2 - 75
                        score_text.y = SCREEN_HEIGHT/2
                        obj_list.append(game_over_text)
                        score_text.alive = True
                        background.alive = True

    for i in range(len(obj_list)-1,0,-1):
        if not obj_list[i].alive:
            del obj_list[i]

    window.fill((0, 0, 0))                      # Clear the window

    for image in obj_list:
        image.render(window)                    # Render the image onto the window

    pygame.display.flip()                       # Update the display
    curr_frames =  clock.tick(FPS)/FPS
    frames = frames + curr_frames
    E_timer = E_timer + curr_frames

    fps_text.text = str(int(clock.get_fps()))


pygame.quit()
