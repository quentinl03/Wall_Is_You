import structure as struct
from typing import Optional
from collections import deque


def find_path_depth(wis: struct.WallIsYou, x: int, y: int, path: set
                    ) -> Optional[tuple[list[tuple[int, int]], int]]:

    # return dragon coordinates and his level
    if wis.board[y][x].got_drag is True:
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
    if wis.is_in_board(x, y - 1):
        if r.is_connected(wis.board[y - 1][x], struct.Dir.NORTH):
            lst_res[0] = find_path_depth(wis, x, y - 1, path)

    if wis.is_in_board(x + 1, y):
        if r.is_connected(wis.board[y][x + 1], struct.Dir.EAST):
            lst_res[1] = find_path_depth(wis, x + 1, y, path)

    if wis.is_in_board(x, y + 1):
        if r.is_connected(wis.board[y + 1][x], struct.Dir.SOUTH):
            lst_res[2] = find_path_depth(wis, x, y + 1, path)

    if wis.is_in_board(x - 1, y):
        if r.is_connected(wis.board[y][x - 1], struct.Dir.WEST):
            lst_res[3] = find_path_depth(wis, x - 1, y, path)

    # get the maximum value
    maxi = 0
    maxi_e = None
    for elem in lst_res:
        if elem is not None and maxi < elem[1]:
            maxi_e, maxi = elem

    if maxi_e is None:
        return None
    return maxi_e + [(x, y)], maxi


def find_path_breadth(wis: struct.WallIsYou, dest_x, dest_y) -> list[tuple[int, int]]:
    closed = set()

    to_do = deque()
    to_do.append(((wis.adv.x, wis.adv.y), [(wis.adv.x, wis.adv.y)]))
    while to_do:

        (x, y), path = to_do.popleft()
        if x == dest_x and y == dest_y:
            return path
        
        r = wis.board[y][x]


        dirs = [(x, y - 1, struct.Dir.NORTH), (x + 1, y, struct.Dir.EAST), (x, y + 1, struct.Dir.SOUTH), (x - 1, y, struct.Dir.WEST)]
        for nx, ny, dir in dirs:

            if wis.is_in_board(nx, ny) and r.is_connected(wis.board[ny][nx], dir) and (nx, ny) not in closed:
                if not wis.board[ny][nx].got_drag or nx == dest_x and ny == dest_y:
                    to_do.append(((nx, ny), path + [(nx, ny)]))

        closed.add((x, y))

    return


def find_path(wis):
    if wis.treasure is not None:
        solv = find_path_breadth(wis, wis.trea.x, wis.trea.y)
        if solv is not None:
            return solv
    
    drags = sorted(wis.drags, reverse=True)
    for elem in drags:
        solv = find_path_breadth(wis, elem.x, elem.y)
        if solv is not None:
            return solv