import struct
import fltk
from enum import IntEnum

class Dir(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

#100 est la taille des images
DIVISEUR = 1
WIDTH_CASE = 100 // DIVISEUR
HEIGHT_CASE = 100 // DIVISEUR
THICKNESS = 10 // DIVISEUR
REDUCE_IMG = .5 / DIVISEUR

def draw_back(x: int, y: int) -> None:
    fltk.image(x * WIDTH_CASE,
               y * HEIGHT_CASE,
               "./media/fond.png",
               largeur = WIDTH_CASE,
               hauteur = HEIGHT_CASE,
               ancrage="nw")

def draw_corner_NW(x: int, y: int) -> None:
    fltk.rectangle(x , y,
                   x + WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x , y,
                   x + THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")
    
def draw_corner_NE(x: int, y: int) -> None:
    fltk.rectangle(x , y,
                   x - WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x , y,
                   x - THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")

def draw_corner_SE(x: int, y: int) -> None:
    fltk.rectangle(x , y,
                   x - WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x , y,
                   x - THICKNESS,
                   y - HEIGHT_CASE / 4,
                   remplissage="Black")

def draw_corner_SW(x: int, y: int) -> None:
    fltk.rectangle(x , y,
                   x + WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x , y,
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
                   remplissage = "Black",
                   tag = f"W({x}{y})N"
                   )

def draw_wall_E(x: int, y: int) -> None:
    fltk.rectangle(x + WIDTH_CASE,
                   y + HEIGHT_CASE / 4,
                   x + WIDTH_CASE - THICKNESS,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag = f"W({x}{y})E"
                   )

def draw_wall_S(x: int, y: int) -> None:
    fltk.rectangle(x + WIDTH_CASE / 4,
                   y + HEIGHT_CASE,
                   x + 3 * WIDTH_CASE / 4 ,
                   y + HEIGHT_CASE - THICKNESS,
                   remplissage="Black",
                   tag = f"W({x}{y})S"
                   )

def draw_wall_W(x: int, y: int) -> None:
    fltk.rectangle(x,
                   y + HEIGHT_CASE / 4,
                   x + THICKNESS ,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag = f"W({x}{y})W"
                   )

def draw_walls(x: int, y: int, walls: tuple) -> None:
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    tab_f = [draw_wall_N,
            draw_wall_E,
            draw_wall_S,
            draw_wall_W
    ]
    for i, elem in enumerate(walls):
        if elem is False:
            tab_f[i](x, y)

def erase_walls(x: int, y: int, walls: tuple):
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    for i, elem in enumerate(walls):
        if elem is False and i == Dir.NORTH:
            fltk.efface(f"W({x}{y})N")
        elif elem is False and i == Dir.EAST:
            fltk.efface(f"W({x}{y})E")
        elif elem is False and i == Dir.SOUTH:
            fltk.efface(f"W({x}{y})S")
        elif elem is False and i == Dir.WEST :
            fltk.efface(f"W({x}{y})W")

def draw_room(x: int, y: int, r: struct.Room) -> None:
    draw_back(x, y)
    draw_corners(x, y)
    draw_walls(x, y, r.val)

def draw_level(x: int, y: int, lv: int):
    start_x = x * WIDTH_CASE + 2 * WIDTH_CASE / 3
    start_y = y * HEIGHT_CASE + 2 * THICKNESS
    # (lv // 10 + 1) pour gerer les levels a plusieurs chiffres
    fltk.rectangle(start_x, start_y,
                start_x + THICKNESS * (lv // 10 + 1),
                start_y + 2 * THICKNESS,
                remplissage="White")
    fltk.texte(start_x, start_y,
               str(lv), taille=12)

def draw_entity(x: int, y: int, img: str) -> None:
    fltk.image(x * WIDTH_CASE + WIDTH_CASE / 4,
               y * HEIGHT_CASE + HEIGHT_CASE / 4,
               img,
               int(WIDTH_CASE * REDUCE_IMG),
               int(HEIGHT_CASE * REDUCE_IMG),
               ancrage="nw")

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