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
                          [-1, 0, 0, 0, 1], [-1, 0, 0, -1], [-1, 0, 0, 1], [-1, 0, 1]]
    cardinal_directions = [0, .785, 1.571, 2.356, 3.142, 3.927, 4.712, 5.498]

    def __init__(self, board: list, patterns0: dict, patterns1: dict):
        self.board = board
        self.patterns0 = patterns0
        self.patterns1 = patterns1

    def __getitem__(self):
        return self

    def open_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    positions.append((x, y))
        return positions

    def update_board(self, player, x, y):
        self.subtract_patterns(self.find_patterns(player, x, y), player)
        self.board[x][y] = player
        self.add_patterns(self.find_patterns(player, x, y), player)

    def subtract_patterns(self, patterns, player):
        for pattern in patterns:
            key = get_key(pattern)
            if player == 0:
                self.patterns0[key] = self.patterns0[key] - 1
            else:
                self.patterns1[key] = self.patterns1[key] - 1

    def add_patterns(self, patterns, player):
        for pattern in patterns:
            key = [player, get_key(pattern)]
            self.patterns[key] = self.patterns[key] + 1

    def find_patterns(self, player, x, y):
        found_patterns = []
        for index, theta in enumerate(self.cardinal_directions):
            pattern = []
            for radius in range(5):
                pos = [x + round(math.cos(theta)) * radius, y + round(math.sin(theta)) * radius]
                if self.out_of_bounds(pos) or self.opposing_player(pos, player):
                    pattern.append(1)
                    break
                elif self.blank(pos):
                    pattern.append(-1)
                    break
                else:
                    pattern.append(0)
            if index > 3 and pattern[0] == 0:
                pattern.remove(0)
                for value in pattern:
                    found_patterns[index - 4].append(value)
            else:
                found_patterns.append(pattern)
        valid_patterns = []
        for pattern in found_patterns:
            print(pattern)
            if pattern in self.available_patterns:
                print("found valid pattern!")
                valid_patterns.append(pattern)
        return valid_patterns

    def out_of_bounds(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def opposing_player(self, pos, player):
        return self.board[pos[0], pos[1]] == int(not player)

    def blank(self, pos):
        return self.board[pos[0], pos[1]] == -1

    def get_children(self, player):
        children = []
        for pos in self.open_positions():
            child = (copy.deepcopy(self.board), pos[0], pos[1])
            child[0][pos[0]][pos[1]] = player
            children.append(child)
        return children

    def get_patterns(self):
        return [self.patterns0, self.patterns1]
