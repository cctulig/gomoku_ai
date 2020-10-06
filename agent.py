import random
import copy
import math
import time
import file_logic as fl
from random import seed
from random import randint

turn_length_in_seconds = 9.9

class Agent(object):
    def __init__(self, name):
        self.name = name
        self.player = None
        self.timeout = 0
        seed(1)

    def take_turn(self, board):
        raise NotImplementedError("implement")


class RandomAgent(Agent):
    def take_turn(self, board):
        return random.choice(board.open_positions())


class AlphaBetaAgent(Agent):
    def take_turn(self, board):
        self.timeout = time.time() + turn_length_in_seconds
        return self.alpha_beta(board, True, 0, -math.inf, math.inf, -1, -1)

    def alpha_beta(self, board, maximizing_player, depth, alpha, beta, x, y):
        if (depth  >= 4 or time.time() >= self.timeout):
            #print("Current best move: {0}, {1}".format(fl.convert_num_to_alphabet(x), y + 1))
            value = randint(0, 100)
            #print("Value of this move: {0}".format(value))
            print("Time left: {0}".format(int(self.timeout - time.time())))
            return (board, x, y, value)
        elif maximizing_player:
            children = self.get_children(board)
            val = list((board, x, y, -math.inf))
            for child in children:
                currentmove = self.alpha_beta(child[0], False, depth+1, alpha, beta, child[1], child[2])
                if(currentmove[3] > val[3]):
                    val[0] = currentmove[0]
                    val[1] = currentmove[1]
                    val[2] = currentmove[2]
                    val[3] = max(val[3], currentmove[3])
                if val[3] >= beta:
                    return val
                alpha = max(val[3], alpha)
            return val
        else:
            children = self.get_children(board)
            val = list((board, x, y, math.inf))
            for child in children:
                currentmove = self.alpha_beta(child[0], True, depth+1, alpha, beta, child[1], child[2])
                if (currentmove[3] < val[3]):
                    val[0] = currentmove[0]
                    val[1] = currentmove[1]
                    val[2] = currentmove[2]
                    val[3] = min(val[3], currentmove[3])
                if val[3] <= alpha:
                    return val
                beta = min(val[3], beta)
            return val


    def get_children(self, board):
        children = []
        for pos in board.open_positions():
            child = (copy.deepcopy(board), pos[0], pos[1])
            child[0].update_board(self.player, pos[0], pos[1])
            children.append(child)
        return children

    def get_value(self, board):
        return