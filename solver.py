import structure as struct
from typing import Optional
from collections import deque


def find_path_depth(wis: struct.WallIsYou, x: int, y: int, path: set
                    ) -> Optional[tuple[list[tuple[int, int]], int]]:

    # return dragon coordinates and his level
    if wis.board[y][x].got_drag:
        lv = wis.level_drag(x, y)
        if lv == 0:
            raise (ValueError("Dragon not found but should have been"))
        return [(x, y)], lv

    # if already visited end here to avoid infinite loop
    if (x, y) in path:
        return None

    path.add((x, y))
    r = wis.board[y][x]

    # Testing if 4 rooms next to us are connected
    lst_res = [None, None, None, None]
    dirs = [(x, y - 1, struct.Dir.NORTH), (x + 1, y, struct.Dir.EAST),
            (x, y + 1, struct.Dir.SOUTH), (x - 1, y, struct.Dir.WEST)]
    for i, (nx, ny, dir) in enumerate(dirs):
        if wis.is_in_board(nx, ny) and r.is_connected(wis.board[ny][nx], dir):
            lst_res[i] = find_path_depth(wis, nx, ny, path)

    # get the maximum value
    maxi = 0
    maxi_e = None
    for elem in lst_res:
        if elem is not None and maxi < elem[1]:
            maxi_e, maxi = elem

    if maxi_e is None:
        return None
    return maxi_e + [(x, y)], maxi


def find_path_breadth(wis: struct.WallIsYou, dest_x, dest_y) -> Optional[list[tuple[int, int]]]:
    closed = set()

    to_do = deque()
    to_do.append(((wis.adv.x, wis.adv.y), [(wis.adv.x, wis.adv.y)]))
    while to_do:

        (x, y), path = to_do.popleft()
        if x == dest_x and y == dest_y:
            return path

        r = wis.board[y][x]

        dirs = [(x, y - 1, struct.Dir.NORTH), (x + 1, y, struct.Dir.EAST),
                (x, y + 1, struct.Dir.SOUTH), (x - 1, y, struct.Dir.WEST)]
        for nx, ny, dir in dirs:
            if (wis.is_in_board(nx, ny) and (nx, ny) not in closed and
               r.is_connected(wis.board[ny][nx], dir)):

                if not wis.board[ny][nx].got_drag or nx == dest_x and ny == dest_y:
                    to_do.append(((nx, ny), path + [(nx, ny)]))

        closed.add((x, y))

    return


def find_path(wis: struct.WallIsYou) -> Optional[list[tuple[int, int]]]:
    if wis.treasure is not None:
        solv = find_path_breadth(wis, wis.trea.x, wis.trea.y)
        if solv is not None:
            return solv

    drags = sorted(wis.drags, reverse=True)
    for elem in drags:
        solv = find_path_breadth(wis, elem.x, elem.y)
        if solv is not None:
            return solv
