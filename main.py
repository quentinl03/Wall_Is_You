import argparse
import structure as struct
import solver
import fltk
import graph
import file
import editor


def init_graph(wis: struct.WallIsYou) -> None:
    fltk.cree_fenetre(wis.width * graph.WIDTH_CASE, wis.height * graph.HEIGHT_CASE)
    graph.draw_game(wis)


def parser() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("map",
                        help="Path to file to open/write")
    parser.add_argument("-e", "--editor", nargs=2, type=int,
                        help="2 positionals arguments (x, y) \
                            This option allows you to create your map, \
                            this map will be save at the path give in argument. \
                            You can play you're map instantly after creating it.\
                            /!\\ You can create impossible map /!\\")
    return vars(parser.parse_args())


if __name__ == "__main__":
    victory = False
    pars = parser()
    game = struct.WallIsYou(pars["map"])
    if pars["editor"] is None:
        file.open_map(game)
        init_graph(game)
    else:
        game.width = pars["editor"][0]
        game.height = pars["editor"][1]
        game.board = editor.init_from_size(game.width, game.height)
        init_graph(game)
        playable = editor.map_editor(game)
        if not playable:
            quit()

    path = solver.find_path(game)
    if path is not None:
        graph.draw_path(path)
    while ev := fltk.attend_ev():
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            break

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
        elif tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "space" and path is not None:
                dest_x, dest_y = path[-1]
                if game.defeat(dest_x, dest_y):
                    break
                game.play(dest_x, dest_y)
                fltk.efface_tout()
                graph.draw_game(game)

                victory = game.victory()
                if victory:
                    break
            elif touche == "s":
                file.save(game, True)

        if path is not None:
            graph.erase_path(path)
        path = solver.find_path(game)
        # path = solver.find_path_depth(game, game.adv.x, game.adv.y, set())
        if path is not None:
            graph.draw_path(path)
        fltk.mise_a_jour()

    fin = graph.draw_victory if victory else graph.draw_loose
    fin(game.width * graph.WIDTH_CASE, game.height * graph.HEIGHT_CASE)
    if tev != "Quitte":
        fltk.mise_a_jour()
        fltk.attend_fermeture()
