from object import *


class button:

    def __init__(self,text):
        self.button = txt_obj(text)
        self.button.width = 90
        self.button.x = SCREEN_WIDTH / 2 - 50
        self.button.y = SCREEN_HEIGHT / 2 - 20

    def clicked(self,x,y):
        return self.button.clicked(x,y)

    def update(self):
        self.button.update()

    def render(self,window):
        self.button.render(window)

class menu:

    def __init__(self):
        self.background = backdrop()
        self.play_button = button("PLAY")
        self.quit_button = button("QUIT")
        self.play_button.button.y = SCREEN_HEIGHT / 2 - 25
        self.quit_button.button.y = SCREEN_HEIGHT / 2 + 25

    def play_button_clicked(self,x,y):
        return self.play_button.clicked(x,y)

    def quit_button_clicked(self,x,y):
        return self.quit_button.clicked(x,y)

    def update(self):
        self.background.update()
        self.play_button.update()
        self.quit_button.update()

    def render(self,window):
        self.background.render(window)
        self.play_button.render(window)
        self.quit_button.render(window)