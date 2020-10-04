class Board(object):
    width = 15
    height = 15
    win_condition = 5

    def __init__(self):
        self.board = [[-1] * self.width for _ in range(self.height)]

    def open_positions(self):
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    positions.append((x, y))
        return positions

    def update_board(self, player, x, y):
        self.board[x][y] = player
