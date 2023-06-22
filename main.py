from pprint import pprint
import sys
import structure as struct
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

    path = None
    while ev := fltk.attend_ev():
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            break
        if path is not None:
            graph.erase_path(path)
        path = solver.find_path(game)
        # path = solver.find_path_depth(game, game.adv.x, game.adv.y, set())
        if path is not None:
            # path[0].reverse()
            # path = path[0]
            graph.draw_path(path)
        if tev == "ClicGauche" or tev == "ClicDroit":
            x = fltk.abscisse_souris() // (graph.WIDTH_CASE // graph.DIVISOR)
            y = fltk.ordonnee_souris() // (graph.HEIGHT_CASE // graph.DIVISOR)
            if tev == "ClicGauche":
                graph.erase_walls(x, y, game.board[y][x].val)
                game.board[y][x].rotate()
                graph.draw_walls(x, y, game.board[y][x].val)
            elif (tev == "ClicDroit" and
                  not game.board[y][x].got_drag and not game.board[y][x].got_adv):
                if game.board[y][x].got_trea is True:
                    game.treasure = None
                    game.board[y][x].got_trea = False
                    graph.erase_entity(x, y)
                elif game.treasure is None:
                    game.treasure = struct.Treasure(y, x)
                    game.board[y][x].got_trea = True
                    graph.draw_treasure(game.treasure)
        elif tev == "Touche" and fltk.touche(ev) == "space" and path is not None:
            dest_x, dest_y = path[-1]
            if game.defeat(dest_x, dest_y):
                break
            game.play(dest_x, dest_y)
            fltk.efface_tout()
            graph.draw_game(game)

            victory = game.victory()
            if victory:
                break

        if path is not None:
            graph.erase_path(path)
        path = solver.find_path(game)
        # path = solver.find_path_depth(game, game.adv.x, game.adv.y, set())
        if path is not None:
            graph.draw_path(path)
        fltk.mise_a_jour()

        pprint(game.board)
        print(ev, tev, path)

    fin = graph.draw_victory if victory else graph.draw_loose
    fin(game.width * graph.WIDTH_CASE, game.height * graph.HEIGHT_CASE)
    if tev != "Quitte":
        fltk.mise_a_jour()
        fltk.attend_fermeture()
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)
