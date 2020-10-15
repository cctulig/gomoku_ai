import copy
import math
import numpy as np

from copier import copy_2d_list, copy_dict, clone_list, copy_list


def get_key(lst):
    string = ''
    for item in lst:
        string += str(item)
    return string


class Board(object):
    width = 15
    height = 15
    win_condition = 5
    available_patterns = [[0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 1], [-1, 0, 0, 0, -1], [0, 0, -1, 0, 0], [1, 0, 0, 0, -1, 0], [-1, 0, -1, 0, 0, -1], [-1, 0, 0, -1],
                          [1, 1, 1, 1, 1], [-1, 1, 1, 1, 1, -1], [-1, 1, 1, 1, 1, 0], [-1, 1, 1, 1, -1], [1, 1, -1, 1, 1], [0, 1, 1, 1, -1, 1], [-1, 1, -1, 1, 1, -1], [-1, 1, 1, -1]]
    cardinal_directions = [0, .785, 1.571, 2.356, 3.142, 3.927, 4.712, 5.498]

    def __init__(self, board: list, open_positions: list, patterns0: dict, patterns1: dict):
        self.board = board
        self.patterns0 = patterns0
        self.patterns1 = patterns1
        self.open_positions = open_positions

    def __getitem__(self):
        return self

    def copy(self):
        return Board(copy_list(self.board), copy_2d_list(self.open_positions), copy_dict(self.patterns0), copy_dict(self.patterns1))

    def all_open_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x + 15 * y] == -1:
                    positions.append((x, y))
        return positions

    def reduced_open_positions(self):
        return self.open_positions

    def update_board(self, player, x, y):
        # self.subtract_patterns(self.find_patterns(player, x, y))
        # self.subtract_patterns(self.find_patterns(int(not player), x, y))
        self.board[x + 15 * y] = player
        self.update_open_positions([x, y])
        self.find_patterns2(player, x, y)
        # self.add_patterns(self.find_patterns(player, x, y))
        # self.add_patterns(self.find_patterns(int(not player), x, y))

    def subtract_patterns(self, patterns):
        for pattern in patterns:
            self.subtract_pattern(pattern)

    def subtract_pattern(self, pattern):
        key = get_key(pattern)
        if self.get_pattern_player(pattern) == 0:
            self.patterns0[key] -= 1
        else:
            self.patterns1[key] -= 1

    def add_patterns(self, patterns):
        for pattern in patterns:
            self.add_pattern(pattern)

    def add_pattern(self, pattern):
        key = get_key(pattern)
        if self.get_pattern_player(pattern) == 0:
            self.patterns0[key] += 1
        else:
            self.patterns1[key] += 1

    def update_open_positions(self, pos):
        if pos in self.open_positions:
            self.open_positions.remove(pos)
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_pos = [pos[0] + x, pos[1] + y]
                if not self.out_of_bounds(new_pos) and self.blank(new_pos) and new_pos not in self.open_positions:
                    self.open_positions.append(new_pos)

    def find_patterns2(self, player, x, y):
        cardinal_patterns = []
        for index, theta in enumerate(self.cardinal_directions):
            pattern = [-1]
            for radius in range(1, 6):
                pos = [x + round(math.cos(theta)) * radius, y + round(math.sin(theta)) * radius]
                if not self.out_of_bounds(pos):
                    pattern.append(self.board[pos[0] + 15 * pos[1]])
            sub_patterns = self.pass_template_over_pattern(pattern)
            for sub_pattern in sub_patterns:
                self.subtract_pattern(sub_pattern)
            pattern.remove(-1)
            pattern.insert(0, player)
            if index > 3:
                pattern.remove(player)
                for value in pattern:
                    cardinal_patterns[index - 4].insert(0, value)
            else:
                cardinal_patterns.append(pattern)
        for pattern in cardinal_patterns:
            add_patterns = self.pass_template_over_pattern(pattern)
            for add_pattern in add_patterns:
                self.add_pattern(add_pattern)

    def pass_template_over_pattern(self, pattern):
        found_patterns = []
        for template in self.available_patterns:
            start_range = max(len(pattern) - len(template), 0)
            for start_pos in range(start_range):
                sub_pattern = pattern[start_pos:(start_pos + len(template))]
                if template == sub_pattern:
                    found_patterns.append(sub_pattern)
                else:
                    sub_pattern.reverse()
                    if template == sub_pattern:
                        found_patterns.append(sub_pattern)
        return found_patterns

    def trim_pattern(self, pattern: list, player):
        length = len(pattern)
        for i in range(0, length):
            done = True
            if len(pattern) >= 2 and pattern[1] != player:
                pattern.pop(0)
                done = False
            if len(pattern) >= 2 and pattern[-2] != player:
                pattern.pop(-1)
                done = False
            if done:
                return pattern

    def add_valid_pattern(self, pattern):
        if pattern in self.available_patterns:
            self.add_pattern(pattern)
        else:
            pattern.reverse()
            if pattern in self.available_patterns:
                self.add_pattern(pattern)

    def sub_valid_pattern(self, pattern):
        if pattern in self.available_patterns:
            self.subtract_pattern(pattern)
        else:
            pattern.reverse()
            if pattern in self.available_patterns:
                self.subtract_pattern(pattern)

    def find_patterns(self, player, x, y):
        found_patterns = []
        for index, theta in enumerate(self.cardinal_directions):
            pattern = [self.board[x + 15 * y]]
            for radius in range(1, 6):
                pos = [x + round(math.cos(theta)) * radius, y + round(math.sin(theta)) * radius]
                if self.out_of_bounds(pos) or self.opposing_player(pos, player):
                    pattern.append(int(not player))
                    break
                elif self.blank(pos):
                    pattern.append(-1)
                    break
                else:
                    pattern.append(player)
            if index > 3 and pattern[0] == player:
                pattern.remove(player)
                for value in pattern:
                    found_patterns[index - 4].insert(0, value)
                    if len(found_patterns[index - 4]) >= 7:
                        found_patterns[index - 4] = [player, player, player, player, player]
            else:
                found_patterns.append(pattern)
        valid_patterns = []
        for pattern in found_patterns:
            if pattern in self.available_patterns:
                valid_patterns.append(pattern)
            else:
                pattern.reverse()
                if pattern in self.available_patterns:
                    valid_patterns.append(pattern)
        return valid_patterns

    def out_of_bounds(self, pos):
        return not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height)

    def opposing_player(self, pos, player):
        return self.board[pos[0] + 15 * pos[1]] == int(not player)

    def blank(self, pos):
        if 224 < pos[0] + 15 * pos[1] < 0:
            print('({0},{1}) = {2}'.format(pos[0], pos[1], pos[0] + 15 * pos[1]))
        return self.board[pos[0] + 15 * pos[1]] == -1

    def get_patterns(self):
        return [self.patterns0, self.patterns1]

    def get_pattern_player(self, pattern):
        if pattern.count(0) > pattern.count(1):
            return 0
        return 1

    def winning_pattern_exists(self):
        return self.patterns0['00000'] > 0 or self.patterns1['11111'] > 0

    def exists_immediate_win(self, player):
        if player == 0:
            return self.patterns0['-100001'] > 0 or self.patterns0['1000-10'] > 0 or self.patterns0['00-100'] > 0 or self.patterns0['-100001'] or self.patterns0['-10-100-1']
        return self.patterns1['-111110'] > 0 or self.patterns1['0111-11'] > 0 or self.patterns1['11-111'] > 0 or self.patterns1['-1111-1'] or self.patterns1['-11-111-1']

    def exists_strategic_pattern(self):
        return self.patterns0['-100001'] > 0 or self.patterns1['-111110'] > 0 or self.patterns0['-10000-1'] > 0 or self.patterns1['-11111-1'] > 0 or self.patterns0['-1000-1'] > 0 or self.patterns1['-1111-1'] > 0

