import random
import copy
import math
import time
from random import seed

turn_length_in_seconds = 9.7


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
        random_pos = random.choice(board.all_open_positions())
        return [None, random_pos[0], random_pos[1], None]


class AlphaBetaAgent(Agent):
    max_branches = 8

    heuristic_patterns = [
        {
            "00000": 10000000,
            "-10000-1": 10000,
            "-100001": 100,
            "-1000-1": 1000,
            "-10001": 0,
            "-100-1": 10,
            "-1001": 0,
            "-101": 0
        },
        {
            "11111": 10000000,
            "-11111-1": 10000,
            "-111110": 100,
            "-1111-1": 1000,
            "-11110": 0,
            "-111-1": 10,
            "-1110": 0,
            "-110": 0
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
            # print(best_move)
            depth_limit += 1
        formatted_move = [best_move[0], best_move[1][0][0], best_move[1][0][1], best_move[2]]
        return formatted_move

    def alpha_beta(self, maximizing_player, alpha, beta, value, depth, depth_limit):
        if time.time() > self.timeout:
            return []
        if depth > depth_limit or value[0].winning_pattern_exists():
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
        for pos in board.reduced_open_positions():
            new_path = copy.deepcopy(path)
            new_path.append(pos)
            child = [copy.deepcopy(board), new_path, 0]
            child[0].update_board(player, pos[0], pos[1])
            child[2] = self.get_value(child[0])
            if player == self.player:
                if len(children) < self.max_branches:
                    children.append(child)
                    children.sort(key=sort_heuristic)
                elif child[2] > children[0][2]:
                    children.remove(children[0])
                    children.append(child)
                    children.sort(key=sort_heuristic)
            else:
                if len(children) < self.max_branches:
                    children.append(child)
                    children.sort(key=sort_heuristic, reverse=True)
                elif child[2] < children[0][2]:
                    children.remove(children[0])
                    children.append(child)
                    children.sort(key=sort_heuristic, reverse=True)
        return children

    def get_value(self, board):
        value = 0
        patterns = board.get_patterns()
        for key in self.heuristic_patterns[self.player]:
            value += patterns[self.player][key] * self.heuristic_patterns[self.player][key]
        for key in self.heuristic_patterns[int(not self.player)]:
            value -= patterns[int(not self.player)][key] * self.heuristic_patterns[int(not self.player)][key]
        return value


def sort_heuristic(child: list):
    return child[2]
