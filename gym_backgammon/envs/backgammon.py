import gym
import numpy as np
import random


class Backgammon(gym.Env):

    def __init__(self, black_ia):
        self.state = State()
        self.white = WhiteAgent(self.state)
        self.black_ia = black_ia

    def play(self, action):
        for move in action:
            self.state.compute_state(move)
        #print('black player s turn')
        self.state.update_board(reverse=True)
        #print('the board is :')
        #print(self.state.board)
        self.roll()
        #print('the dices are :')
        #print(self.dices)
        self.black = BlackAgent(self.state, ia = self.black_ia)
        self.black_action = self.black.play(self.dices)
        for move in self.black_action:
            #print('the move os :')
            #print(move)
            self.state.compute_state(move, black_agent=True)
            #print('the new board is :')
            #print(self.state.board)
        self.state.update_board(reverse=True)

    def roll(self):
        self.dices = [np.random.randint(1, 6), np.random.randint(1, 6)]

    def get_observation(self):
        return self.state.board


class State():

    def __init__(self, state=None, move=None, black_agent=False, args = None):

        if state == None:
            self.starting_positions()
            self.off_board = {'white': 0, 'black': 0}
            self.barred = {'white': 0, 'black': 0}

        elif move == None and state != None:
            self.off_board = state.off_board
            self.barred = state.barred.copy()

            self.board = state.board.copy()
        elif args != None :
            #args = board
            self.board = args
            self.off_board = {'white': self.board[24], 'black': self.board[25]}
            self.barred = {'white': self.board[26], 'black': self.board[27]}

        else:
            self.compute_state(move, state, black_agent)

    def get_playfield(self):
        return self.board[:24]

    def starting_positions(self):
        self.board = [0 for i in range(28)]
        self.board[0] = -2
        self.board[5] = self.board[12] = 5
        self.board[7] = 3
        self.board[11] = self.board[18] = -5
        self.board[16] = -3
        self.board[23] = 2
        self.board[24:] = [0 for i in range(4)]

    def compute_state(self, move, previous_state=None, black_agent=False):

        board = None
        if previous_state != None:
            board = previous_state.board.copy()
            self.off_board = previous_state.off_board.copy()
            self.barred = previous_state.barred.copy()
        else :
            board = self.board

        #
        # print('the previous board is :')
        # print(board)
        # print('the move is :')
        # print(move)
        agent = 'white'
        opponent = 'black'
        if black_agent:
            agent = 'black'
            opponent = 'white'

        if self.barred[agent] > 0 and move[1] != 0:
            self.barred[agent] -= 1

        if move[0]-move[1] < 0 :
            board[move[0]] -= 1
            self.off_board[agent] += 1

        elif board[move[0]-move[1]] == -1 :
            board[move[0]] -= 1
            board[move[0] - move[1]] = 1
            self.barred[opponent] += 1
        else :
            board[move[0]] -= 1
            board[move[0] - move[1]] += 1


        self.board = board

        # print('the new board is: ')
        # print(self.board)
        self.update_board()

    def win(self):
        if self.off_board['white'] == 15:
            return 1
        if self.off_board['black'] == 15:
            return -1
        return 0

    def update_board(self, reverse=False):

        if reverse:
            self.board = reverse_view(self.board)

        self.board[24] = self.off_board['white']
        self.board[25] = self.off_board['black']
        self.board[26] = self.barred['white']
        self.board[27] = self.barred['black']


class WhiteAgent():

    def __init__(self, state):

        self.state = state

    def possible_moves(self, dice, state=None):
        moves = []
        if state == None:
            state = self.state
        if state.barred['white'] == 0:
            for i in range(24):
                if state.board[i] > 0 :
                    if i-dice < 0 or state.board[i - dice] in [i for i in range(-1,9)] :
                        moves.append((i, dice))

            if len(moves) == 0:
                moves.append((0, 0))
        else:
            if state.board[24 - dice] >= -1:
                moves.append((24, dice))
            else :
                moves.append((0,0))

        return moves


class BlackAgent():

    def __init__(self, state, ia):

        self.state = state
        self.ia= ia

    def play(self, dices):
        out = []
        if dices[0] != dices[1]:
            n = random.randint(0, 1)
            d1 = dices[n]
            d2 = dices[1 - n]
            moves = self.possible_moves(self.state, d1)
            #print('first moves :')
            #print(moves)
            m1 = self.choose_move(moves)
            #print(m1)
            new_state = State(self.state, m1, black_agent=True)
            #print('new state')
            #print(new_state.board)
            moves_2 = self.possible_moves(new_state, d2)
            #print('moves_2')
            #print(moves_2)
            m2 = self.choose_move(moves_2)
            #print('m2')
            #print(m2)
            out = [m1, m2]
        else:
            d = dices[0]
            moves_1 = self.possible_moves(self.state, d)
            m1 = self.choose_move(moves_1)
            new_state_1 = State(self.state, m1, black_agent=True)
            moves_2 = self.possible_moves(new_state_1, d)
            m2 = self.choose_move(moves_2)
            new_state_2 = State(new_state_1, m2, black_agent=True)
            moves_3 = self.possible_moves(new_state_2, d)
            m3 = self.choose_move(moves_3)
            new_state_3 = State(new_state_2, m3, black_agent=True)
            moves_4 = self.possible_moves(new_state_3, d)
            m4 = self.choose_move(moves_4)
            out = [m1, m2, m3, m4]
        return out

    def choose_move(self, moves):
        if self.ia=='random':
            return random.sample(moves, 1)[0]
        else :
            possible_next_states = [State(state = init_state, move = m) for m in moves]
            _, _, idx = BlackAgent.max_value(possible_next_states)
            move = moves[idx]
            return move

    @staticmethod
    def get_score(board):
      """
        Gives scores from a board of size 28 (without dices rolls)
        Normalized.
      """
      if board[24] == 15 :
        return 1
      else :
        max_score = 15*24
        result = 0
        result+= (board[24]-board[25])*24
        for k,pins in enumerate(board[:24]) :
          pos = 23 - k
          if pins > 0 :
            if pins > 1 :
              result += pins*((pos//6+1)*6)
            else :
              result+= (pos//6)*6 + 1
        return result/max_score

    @staticmethod
    def max_value(resulting_states):
      """
        Takes a list of stae and returns
        s : the state having the highest score
        m : the corresponding state score
        i : the corresponfing index in the list
      """
      s = resulting_states[0]
      m = BlackAgent.get_score(s.board)
      i=0
      for k,res in enumerate(resulting_states[1:]) :
        sc = BlackAgent.get_score(res.board)
        if sc > m :
          m = sc
          s = res
          i=k
      return m,s,i



    def possible_moves(self, state, dice):
        moves = []

        if state == None:
            state = self.state

        if state.barred['black'] == 0:
            for i in range(24):
                if state.board[i] > 0 :
                    if i-dice < 0 or state.board[i - dice] in [i for i in range(-1,9)] :
                        moves.append((i, dice))

            if len(moves) == 0:
                moves.append((0, 0))
        else:

            if state.board[24 - dice] >= -1:
                moves.append((24, dice))
            else :
                moves.append((0,0))

        return moves


def reverse_view(board):
    new_board = [-board[i]
                 for i in range(23, -1, -1)] + [board[i] for i in range(24, len(board))]
    return new_board
