import gym
from gym import error, spaces, utils
from gym.utils import seeding
from envs.display import backgammonBoard
import importlib
from envs.backgammon import Backgammon
import numpy as np
import random


class BackgammonEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = Backgammon()

        low = [-9 for i in range(24)]  # board information - lowest
        high = [9 for i in range(24)]  # board information - highest
        # Numbers of white / black checkers out, numbers of white / black ckeckers barred - lowest
        low += [0, 0, 0, 0, 0]
        # Numbers of white / black checkers out, numbers of white / black ckeckers barred - highest
        high += [15, 15, 15, 15, 1]

        #self.observation_space = Box(low=low, high=high)
        self.counter = 0
        self.max_length_episode = 10000
        self.viewer = None  # backgammonBoard(delay=1)

    def step(self, action):
        self.game.play(action)
        observation = self.game.get_observation()

        reward = 0
        done = False

        winner = self.game.state.win()

        if winner != 0:
            done = True
            if winner == 1:
                reward = 1

        self.counter += 1

        return observation, reward, done, winner

    def reset(self):
        self.game = Backgammon()

    def render(self, mode='human', close=False):
        # self.viewer.play(self.game.state.board[:24])
        print(self.game.state.board)

    def get_action_space(self, dice):
        return self.game.white.possible_moves(dice)

"""
env = BackgammonEnv()
env.reset()
# print(env.game.state.board)
env.game.roll()
print(env.game.dices)
print(env.game.get_observation())
# env.game.state.compute_state((5,4,0))
# env.game.state.update_board(black_agent=True)
# print(env.game.state.board)
# env.game.state.compute_state((23,1,-1), black_agent=True)
# env.game.state.update_board(black_agent=False)
# print(env.game.state.board)
# env.game.state.compute_state((5,6,1), black_agent=False)
# env.game.state.update_board(black_agent=True)

action_space = [env.get_action_space(d) for d in env.game.dices]
print(np.array(action_space).shape)
print(action_space[0])
action = random.sample(action_space, 1)
print(action)
env.reset()
print(env.game.state.board)
env.game.state.board[0] = -1
env.game.state.board[27] = 1

env.step([(23, 3, -1), (5, 2, 0)])

env.render()
moves = [(7, 5, 0), (12, 5, 0)]
m = random.sample(moves, 1)
m
"""
