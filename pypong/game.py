import pygame, random, sys, time
from pygame.locals import *

MAX_SCORE = 5
FPS = 60
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PAD_WIDTH = SCREEN_WIDTH // 40
PAD_HEIGHT = SCREEN_HEIGHT // 5
BALL_RADIUS = 5
PAD_STEP_MOVE = 5
BALL_STEP_MOVE = 5
GAME_OVER_TEXT = "Game Over. Press [N] for New Game."
VOLLEY_PAUSE = 2

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, left_pad, right_pad, left_up_callback, right_up_callback):
        super().__init__() 
        self.image = pygame.Surface([radius*2, radius*2])
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x,y))
        self.h_velo = BALL_STEP_MOVE
        self.v_velo = 0
        self.radius = radius
        self.left_pad = left_pad
        self.right_pad = right_pad
        self.left_up_callback = left_up_callback
        self.right_up_callback = right_up_callback
        self.pop = pygame.mixer.Sound('pop.wav')

    def move(self):
        self.rect.move_ip(self.h_velo, self.v_velo)
        for pad in [self.left_pad, self.right_pad]:
            if self.rect.colliderect(pad.rect):
                self.pop.play()
                self.h_velo *= -1
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pad.key_up]:
                    self.v_velo -= 1
                elif pressed_keys[self.left_pad.key_down]:
                    self.v_velo += 1
                return

        if self.h_velo > 0 and self.rect.right >= SCREEN_WIDTH:
            # bounce right wall, reverse ball's horizontal velocity, increase left score
            self.h_velo *= -1
            self.v_velo = 0
            self.pop.play(VOLLEY_PAUSE)
            self.left_up_callback()
            time.sleep(VOLLEY_PAUSE)

        elif self.h_velo < 0 and self.rect.left <= 0:
            # bounce left wall, reverse ball's horizontal velocity
            self.h_velo *= -1
            self.v_velo = 0
            self.pop.play(VOLLEY_PAUSE)
            self.right_up_callback()
            time.sleep(VOLLEY_PAUSE)

        if self.v_velo > 0 and self.rect.bottom >= SCREEN_HEIGHT - self.radius or self.v_velo < 0 and self.rect.top <= self.radius:
            # bounce bottom or top wall, reverse ball's vertical velocity
            self.v_velo *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Pad(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, key_up, key_down):
       super().__init__()
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       self.rect = self.image.get_rect(center = (x,y))
       self.key_up = key_up
       self.key_down = key_down

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > PAD_STEP_MOVE:
              if pressed_keys[self.key_up]:
                  self.rect.move_ip(0, -PAD_STEP_MOVE)
        if self.rect.bottom < SCREEN_HEIGHT - PAD_STEP_MOVE:        
              if pressed_keys[self.key_down]:
                  self.rect.move_ip(0, PAD_STEP_MOVE)

    def draw(self, surface):
        surface.blit(self.image, self.rect)     


class Game():
    def __init__(self):
        pygame.init()
        self.FramePerSec = pygame.time.Clock()
        self.display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.display.fill(BLACK)
        pygame.display.set_caption("Game")
        self.left_score = 0
        self.right_score = 0

        def left_up(): self.left_score += 1
        def right_up(): self.right_score += 1
        
        self.left_pad = Pad(0 + PAD_WIDTH//2, SCREEN_HEIGHT//2, PAD_WIDTH, PAD_HEIGHT, BLUE, K_a, K_z)
        self.right_pad = Pad(SCREEN_WIDTH - PAD_WIDTH//2, SCREEN_HEIGHT//2, PAD_WIDTH, PAD_HEIGHT, RED, K_UP, K_DOWN)
        self.ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_RADIUS, WHITE, self.left_pad, self.right_pad, left_up, right_up)

    def run(self):
        while True:     
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            if max(self.left_score, self.right_score) < MAX_SCORE:
                self.left_pad.update()
                self.right_pad.update()
                self.ball.move()
                self.display.fill(BLACK)
                self.left_pad.draw(self.display)
                self.right_pad.draw(self.display)
                self.ball.draw(self.display)
                score_text = f"{self.left_score} : {self.right_score}"
                self.text_to_screen(self.display, score_text, SCREEN_WIDTH//2, 0)
            else:
                self.text_to_screen(self.display, GAME_OVER_TEXT, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_n]:
                    self.left_score = 0
                    self.right_score = 0

            pygame.display.update()
            self.FramePerSec.tick(FPS)

    def text_to_screen(self, screen, text, x, y, size=30, color = WHITE):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        rendered_text = font.render(str(text), True, color)
        text_rect = rendered_text.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(rendered_text, text_rect)

if __name__ == '__main__':
    Game().run()