import copy

class Board(object):
    width = 15
    height = 15
    win_condition = 5
    available_patterns = [[0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, -1], [-1, 0, 0, 0, 0, 1], [-1, 0, 0, 0, -1], [-1, 0, 0, 0, 1], [-1, 0, 0, -1], [-1, 0, 0, 1], [-1, 0, -1], [-1, 0, 1]]

    def __init__(self, board: list, patterns: dict):
        self.board = board
        self.patterns = patterns

    def open_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    positions.append((x, y))
        return positions

    def update_board(self, player, x, y):
        self.board[x][y] = player

    def get_children(self, player):
        children = []
        for pos in self.open_positions():
            child = (copy.deepcopy(self.board), pos[0], pos[1])
            child[0][pos[0]][pos[1]] = player
            children.append(child)
        return children

    def find_patterns(self, player, x, y):
        return

#
# ---011-111--111-- [011, (2) 111]
# ---0110111--111-- [011, 111] (subtract) => [111], [0110, 0111] (add) => [0110, 0111, 111]

# -01 -001 -0001 -00001 -00- -000- -0000-