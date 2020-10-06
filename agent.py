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
    max_branches = 5

    heuristic_patterns = {
        "00000": 10000000000,
        "-10000-1": 1000,
        "-100001": 500,
        "-1000-1": 100,
        "-10001": 50,
        "-100-1": 10,
        "-1001": 5,
        "-101": 1
    }

    def take_turn(self, board):
        self.timeout = time.time() + turn_length_in_seconds
        return self.alpha_beta(board, True, -math.inf, math.inf, -1, -1, -math.inf)

    def alpha_beta(self, board, maximizing_player, alpha, beta, x, y, value):
        if (time.time() >= self.timeout):
            # print("Current best move: {0}, {1}".format(fl.convert_num_to_alphabet(x), y + 1))
            # print("Value of this move: {0}".format(value))
            # print("Time left: {0}".format(int(self.timeout - time.time())))
            return (board, x, y, value)
        elif maximizing_player:
            children = self.get_children(board, self.player)
            val = list((board, x, y, -math.inf))
            for child in children:
                currentmove = self.alpha_beta(child[0], False, alpha, beta, child[1], child[2], child[3])
                if (currentmove[3] > val[3]):
                    val[0] = currentmove[0]
                    val[1] = currentmove[1]
                    val[2] = currentmove[2]
                    val[3] = max(val[3], currentmove[3])
                if val[3] >= beta:
                    return val
                alpha = max(val[3], alpha)
            return val
        else:
            children = self.get_children(board, int(not self.player))
            val = list((board, x, y, math.inf))
            for child in children:
                currentmove = self.alpha_beta(child[0], True, alpha, beta, child[1], child[2], child[3])
                if (currentmove[3] < val[3]):
                    val[0] = currentmove[0]
                    val[1] = currentmove[1]
                    val[2] = currentmove[2]
                    val[3] = min(val[3], currentmove[3])
                if val[3] <= alpha:
                    return val
                beta = min(val[3], beta)
            return val

    def get_children(self, board, player):
        children = []
        for pos in board.open_positions():
            child = [copy.deepcopy(board), pos[0], pos[1], 0]
            child[0].update_board(self.player, pos[0], pos[1])
            child[3] = self.get_value(child[0], player)
            if len(children) < self.max_branches:
                children.append(child)
                children.sort(key=sort_heuristic)
            elif child[3] > children[0][3]:
                children.remove(children[0])
                children.append(child)
                children.sort(key=sort_heuristic)
        return children

    def get_value(self, board, player):
        value = 0
        patterns = board.get_patterns()
        for key in self.heuristic_patterns:
            value += patterns[player][key] * self.heuristic_patterns[key]
            value -= patterns[int(not player)][key] * self.heuristic_patterns[key]
        return value


def sort_heuristic(child: list):
    return child[3]
