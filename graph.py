import structure as struct
import fltk

# 100 due to image size
DIVISOR = 1
WIDTH_CASE = 100 // DIVISOR
HEIGHT_CASE = 100 // DIVISOR
THICKNESS = 10 // DIVISOR
REDUCE_IMG = .5 / DIVISOR


def draw_back(x: int, y: int) -> None:
    fltk.image(x * WIDTH_CASE,
               y * HEIGHT_CASE,
               "./media/fond.png",
               largeur=WIDTH_CASE,
               hauteur=HEIGHT_CASE,
               ancrage="nw")


def draw_corner_NW(x: int, y: int) -> None:
    fltk.rectangle(x, y,
                   x + WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x + THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_NE(x: int, y: int) -> None:
    fltk.rectangle(x, y,
                   x - WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x - THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_SE(x: int, y: int) -> None:
    fltk.rectangle(x, y,
                   x - WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x - THICKNESS,
                   y - HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_SW(x: int, y: int) -> None:
    fltk.rectangle(x, y,
                   x + WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x + THICKNESS,
                   y - HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corners(x: int, y: int) -> None:
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    draw_corner_NW(x, y)
    draw_corner_NE(x + WIDTH_CASE, y)
    draw_corner_SE(x + WIDTH_CASE, y + HEIGHT_CASE)
    draw_corner_SW(x, y + HEIGHT_CASE)


def draw_wall_N(x: int, y: int) -> None:
    fltk.rectangle(x + WIDTH_CASE / 4,
                   y,
                   x + 3 * WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black",
                   tag=f"W({x}{y})N")


def draw_wall_E(x: int, y: int) -> None:
    fltk.rectangle(x + WIDTH_CASE,
                   y + HEIGHT_CASE / 4,
                   x + WIDTH_CASE - THICKNESS,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag=f"W({x}{y})E")


def draw_wall_S(x: int, y: int) -> None:
    fltk.rectangle(x + WIDTH_CASE / 4,
                   y + HEIGHT_CASE,
                   x + 3 * WIDTH_CASE / 4,
                   y + HEIGHT_CASE - THICKNESS,
                   remplissage="Black",
                   tag=f"W({x}{y})S")


def draw_wall_W(x: int, y: int) -> None:
    fltk.rectangle(x,
                   y + HEIGHT_CASE / 4,
                   x + THICKNESS,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag=f"W({x}{y})W")


def draw_walls(x: int, y: int, walls: tuple) -> None:
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    tab_f = [draw_wall_N,
             draw_wall_E,
             draw_wall_S,
             draw_wall_W]
    for i, elem in enumerate(walls):
        if not elem:
            tab_f[i](x, y)


def erase_walls(x: int, y: int, walls: tuple) -> None:
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    for i, elem in enumerate(walls):
        if not elem and i == struct.Dir.NORTH:
            fltk.efface(f"W({x}{y})N")
        elif not elem and i == struct.Dir.EAST:
            fltk.efface(f"W({x}{y})E")
        elif not elem and i == struct.Dir.SOUTH:
            fltk.efface(f"W({x}{y})S")
        elif not elem and i == struct.Dir.WEST:
            fltk.efface(f"W({x}{y})W")


def draw_room(x: int, y: int, r: struct.Room) -> None:
    draw_back(x, y)
    draw_corners(x, y)
    draw_walls(x, y, r.val)


def draw_level(x: int, y: int, lv: int) -> None:
    start_x = x * WIDTH_CASE + 2 * WIDTH_CASE / 3
    start_y = y * HEIGHT_CASE + 2 * THICKNESS

    tx, ty = fltk.taille_texte(str(lv), taille=12)

    fltk.rectangle(start_x, start_y,
                   start_x + tx,
                   start_y + ty,
                   remplissage="White",
                   tag=f"LV({x}{y})r")
    fltk.texte(start_x, start_y,
               str(lv), taille=12,
               tag=f"LV({x}{y})t")


def erase_level(x: int, y: int) -> None:
    fltk.efface(f"LV({x}{y})r")
    fltk.efface(f"LV({x}{y})t")


def draw_entity(x: int, y: int, img: str) -> None:
    fltk.image(x * WIDTH_CASE + WIDTH_CASE / 4,
               y * HEIGHT_CASE + HEIGHT_CASE / 4,
               img,
               int(WIDTH_CASE * REDUCE_IMG),
               int(HEIGHT_CASE * REDUCE_IMG),
               ancrage="nw",
               tag=f"E({x}{y})")


def erase_entity(x: int, y: int) -> None:
    fltk.efface(f"E({x}{y})")


def draw_adv(adv: struct.Adventurer) -> None:
    draw_entity(adv.x, adv.y, "./media/Knight_s_resized.png")
    draw_level(adv.x, adv.y, adv.level)


def draw_drags(lst_drags: list[struct.Dragon]) -> None:
    for elem in lst_drags:
        draw_entity(elem.x, elem.y, "./media/Dragon_s.png")
        draw_level(elem.x, elem.y, elem.level)


def draw_treasure(trea: struct.Treasure) -> None:
    draw_entity(trea.x, trea.y, "./media/treasure_resized.png")


def draw_game(wis: struct.WallIsYou) -> None:
    for y in range(wis.height):
        for x in range(wis.width):
            draw_room(x, y, wis.board[y][x])
    draw_adv(wis.adv)
    draw_drags(wis.drags)
    if wis.treasure:
        draw_treasure(wis.treasure)


def draw_path(lst_solus: list[tuple[int, int]]) -> None:
    start_x = WIDTH_CASE / 2
    start_y = HEIGHT_CASE / 2
    for i in range(len(lst_solus) - 1):
        x1, y1 = lst_solus[i]
        x2, y2 = lst_solus[i + 1]
        fltk.ligne(start_x + x1 * WIDTH_CASE,
                   start_y + y1 * HEIGHT_CASE,
                   start_x + x2 * WIDTH_CASE,
                   start_y + y2 * HEIGHT_CASE,
                   couleur="red",
                   epaisseur=3,
                   tag=f"P{i}")


def erase_path(lst_solus: list[tuple[int, int]]) -> None:
    for i in range(len(lst_solus) - 1):
        fltk.efface(f"P{i}")


def draw_loose(w_width: int, w_height: int) -> None:
    fltk.efface_tout()
    fltk.rectangle(0, 0, w_width, w_height,
                   remplissage="black")
    fltk.image(w_width // 2,
               w_height // 2,
               "./media/dead_screen.png")


def draw_victory(w_width: int, w_height: int) -> None:
    fltk.efface_tout()
    fltk.rectangle(0, 0, w_width, w_height,
                   remplissage="black")
    fltk.image(w_width // 2,
               w_height // 2,
               "./media/victory_screen.png")
