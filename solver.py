import struct

def find_path_depth(wis: struct.WallIsYou, x: int, y: int, path: set):
    if wis.board[y][x].got_drag is True:
        lv = wis.level_drag(x, y)
        if lv == 0:
            raise(ValueError("Un dragon n'as pas été touver dans la case alors qu'il doit en avoir un"))
        return [(x, y)], lv
    
    if (x,y) in path:
        return None
    
    path.add((x,y))
    r = wis.board[y][x]

    lst_res = [None, None, None, None]
    for elem in struct.Dir:
        if elem == struct.Dir.NORTH and wis.is_in_board(x, y - 1):
            if r.is_connected(wis.board[y - 1][x], struct.Dir.NORTH):
                lst_res[elem.value] = find_path_depth(wis, x, y - 1, path)
        
        elif elem == struct.Dir.EAST and wis.is_in_board(x + 1, y):
            if r.is_connected(wis.board[y][x + 1], struct.Dir.EAST):
                lst_res[elem.value] = find_path_depth(wis, x + 1, y, path)
        
        elif elem == struct.Dir.SOUTH and wis.is_in_board(x, y + 1):
            if r.is_connected(wis.board[y + 1][x], struct.Dir.SOUTH):
                lst_res[elem.value] = find_path_depth(wis, x, y + 1, path)
        
        elif elem == struct.Dir.WEST and wis.is_in_board(x - 1, y):
            if r.is_connected(wis.board[y][x - 1], struct.Dir.WEST):
                lst_res[elem.value] = find_path_depth(wis, x - 1, y, path)
    maxi = 0
    maxi_e = None
    for elem in lst_res:
        if elem is not None and maxi < elem[1]:
            maxi_e, maxi = elem
    
    if maxi_e is None:
        return None
    return maxi_e + [(x,y)], maxi

    
    
# import struct

# def find_path_depth(wis: struct.WallIsYou, x: int, y: int, path: set):
#     print(x,y)
#     if wis.board[y][x].got_drag is True:
#         lv = wis.level_drag(x, y)
#         if lv == 0:
#             raise(ValueError("Un dragon n'as pas été touver dans la case alors qu'il doit en avoir un"))
#         return [(x, y)], lv
    
#     if (x,y) in path:
#         return None
    
#     path.add((x,y))
#     r = wis.board[y][x]

#     lst_res = [None, None, None, None]
#     for elem in struct.Dir:
#         if elem == struct.Dir.NORTH and wis.is_in_board(x, y - 1):
#             if r.is_connected(wis.board[y - 1][x], struct.Dir.NORTH):
#                 lst_res[elem.value] = find_path_depth(wis, x, y - 1, path)
        
#         elif elem == struct.Dir.EAST and wis.is_in_board(x + 1, y):
#             if r.is_connected(wis.board[y][x + 1], struct.Dir.EAST):
#                 lst_res[elem.value] = find_path_depth(wis, x + 1, y, path)
        
#         elif elem == struct.Dir.SOUTH and wis.is_in_board(x, y + 1):
#             if r.is_connected(wis.board[y + 1][x], struct.Dir.SOUTH):
#                 lst_res[elem.value] = find_path_depth(wis, x, y + 1, path)
        
#         elif elem == struct.Dir.WEST and wis.is_in_board(x - 1, y):
#             if r.is_connected(wis.board[y][x - 1], struct.Dir.WEST):
#                 lst_res[elem.value] = find_path_depth(wis, x - 1, y, path)
#     print(lst_res)
#     maxi = 0
#     maxi_e = None
#     for elem in lst_res:
#         if elem is not None and maxi < elem[1]:
#             maxi_e, maxi = elem
    
#     if maxi_e is None:
#         return None
#     return maxi_e + [(x,y)], maxi
