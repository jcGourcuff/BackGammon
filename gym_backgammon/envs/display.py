# %% codecell
import sys
import pygame
import time
import numpy as np
import os
root_dir = 'display/'
# %% codecell
# %% codecell
# params
size = width, height = 800, 800

y_high = -55
X = [653, 262, -53, 338]
gap = 63
y_low = 655
pin_size = 47

# %% codecell


class backgammonBoard():

    def __init__(self, delay=.9):

        self.playing = False
        self.init()
        self.current_state = None
        self.delay = delay

    def display(self, board_state):
        n = len(board_state)
        assert len(board_state) == 24
        positions = [[]] * n

        for k in range(n):
            nb = board_state[k]
            coords = self.generate_pos(k, nb=np.abs(nb))
            positions[k] = coords

        for k in range(n):
            if board_state[k] > 0:
                for x in positions[k]:
                    rect = self.black.get_rect()
                    self.screen.blit(self.black, x)
            elif board_state[k] < 0:
                for x in positions[k]:
                    rect = self.white.get_rect()
                    self.screen.blit(self.white, x)

    def generate_pos(self, k, nb=0):
        if nb == 0:
            return []
        else:
            result = []
            for pin in range(nb):
                x, y = X[k // 6], 0

                if k // 6 <= 1:
                    y = y_high + pin * pin_size
                    x = x - (k % 6) * gap
                else:
                    y = y_low - pin * pin_size
                    x = x + (k % 6) * gap
                result.append((x, y))
            return result

    def init(self):
        self.screen = pygame.display.set_mode(size)

        self.board = pygame.image.load(root_dir + "gammon_board.png")
        self.boardrect = self.board.get_rect()

        white = pygame.image.load(root_dir + "white_pin.jpg")
        self.white = pygame.transform.scale(white, (200, 200))

        black = pygame.image.load(root_dir + "black_pin.jpg")
        self.black = pygame.transform.scale(black, (200, 200))

    def play(self, input, delay=None):
        if delay is None:
            delay = self.delay
        self.playing = True
        count = 0
        pygame.init()
        nb_i = 1
        state = input
        if type(state[0]) != int:
            nb_i = len(state)

        while(self.playing and count < nb_i):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                    self.playing = False

            self.screen.fill((255, 255, 255))
            if type(state[0]) == int:
                self.display_one_state(state)
            else:
                self.display_one_state(state[count])
            count += 1
            pygame.display.update()
            time.sleep(delay)

    def display_one_state(self, board_state):
        self.screen.blit(self.board, self.boardrect)
        self.display(board_state)

    def kill(self):
        pygame.display.quit()
        sys.exit()
        self.playing = False
