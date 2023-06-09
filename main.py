from pprint import pprint
import sys
import struct as strc
import file

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You have to choose a map")
        exit()
    game = strc.WallIsYou(sys.argv[1])
    file.open_map(game)
    game.board[1][0].rotate()
    game.board[1][0].rotate()
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)