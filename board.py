import copy
import math


def get_key(lst):
    string = ''
    for item in lst:
        string += str(item)
    return string


class Board(object):
    width = 15
    height = 15
    win_condition = 5
    available_patterns = [[0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 1], [-1, 0, 0, 0, -1],
                          [-1, 0, 0, 0, 1], [-1, 0, 0, -1], [-1, 0, 0, 1], [-1, 0, 1], [1, 1, 1, 1, 1],
                          [-1, 1, 1, 1, 1, -1], [-1, 1, 1, 1, 1, 0], [-1, 1, 1, 1, -1],
                          [-1, 1, 1, 1, 0], [-1, 1, 1, -1], [-1, 1, 1, 0], [-1, 1, 0]]
    cardinal_directions = [0, .785, 1.571, 2.356, 3.142, 3.927, 4.712, 5.498]

    def __init__(self, board: list, open_positions: list, patterns0: dict, patterns1: dict):
        self.board = board
        self.patterns0 = patterns0
        self.patterns1 = patterns1
        self.open_positions = open_positions

    def __getitem__(self):
        return self

    def all_open_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    positions.append((x, y))
        return positions

    def reduced_open_positions(self):
        return self.open_positions

    def update_board(self, player, x, y):
        self.subtract_patterns(self.find_patterns(player, x, y))
        self.subtract_patterns(self.find_patterns(int(not player), x, y))
        self.board[x][y] = player
        self.update_open_positions([x, y])
        self.add_patterns(self.find_patterns(player, x, y))
        self.add_patterns(self.find_patterns(int(not player), x, y))

    def subtract_patterns(self, patterns):
        for pattern in patterns:
            key = get_key(pattern)
            if self.get_pattern_player(pattern) == 0:
                self.patterns0[key] -= 1
            else:
                self.patterns1[key] -= 1

    def add_patterns(self, patterns):
        for pattern in patterns:
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

    def find_patterns(self, player, x, y):
        found_patterns = []
        for index, theta in enumerate(self.cardinal_directions):
            pattern = [self.board[x][y]]
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
        return self.board[pos[0]][pos[1]] == int(not player)

    def blank(self, pos):
        return self.board[pos[0]][pos[1]] == -1

    def get_children(self, player):
        children = []
        for pos in self.open_positions():
            child = (copy.deepcopy(self.board), pos[0], pos[1])
            child[0][pos[0]][pos[1]] = player
            children.append(child)
        return children

    def get_patterns(self):
        return [self.patterns0, self.patterns1]

    def get_pattern_player(self, pattern):
        return pattern[round((len(pattern)-1)/2)]

    def winning_pattern_exists(self):
        return self.patterns0['00000'] > 0 or self.patterns1['11111'] > 0

    def exists_four_in_row_one_side_blocked(self):
        return self.patterns0['-100001'] > 0 or self.patterns1['-111110'] > 0

    def exists_strategic_pattern(self):
        return self.patterns0['-100001'] > 0 or self.patterns1['-111110'] > 0 or self.patterns0['-10000-1'] > 0 or self.patterns1['-11111-1'] > 0 or self.patterns0['-1000-1'] > 0 or self.patterns1['-1111-1'] > 0

