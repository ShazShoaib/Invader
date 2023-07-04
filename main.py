import pygame
from helper import *  # this has all sorts of helpful functions
from menuManager import *
from object import *  # this has the Classes for Objects used in the game
from settings import *  # this has setting and config values
from highscore import *

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

if MENU_ENABLED:
    main_menu = menu()
    in_menu = True

    while in_menu:
        x = -1                                                             # mouse click coordinate x
        y = -1                                                             # mouse click coordinate y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
                x, y = event.pos

        if main_menu.play_button_clicked(x, y):                            # check if clicked play button
            in_menu = False
        elif main_menu.quit_button_clicked(x,y):                           # check if clicked quit button
            exit(0)

        main_menu.update()
        main_menu.render(window)
        pygame.display.flip()
        clock.tick(FPS)

obj_list = []  # Stores all game objects
frames = 0  # Total number of frames elapsed
E_timer = 0  # To Generate Enemies with a delay
S_timer = 0  # To Generate Stars with a delay

background = backdrop()  # The Background of the game
fps_text = txt_obj(str(FPS))  # The FPS counter

score = 0  # Player Score
score_text = txt_obj('SCORE ' + str(score))  # To Display Player Score
score_text.y = SCREEN_HEIGHT - 50  # Set position screen
player = player()  # Create the Player

obj_list.append(background)  # Add background as a object to list
obj_list.append(fps_text)  # Add the FPS counter as a object to list
obj_list.append(score_text)  # Add Score Display as a object to list
obj_list.append(player)  # Add the Player as a object to list
obj_list.append(enemy())  # Add a single Enemy as a object to list

running = True  # manages when the game runs/ends
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        set_input(event)
    manage_input(player, obj_list)  # Player Input is managed in a helper function

    if E_timer > ENEMY_DELAY:  # Generates enemies with a delay
        E = enemy()
        obj_list.append(E)
        E_timer = 0
        print(len(obj_list))
    if S_timer > STAR_DELAY:
        star1 = star()
        obj_list.append(star1)
        S_timer = 0

    for fiend in obj_list:  # check enemy collision
        if fiend.type == ENEMY_TAG:
            for p_attack in obj_list:
                if p_attack.type == P_BULLET_TAG:  # check for player bullet
                    if collide_check(p_attack, fiend):  # if enemy collides with a player bullet
                        p_attack.alive = False  # bullet is destroyed
                        fiend.alive = False  # enemy is destroyed
                        obj_list.append(explosion(fiend.x, fiend.y))
                        score = score + 10  # score is increased
                        score_text.text = 'SCORE ' + str(score)  # score display updated
                        break
                if p_attack.type == PLAYER_TAG:  # check for player
                    if collide_check(p_attack, fiend):  # if enemy collides with the player
                        for obj in obj_list:
                            obj.alive = False  # everything is destroyed
                        score_text.alive = True  # except score text
                        background.alive = True  # and background

                        game_over_text = txt_obj("GAME OVER")  # game over text is made
                        game_over_text.x = SCREEN_WIDTH / 2 - 100  # game over text is positioned
                        game_over_text.y = 50
                        score_text.x = SCREEN_WIDTH / 2 - 70  # score text is repositioned
                        score_text.y = SCREEN_HEIGHT / 2 - 150
                        obj_list.append(game_over_text)  # game over text added to object list

                        insert_scores(obj_list,score)




    for i in range(len(obj_list) - 1, 0, -1):  # remove all items which are marked as destroyed
        if not obj_list[i].alive:
            del obj_list[i]

    for game_obj in obj_list:  # Update all game objects
        game_obj.update()

    window.fill((0, 0, 0))  # Clear the window

    for image in obj_list:
        image.render(window)  # Render the image onto the window

    pygame.display.flip()  # Update the display
    curr_frames = clock.tick(FPS) / FPS  # get the current frame rate
    frames = frames + curr_frames  # update the number of frames elapsed
    E_timer = E_timer + curr_frames  # update the timer for enemy generation
    S_timer = S_timer + curr_frames  # update the timer for star generation

    player.cooldown(curr_frames)  # cooldown player specials
    fps_text.text = str(int(clock.get_fps()))  # update FPS counter display

pygame.quit()
