from object import *


class play_button:

    def __init__(self):
        self.play_button = txt_obj("PLAY")
        self.play_button.width = 90
        self.play_button.x = SCREEN_WIDTH / 2 - 50
        self.play_button.y = SCREEN_HEIGHT / 2 - 20

    def clicked(self,x,y):
        return self.play_button.clicked(x,y)

    def update(self):
        self.play_button.update()

    def render(self,window):
        self.play_button.render(window)

class menu:

    def __init__(self):
        self.background = backdrop()
        self.play_button = play_button()

    def play_button_clicked(self,x,y):
        return self.play_button.clicked(x,y)

    def update(self):
        self.background.update()
        self.play_button.update()

    def render(self,window):
        self.background.render(window)
        self.play_button.render(window)