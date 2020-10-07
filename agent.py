import random
import copy
import math
import time
import file_logic as fl
from random import seed
from random import randint

turn_length_in_seconds = 9.8


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
        random_pos = random.choice(board.open_positions())
        return [None, random_pos[0], random_pos[1], None]


class AlphaBetaAgent(Agent):
    max_branches = 5

    heuristic_patterns = [
        {
            "00000": 10000000000,
            "-10000-1": 1000,
            "-100001": 500,
            "-1000-1": 100,
            "-10001": 50,
            "-100-1": 10,
            "-1001": 5,
            "-101": 1
        },
        {
            "11111": 10000000000,
            "-11111-1": 1000,
            "-111110": 500,
            "-1111-1": 100,
            "-11110": 50,
            "-111-1": 10,
            "-1110": 5,
            "-110": 1
        }
    ]

    def take_turn(self, board):
        self.timeout = time.time() + turn_length_in_seconds
        depth_limit = 1
        best_move: list = []
        while True:
            current_move = self.alpha_beta(True, -math.inf, math.inf, [board, [], -math.inf], 0, depth_limit)
            if len(current_move) == 0:
                break
            best_move = current_move
            if best_move[2] >= 10000000000:
                break
            print(best_move)
            depth_limit += 1
        print(best_move)
        formatted_move = [best_move[0], best_move[1][0][0], best_move[1][0][1], best_move[2]]
        return formatted_move

    def alpha_beta(self, maximizing_player, alpha, beta, value, depth, depth_limit):
        if time.time() > self.timeout:
            return []
        if depth > depth_limit:
            # print("Current best move: {0}, {1}".format(fl.convert_num_to_alphabet(x), y + 1))
            # print("Value of this move: {0}".format(value))
            # print("Time left: {0}".format(int(self.timeout - time.time())))
            return value
        if maximizing_player:
            children = self.get_children(value[0], self.player, value[1])
            val = [value[0], [], -math.inf, 0]
            for child in children:
                current_move = self.alpha_beta(False, alpha, beta, child, depth + 1, depth_limit)
                if len(current_move) == 0:
                    return current_move
                if current_move[2] > val[2]:
                    val = current_move
                if val[2] >= beta:
                    return val
                alpha = max(val[2], alpha)
            return val
        else:
            children = self.get_children(value[0], int(not self.player), value[1])
            val = [value[0], [], math.inf, 0]
            for child in children:
                current_move = self.alpha_beta(True, alpha, beta, child, depth + 1, depth_limit)
                if len(current_move) == 0:
                    return current_move
                if current_move[2] < val[2]:
                    val = current_move
                if val[2] <= alpha:
                    return val
                beta = min(val[2], beta)
            return val

    def get_children(self, board, player, path: list):
        children = []
        for pos in board.open_positions():
            new_path = copy.deepcopy(path)
            new_path.append(pos)
            child = [copy.deepcopy(board), new_path, 0]
            child[0].update_board(self.player, pos[0], pos[1])
            child[2] = self.get_value(child[0], player)
            if len(children) < self.max_branches:
                children.append(child)
                children.sort(key=sort_heuristic)
            elif child[2] > children[0][2]:
                children.remove(children[0])
                children.append(child)
                children.sort(key=sort_heuristic)
        return children

    def get_value(self, board, player):
        value = 0
        patterns = board.get_patterns()
        for key in self.heuristic_patterns[player]:
            value += patterns[player][key] * self.heuristic_patterns[player][key]
        for key in self.heuristic_patterns[int(not player)]:
            value -= patterns[int(not player)][key] * self.heuristic_patterns[int(not player)][key]
        return value


def sort_heuristic(child: list):
    return child[2]
