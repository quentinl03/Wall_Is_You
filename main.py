from pprint import pprint
import sys
import struct
import fltk
import graph
import file

def init_graph(wis: struct.WallIsYou) -> None:
    fltk.cree_fenetre(wis.width * graph.WIDTH_CASE, wis.height * graph.HEIGHT_CASE)
    graph.draw_game(wis)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You have to choose a map")
        exit()
    game = struct.WallIsYou(sys.argv[1])
    file.open_map(game)
    init_graph(game)
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)
    fltk.attend_fermeture()