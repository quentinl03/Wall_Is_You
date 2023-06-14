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
    victory = False
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
            graph.erase_path(path)
        path = solver.find_path_depth(game, game.adv.x, game.adv.y, set())
        if path is not None:
            graph.draw_path(path[0])
            path = path[0]
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            x = fltk.abscisse_souris() // (graph.WIDTH_CASE // graph.DIVISOR)
            y = fltk.ordonnee_souris() // (graph.HEIGHT_CASE // graph.DIVISOR)
            graph.erase_walls(x, y, game.board[y][x].val)
            game.board[y][x].rotate()
            graph.draw_walls(x, y, game.board[y][x].val)
        if tev == "Touche" and fltk.touche(ev) == "space" and path is not None:
            dest_x, dest_y = path[0]
            if game.defeat(dest_x, dest_y) is True:
                break
            game.play(dest_x, dest_y)
            fltk.efface_tout()
            graph.draw_game(game)

            if game.victory() is True:
                victory = True
                break
        fltk.mise_a_jour()

    if victory is True :
        graph.draw_victory(game.width * graph.WIDTH_CASE, game.height * graph.HEIGHT_CASE)
    else :
        graph.draw_loose(game.width * graph.WIDTH_CASE, game.height * graph.HEIGHT_CASE)
    fltk.mise_a_jour()
    fltk.attend_fermeture()
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)