import structure as struct
import fltk

# 100 due to image size
DIVISOR = 1
WIDTH_CASE = 100 // DIVISOR
HEIGHT_CASE = 100 // DIVISOR
THICKNESS = 10 // DIVISOR
REDUCE_IMG = .5 / DIVISOR


def draw_back(x: int, y: int) -> None:
    """Draws brackgroud of a room.
        Takes the top-left coordinates of the room.

        You must have the `media` subfolder with the `background.png` file.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.image(x * WIDTH_CASE,
               y * HEIGHT_CASE,
               "./media/background.png",
               largeur=WIDTH_CASE,
               hauteur=HEIGHT_CASE,
               ancrage="nw")


def draw_corner_NW(x: int, y: int) -> None:
    """Draws the top-left corner of the room.

    Use instead the function that draws all 4 corners at once `draw_corners`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x, y,
                   x + WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x + THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_NE(x: int, y: int) -> None:
    """Draws the top-right corner of the room.

    Use instead the function that draws all 4 corners at once `draw_corners`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x, y,
                   x - WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x - THICKNESS,
                   y + HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_SE(x: int, y: int) -> None:
    """Draws the bottom-right corner of the room.

    Use instead the function that draws all 4 corners at once `draw_corners`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x, y,
                   x - WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x - THICKNESS,
                   y - HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corner_SW(x: int, y: int) -> None:
    """Draws the bottom-left corner of the room.

    Use instead the function that draws all 4 corners at once `draw_corners`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x, y,
                   x + WIDTH_CASE / 4,
                   y - THICKNESS,
                   remplissage="Black")
    fltk.rectangle(x, y,
                   x + THICKNESS,
                   y - HEIGHT_CASE / 4,
                   remplissage="Black")


def draw_corners(x: int, y: int) -> None:
    """Draws the 4 corners of the room.
        Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    draw_corner_NW(x, y)
    draw_corner_NE(x + WIDTH_CASE, y)
    draw_corner_SE(x + WIDTH_CASE, y + HEIGHT_CASE)
    draw_corner_SW(x, y + HEIGHT_CASE)


def draw_wall_N(x: int, y: int) -> None:
    """Draws the top wall of the room.

    Use instead the function that draws walls with conditions `draw_walls`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x + WIDTH_CASE / 4,
                   y,
                   x + 3 * WIDTH_CASE / 4,
                   y + THICKNESS,
                   remplissage="Black",
                   tag=f"W({x}{y})N")


def draw_wall_E(x: int, y: int) -> None:
    """Draws the right wall of the room.

    Use instead the function that draws walls with conditions `draw_walls`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x + WIDTH_CASE,
                   y + HEIGHT_CASE / 4,
                   x + WIDTH_CASE - THICKNESS,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag=f"W({x}{y})E")


def draw_wall_S(x: int, y: int) -> None:
    """Draws the bottom wall of the room.

    Use instead the function that draws walls with conditions `draw_walls`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x + WIDTH_CASE / 4,
                   y + HEIGHT_CASE,
                   x + 3 * WIDTH_CASE / 4,
                   y + HEIGHT_CASE - THICKNESS,
                   remplissage="Black",
                   tag=f"W({x}{y})S")


def draw_wall_W(x: int, y: int) -> None:
    """Draws the left wall of the room.

    Use instead the function that draws walls with conditions `draw_walls`.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.rectangle(x,
                   y + HEIGHT_CASE / 4,
                   x + THICKNESS,
                   y + 3 * HEIGHT_CASE / 4,
                   remplissage="Black",
                   tag=f"W({x}{y})W")


def draw_walls(x: int, y: int, walls: tuple[bool, bool, bool, bool]) -> None:
    """Draw the walls of the room from the arg walls,
    that tell you which parts to draw.

    Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
        walls (tuple[bool, bool, bool, bool]): (Top, Right, Bottom, Left)
            False if the room is closed to this direction
    """
    x = x * WIDTH_CASE
    y = y * HEIGHT_CASE
    tab_f = [draw_wall_N,
             draw_wall_E,
             draw_wall_S,
             draw_wall_W]
    for i, elem in enumerate(walls):
        if not elem:
            tab_f[i](x, y)


def erase_walls(x: int, y: int, walls: tuple[bool, bool, bool, bool]) -> None:
    """Erase the walls of the room from the arg walls,
    that tell you which parts to erase.

    Takes the top-left coordinates of the room.

    Args:
       x (int): Initial position (width)
       y (int): Initial position (height)
       walls (tuple[bool, bool, bool, bool]): (Top, Right, Bottom, Left)
            False if the room is closed to this direction
    """
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
    """Draw the entire room (background, walls, corners).

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
        r (struct.Room): Got information about which wall is open
    """
    draw_back(x, y)
    draw_corners(x, y)
    draw_walls(x, y, r.val)


