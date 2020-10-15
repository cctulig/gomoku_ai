import random
import copy
import math
import time
from random import seed

from copier import copy_2d_list

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
    max_branches = 15

    heuristic_patterns = [
        [
            {
                "00000": 10000000,
                "-10000-1": 10000,
                "-100001": 100,
                "-1000-1": 1000,
                "-10-100-1": 800,
                "1000-10": 100,
                "00-100": 100,
                "-100-1": 10,
            },
            {
                "00000": 10000000,
                "-10000-1": 100000,
                "-100001": 100000,
                "-1000-1": 10001,
                "-10-100-1": 8001,
                "1000-10": 100000,
                "00-100": 100000,
                "-100-1": 101,
            },
        ],
        [
            {
                "11111": 10000000,
                "-11111-1": 10000,
                "-111110": 1000,
                "-1111-1": 1000,
                "-11-111-1": 800,
                "0111-11": 1000,
                "11-111": 1000,
                "-111-1": 100,
            },
            {
                "11111": 10000000,
                "-11111-1": 100000,
                "-111110": 100000,
                "-1111-1": 10001,
                "-11-111-1": 8001,
                "0111-11": 100000,
                "11-111": 100000,
                "-111-1": 101,
            },
        ],
    ]

    def take_turn(self, board):
        self.timeout = time.time() + turn_length_in_seconds
        depth_limit = 0
        best_move: list = []
        while True:
            current_move = self.alpha_beta(True, -math.inf, math.inf, [board, [], -math.inf], 0, depth_limit)
            if len(current_move) == 0 or len(current_move[1]) == 0:
                break
            best_move = current_move
            print(best_move)
            depth_limit += 1
        formatted_move = [best_move[0], best_move[1][0][0], best_move[1][0][1], best_move[2]]
        return formatted_move

    def alpha_beta(self, maximizing_player, alpha, beta, value, depth, depth_limit):
        if time.time() > self.timeout:
            return []
        if value[0].winning_pattern_exists():
            if value[2] < 0:
                value[2] = -10000000 + depth
            else:
                value[2] = 10000000 - depth
            return value
        if depth > depth_limit:
            return value
        if maximizing_player:
            children = self.get_children(value[0], self.player, value[1], depth)
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
            children = self.get_children(value[0], int(not self.player), value[1], depth)
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

    def get_children(self, board, player, path: list, depth):
        children = []
        safe_children = []
        for pos in board.reduced_open_positions():
            new_path = copy_2d_list(path)
            new_path.append(pos)
            child = [board.copy(), new_path, 0]
            child[0].update_board(player, pos[0], pos[1])
            child[2] = self.get_value(child[0], player)
            if child[0].exists_immediate_win(0) or child[0].exists_immediate_win(1):
                safe_children.append(child)
            elif player == self.player:
                if len(children) < max(self.max_branches - depth * 5, 1):
                    children.append(child)
                    children.sort(key=sort_heuristic)
                elif child[2] > children[0][2]:
                    children.remove(children[0])
                    children.append(child)
                    children.sort(key=sort_heuristic)
            else:
                if len(children) < max(self.max_branches - depth * 5, 1):
                    children.append(child)
                    children.sort(key=sort_heuristic, reverse=True)
                elif child[2] < children[0][2]:
                    children.remove(children[0])
                    children.append(child)
                    children.sort(key=sort_heuristic, reverse=True)
        for child in safe_children:
            children.append(child)
        if depth == 0:
            print(children)
        return children

    def get_value(self, board, player):
        value = 0
        patterns = board.get_patterns()
        for key in self.heuristic_patterns[self.player][0]:
            if player == self.player:
                value += patterns[self.player][key] * self.heuristic_patterns[self.player][0][key]
            else:
                value += patterns[self.player][key] * self.heuristic_patterns[self.player][1][key]
        for key in self.heuristic_patterns[int(not self.player)][0]:
            if player == self.player:
                value -= patterns[int(not self.player)][key] * self.heuristic_patterns[int(not self.player)][1][key]
            else:
                value -= patterns[int(not self.player)][key] * self.heuristic_patterns[int(not self.player)][0][key]
        return value


def sort_heuristic(child: list):
    return child[2]
