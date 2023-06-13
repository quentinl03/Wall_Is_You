from pprint import pprint
import sys
import struct
import solver
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
    tev = None
    path = None
    while tev != "Quitte":
        if path is not None:
            graph.erase_path(path[0])
        path = solver.find_path_depth(game, game.adv.x, game.adv.y, set())
        if path is not None:
            graph.draw_path(path[0])
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            x = fltk.abscisse_souris() // (graph.WIDTH_CASE // graph.DIVISEUR)
            y = fltk.ordonnee_souris() // (graph.HEIGHT_CASE // graph.DIVISEUR)
            graph.erase_walls(x, y, game.board[y][x].val)
            game.board[y][x].rotate()
            graph.draw_walls(x, y, game.board[y][x].val)
        fltk.mise_a_jour()


    fltk.ferme_fenetre()
    print("end of exec")
    # pprint(game.board)
    # print(game.adv)
    # print(game.drags)
    # print(game.treasure)