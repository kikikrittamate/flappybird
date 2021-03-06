import random
import tkinter as tk

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
PILLAR_HEIGHT = random.randint(300,800)

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
JUMP_VELOCITY = -20
PILLAR_SPEED = 10

class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False
        self.is_gameover = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
        elif self.is_gameover:
            self.y = 0

    def start(self):
        self.is_started = True

    def jump(self):
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        return self.y >= CANVAS_HEIGHT

    def game_over(self):
        self.is_gameover = True

    def is_hit(self):
        if (self.y > app.pillar_pair.y + 60 or self.y < app.pillar_pair.y - 60) and self.x == app.pillar_pair.x:
            return True
        elif self.x == app.pillar_pair.x and not self.is_gameover:
            app.score.set_text(int(app.score.text) + 1)

class FlappyGame(GameApp):
    def create_sprites(self):
        self.canvas.config(background="lightblue")
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, PILLAR_HEIGHT// 2)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.is_started = False
        self.is_gameover = False
        self.create_sprites()
        self.score = Text(self, 0, 400, 50)

    def pre_update(self):
        pass

    def post_update(self):
        if (self.dot.is_out_of_screen() or self.dot.is_hit()) and not self.is_gameover:
            self.is_gameover = True
            self.pillar_pair.game_over()
            self.dot.game_over()
            Text(app, "GAME OVER", 400, 100)

    def on_key_pressed(self, event):
        if event.char == " ":
            if not (self.is_started or self.is_gameover):
                self.is_started = True
                self.pillar_pair.start()
                self.dot.start()
            elif not self.is_gameover:
                self.dot.jump()

class PillarPair(Sprite):
    def init_element(self):
        self.is_started = False
        self.is_gameover = False


    def start(self):
        self.is_started = True


    def update(self):
        if self.is_started:
            self.x -= 10
            if self.x <= -100:
                self.x = CANVAS_WIDTH
        if self.is_gameover:
            self.x += 10

    def game_over(self):
        self.is_gameover = True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
