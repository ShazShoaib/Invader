import pygame
from helper import *                                                       # this has all sorts of helpful functions
from object import *                                                       # this has the Classes for Objects used in the game
from settings import *                                                     # this has setting and config values

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
obj_list = []                                                              # Stores all game objects
frames = 0                                                                 # Total number of frames elapsed
E_timer = 0                                                                # To Generate Enemies with a delay

background = backdrop()                                                    # The Background of the game
fps_text = txt_obj(str(FPS))                                               # The FPS counter

score = 0                                                                  # Player Score
score_text = txt_obj('SCORE '+str(score))                                  # To Display Player Score
score_text.y = SCREEN_HEIGHT - 50                                          # Set position screen
player = player()                                                          # Create the Player

obj_list.append(background)                                                # Add background as a object to list
obj_list.append(fps_text)                                                  # Add the FPS counter as a object to list
obj_list.append(score_text)                                                # Add Score Display as a object to list
obj_list.append(player)                                                    # Add the Player as a object to list
obj_list.append(enemy())                                                   # Add a single Enemy as a object to list

running = True                                                             # manages when the game runs/ends
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        set_input(event)
    manage_input(player,obj_list)                                          # Player Input is managed in a helper function

    if E_timer > ENEMY_DELAY:                                              # Generates enemies with a delay
        E = enemy()
        obj_list.append(E)
        E_timer = 0

    for fiend in obj_list:                                                 # check enemy collision
        if fiend.type == ENEMY_TAG:
            for object in obj_list:
                if object.type == P_BULLET_TAG:                            # check for player bullet
                    if collide_check(object, fiend):                       # if enemy collides with a player bullet
                        object.alive = False                               # bullet is destroyed
                        fiend.alive = False                                # enemy is destroyed
                        obj_list.append(explosion(fiend.x,fiend.y))
                        score = score + 10                                 # score is increased
                        score_text.text = 'score ' + str(score)            # score display updated
                        break
                if object.type == PLAYER_TAG:                              # check for player
                    if collide_check(object, fiend):                       # if enemy collides with the player
                        for obj in obj_list:
                            obj.alive = False                              # everything is destroyed
                        score_text.alive = True                            # except score text
                        background.alive = True                            # and background

                        game_over_text = txt_obj("GAME OVER")              # game over text is made
                        game_over_text.x = SCREEN_WIDTH/2 -100             # game over text is positioned
                        game_over_text.y = 50
                        score_text.x = SCREEN_WIDTH/2 - 75                 # score text is repositioned
                        score_text.y = SCREEN_HEIGHT/2
                        obj_list.append(game_over_text)                    # game over text added to object list


    for i in range(len(obj_list)-1,0,-1):                                  # remove all items which are marked as destroyed
        if not obj_list[i].alive:
            del obj_list[i]

    for game_obj in obj_list:                                              # Update all game objects
        game_obj.update()

    window.fill((0, 0, 0))                                                 # Clear the window

    for image in obj_list:
        image.render(window)                                               # Render the image onto the window

    pygame.display.flip()                                                  # Update the display
    curr_frames =  clock.tick(FPS)/FPS                                     # get the current frame rate
    frames = frames + curr_frames                                          # update the number of frames elapsed
    E_timer = E_timer + curr_frames                                        # update the timer for enemy generation

    fps_text.text = str(int(clock.get_fps()))                              # update FPS counter display


pygame.quit()
