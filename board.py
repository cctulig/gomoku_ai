import copy

class Board(object):
    width = 15
    height = 15
    win_condition = 5

    def __init__(self, board):
        self.board = board

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
        self.board[x][y] = player

    def get_children(self, player):
        children = []
        for pos in self.open_positions():
            child = (copy.deepcopy(self.board), pos[0], pos[1])
            child[0][pos[0]][pos[1]] = player
            children.append(child)
        return children

