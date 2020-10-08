from pathlib import Path
import sys

global goFilePath, endFilePath, moveFilePath
goFilePath = Path('./{0}.go'.format(sys.argv[1]))
moveFilePath = Path('./move_file')
endFilePath = Path('./end_game')


def wait_for_file(file):
    return not file.is_file()


def interpret_move(move: str, player_num):
    items = move.split(' ')
    new_move = (player_num, convert_alphabet_to_num(items[1]), int(items[2]) - 1)
    return new_move


def convert_num_to_alphabet(num):
    return chr(65 + num)


def convert_alphabet_to_num(char: str):
    return ord(char.upper()) - 65
