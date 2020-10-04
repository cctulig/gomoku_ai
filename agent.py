import random


class Agent(object):
    def __init__(self, name):
        self.name = name
        self.player = None

    def take_turn(self, board):
        raise NotImplementedError("implement")


class RandomAgent(Agent):
    def take_turn(self, board):
        return random.choice(board.open_positions())

