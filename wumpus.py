import file_logic as fl
from agent import RandomAgent
from board import Board
import sys

random_agent = RandomAgent(sys.argv[1])
board = Board([[-1] * 15 for _ in range(15)])

initialized = False

while fl.wait_for_file(fl.endFilePath):
    while fl.wait_for_file(fl.goFilePath):
        continue
    moveFile = open(fl.moveFilePath, "r")
    if not initialized:
        initialized = True
        readMove = moveFile.read()
        if len(readMove) > 0:
            random_agent.player = 1
            readGo = fl.interpret_move(readMove, int(not random_agent.player))
            board.update_board(readGo[0], readGo[1], readGo[2])
        else:
            random_agent.player = 0
    else:
        readGo = fl.interpret_move(moveFile.read(), int(not random_agent.player))
        board.update_board(readGo[0], readGo[1], readGo[2])

    move = random_agent.take_turn(board)
    print(move)
    board.update_board(random_agent.player, move[0], move[1])
    moveFile = open(fl.moveFilePath, "w")
    moveFile.write("{0} {1} {2}".format(random_agent.name, fl.convert_num_to_alphabet(move[0]), move[1] + 1))
    moveFile.close()
    while not fl.wait_for_file(fl.goFilePath):
        if not fl.wait_for_file(fl.endFilePath):
            break