def draw_level(x: int, y: int, lv: int) -> None:
    """Draws the level of the entity at the top right
    of the room.

    Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position of the room(width)
        y (int): Initial position of the room(height)
        lv (int): Level to draw
    """
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
    """Erase the level of the entity at the top right
    of the room.

    Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position of the room(width)
        y (int): Initial position of the room(height)
    """
    fltk.efface(f"LV({x}{y})r")
    fltk.efface(f"LV({x}{y})t")


def draw_entity(x: int, y: int, img: str) -> None:
    """Draws the entity in the middle of the room.

    Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
        img (str): Path to the image
    """
    fltk.image(x * WIDTH_CASE + WIDTH_CASE / 4,
               y * HEIGHT_CASE + HEIGHT_CASE / 4,
               img,
               int(WIDTH_CASE * REDUCE_IMG),
               int(HEIGHT_CASE * REDUCE_IMG),
               ancrage="nw",
               tag=f"E({x}{y})")


def erase_entity(x: int, y: int) -> None:
    """Erase the entity in the middle of the room.

    Takes the top-left coordinates of the room.
    Args:
        x (int): Initial position (width)
        y (int): Initial position (height)
    """
    fltk.efface(f"E({x}{y})")


def draw_adv(adv: struct.Adventurer) -> None:
    """Draws the adventurer.

    Args:
        adv (struct.Adventurer): Adventurer to draw
    """
    draw_entity(adv.x, adv.y, "./media/Knight.png")
    draw_level(adv.x, adv.y, adv.level)


def draw_drags(lst_drags: list[struct.Dragon]) -> None:
    """Draws all dragons.

    Args:
        lst_drags (list[struct.Dragon]): List of dragons to draw
    """
    for elem in lst_drags:
        draw_entity(elem.x, elem.y, "./media/Dragon.png")
        draw_level(elem.x, elem.y, elem.level)


def draw_drag(drag: struct.Dragon) -> None:
    """Draws one dragons.

    Args:
        lst_drags (struct.Dragon): dragonss to draw
    """
    draw_entity(drag.x, drag.y, "./media/Dragon.png")
    draw_level(drag.x, drag.y, drag.level)


def draw_treasure(trea: struct.Treasure) -> None:
    """Draws the treasure.

    Args:
        trea (struct.Treasure): Treasure to draw
    """
    draw_entity(trea.x, trea.y, "./media/treasure.png")


def draw_game(wis: struct.WallIsYou) -> None:
    """Draw all the game from the board to entities

    Args:
        wis (struct.WallIsYou): Class of the game to draw
    """
    for y in range(wis.height):
        for x in range(wis.width):
            draw_room(x, y, wis.board[y][x])
    if wis.adv:
        draw_adv(wis.adv)
    if wis.drags:
        draw_drags(wis.drags)
    if wis.treasure:
        draw_treasure(wis.treasure)


def draw_path(lst_solus: list[tuple[int, int]]) -> None:
    """Draws the path of the adventurer to a dragon or a treasure.

    Args:
        lst_solus (list[tuple[int, int]]): Path use by the adventurer
    """
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
    """Erase the path of the adventurer.

    Args:
        lst_solus (list[tuple[int, int]]): Path use by the adventurer
    """
    for i in range(len(lst_solus) - 1):
        fltk.efface(f"P{i}")


def draw_loose(w_width: int, w_height: int) -> None:
    """Erase the game and draw the defeat screen.

    Args:
        w_width (int): window widht
        w_height (int): window height
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, w_width, w_height,
                   remplissage="black")
    fltk.image(w_width // 2,
               w_height // 2,
               "./media/dead_screen.png")


def draw_victory(w_width: int, w_height: int) -> None:
    """Erase the game and draw the victory screen.

    Args:
        w_width (int): window widht
        w_height (int): window height
    """
    fltk.efface_tout()
    fltk.rectangle(0, 0, w_width, w_height,
                   remplissage="black")
    fltk.image(w_width // 2,
               w_height // 2,
               "./media/victory_screen.png")


def update_level(x: int, y: int, lv: int) -> None:
    """Ereases the old level of the entity and
    draws the new level of the entity at the top right
    of the room.

    Takes the top-left coordinates of the room.

    Args:
        x (int): Initial position of the room(width)
        y (int): Initial position of the room(height)
        lv (int): Level to draw
    """
    erase_level(x, y)
    draw_level(x, y, lv)
