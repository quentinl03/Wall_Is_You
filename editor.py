import structure as struct
import graph
import fltk

def init_from_size(x: int, y: int) -> list[list[struct.Room]]:
    return [[struct.Room("╬") for __ in range(x)]for _ in range(y)]

def levelup_drag(wiy: struct.WallIsYou, x: int, y: int) -> None:
    for elem in wiy.drags:
        if x == elem.x and y == elem.y:
            elem.level += 1
            graph.update_level(x, y, elem.level)
            return

def leveldown_drag(wiy: struct.WallIsYou, x: int, y: int) -> None:
    for elem in wiy.drags:
        if x == elem.x and y == elem.y and elem.level > 1:
            elem.level -= 1
            graph.update_level(x, y, elem.level)
            return
        
def remove_drag(wiy: struct.WallIsYou, x: int, y: int) -> None:
    for elem in wiy.drags:
        if x == elem.x and y == elem.y:
            wiy.drags.remove(elem)
            return

def change_nb_walls_room(x: int, y: int, r: struct.Room):
    graph.erase_walls(x, y, r.val)
    # 1 for add because we want tu add one door
    nb_door = sum(r.val) % 4 + 1
    r.val = tuple(i < nb_door for i in range(4))
    r.c = struct.PIECES_R[r.val]
    graph.draw_walls(x, y, r.val)

def change_rotation_room(x: int, y: int, r: struct.Room):
    graph.erase_walls(x, y, r.val)
    r.rotate()
    graph.draw_walls(x, y, r.val)

def map_editor(wiy: struct.WallIsYou):
    while ev := fltk.attend_ev():
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            break
        x = fltk.abscisse_souris() // (graph.WIDTH_CASE // graph.DIVISOR)
        y = fltk.ordonnee_souris() // (graph.HEIGHT_CASE // graph.DIVISOR)

        if tev == "ClicGauche":
            change_nb_walls_room(x, y, wiy.board[y][x])
        if tev == "ClicDroit":
            change_rotation_room(x, y, wiy.board[y][x])

        elif tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "space":
                break
            # place/remove a dragon
            if touche == "d" and not wiy.board[y][x].got_adv:
                if wiy.board[y][x].got_drag:
                    wiy.board[y][x].got_drag = False
                    graph.erase_entity(x, y)
                    graph.erase_level(x, y)
                    remove_drag(wiy, x, y)
                else :
                    wiy.board[y][x].got_drag = True
                    drag = struct.Dragon(y, x)
                    wiy.drags.append(drag)
                    graph.draw_drag(drag)

            # place/remove the adventurer
            if touche == "a" and not wiy.board[y][x].got_drag:
                if wiy.adv is None:
                    wiy.adv = struct.Adventurer(y, x)
                    wiy.board[y][x].got_adv = True
                    graph.draw_adv(wiy.adv)
                else :
                    wiy.board[wiy.adv.y][wiy.adv.x].got_adv = False
                    graph.erase_level(wiy.adv.x, wiy.adv.y)
                    graph.erase_entity(wiy.adv.x, wiy.adv.y)
                    wiy.board[y][x].got_adv = True
                    wiy.adv.x = x
                    wiy.adv.y = y
            # level up on entity
            if touche == "Up":
                r = wiy.board[y][x]
                if r.got_drag:
                    levelup_drag(wiy, x, y)
                if r.got_adv:
                    wiy.adv.level += 1
                    graph.update_level(x, y, wiy.adv.level)
            
            # level down on entity
            elif touche == "Down":
                r = wiy.board[y][x]
                if r.got_drag:
                    leveldown_drag(wiy, x, y)
                if r.got_adv and wiy.adv.level > 1:
                    wiy.adv.level -= 1
                    graph.update_level(x, y, wiy.adv.level)
        fltk.mise_a_jour()
        
    # print("phase 2")



    # while ev := fltk.attend_ev():
    #     x = fltk.abscisse_souris() // (graph.WIDTH_CASE // graph.DIVISOR)
    #     y = fltk.ordonnee_souris() // (graph.HEIGHT_CASE // graph.DIVISOR)
    #     tev = fltk.type_ev(ev)
    #     print(tev,x,y)
    #     if tev == "Touche" and fltk.touche(ev) == "space":
    #         break


        