import random
import math


class Agent(object):
    def __init__(self, name):
        self.name = name
        self.player = None

    def take_turn(self, board):
        raise NotImplementedError("implement")


class RandomAgent(Agent):
    def take_turn(self, board):
        return random.choice(board.open_positions())


class AlphaBetaAgent(Agent):
    def take_turn(self, board):
        return self.alpha_beta(board, True, -math.inf, math.inf, -1, -1)

    def alpha_beta(self, board, maximizing_player, alpha, beta, x, y):
        if board.end_state():
            return  # tuple of move you want to make?
        elif maximizing_player:
            children = board.get_children()
            val = (x, y, -math.inf)
            for child in children:
                val[2] = max(val[2], self.alpha_beta(child[0], False, alpha, beta, child[1], child[2]))
                if val[2] >= beta:
                    return val
                alpha = max(val[2], alpha)
            return val
        else:
            children = board.get_children()
            val = math.inf
            for child in children:
                val[2] = min(val[2], self.alpha_beta(child[0], True, alpha, beta, child[1], child[2]))
                if val[2] <= alpha:
                    return val
                beta = min(val[2], beta)
            return val


    def get_value(self, board):
        return