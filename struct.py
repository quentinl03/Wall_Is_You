from functools import total_ordering
import colorama
from enum import IntEnum

PIECES = {
    "╨": (True, False, False, False),
    "╞": (False, True, False, False),
    "╥": (False, False, True, False),
    "╡": (False, False, False, True),
    "╚": (True, True, False, False),
    "╔": (False, True, True, False),
    "╗": (False, False, True, True),
    "╝": (True, False, False, True),
    "╠": (True, True, True, False),
    "╦": (False, True, True, True),
    "╣": (True, False, True, True),
    "╩": (True, True, False, True),
    "║": (True, False, True, False),
    "═": (False, True, False, True),
    "╬": (True, True, True, True)
}

PIECES_R = {item: key for key, item in PIECES.items()}

class Dir(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class DocumentError(Exception):
    pass

class EntityError(DocumentError):
    pass

class AdventurerError(EntityError):
    pass

class TreasureError(EntityError):
    pass

class DragonError(EntityError):
    pass

class Room:
    def __init__(self, c: str) -> None:
        self.got_adv = False
        self.got_drag = False
        self.got_trea = False
        self.c = c
        self.val = None
        if c in PIECES.keys(): #.keys non obligatoire
            self.val = PIECES[c]
    
    def __repr__(self) -> str:
        if self.got_adv:
            return f"{colorama.Fore.GREEN}{self.c}{colorama.Style.RESET_ALL}"
        if self.got_drag:
            return f"{colorama.Fore.RED}{self.c}{colorama.Style.RESET_ALL}"
        if self.got_trea:
            return f"{colorama.Fore.YELLOW}{self.c}{colorama.Style.RESET_ALL}"
        return self.c
    
    def rotate(self):
        self.val = (self.val[3], self.val[0], self.val[1], self.val[2])
        self.c = PIECES_R[self.val]

    def is_connected(self, other, dir: Dir) -> bool:
        return ( 
            (dir == Dir.NORTH and self.val[0] is True and other.val[2] is True) or
            (dir == Dir.EAST and self.val[1] is True and other.val[3] is True) or
            (dir == Dir.SOUTH and self.val[2] is True and other.val[0] is True) or
            (dir == Dir.WEST and self.val[3] is True and other.val[1] is True)
        )

@total_ordering
class Entity:
    def __init__(self, y: int, x: int, level: int = 1) -> None:
        if level < 1:
            raise DragonError("Entity level must be positive")
        self.level = level
        if x < 0 or y < 0:
            raise EntityError("Coordinates must be positive")
        self.x = x
        self.y = y

    def __lt__(self,other) -> bool:
        return self.level != -1 and (self.level < other.level or other.level == -1)

    # def __le__(self,other) -> bool:
    #     return self.level <= other.level or other.level == -1
    
    def __eq__(self, other) -> bool:
        return self.level == other.level
    
    # def __ne__(self, other) -> bool:
    #     return self.level != other.level
    
    # def __gt__(self, other) -> bool:
    #     return other.level != -1 and (self.level > other.level or self.level == -1)
    
    # def __ge__(self, other) -> bool:
    #     return self.level == -1 or self.level >= other.level

class Dragon(Entity):
    def __repr__(self) -> str:
        return f"Dragon: lv{self.level} {self.x, self.y}"

class Treasure(Entity):
    def __repr__(self) -> str:
        return f"Treasure: {self.x, self.y}"

class Adventurer(Entity):
    def __repr__(self) -> str:
        return f"Charcater: lv{self.level} {self.x, self.y}"

class WallIsYou:
    def __init__(self, file: str) -> None:
        self.height = 0
        self.width = 0
        self.file = file
        self.board = list()
        self.adv = None
        self.drags = list()
        self.treasure_limit = None
        self.treasure = None

    def is_in_board(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return (
                x1 < 0 or x2 < 0 or 
                y1 < 0 or y2 < 0 or 
                x1 > self.width or x2 > self.width or
                y1 > self.height or y2 > self.height
            )
    
    def is_neighbour(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if self.is_in_board(x1, y1, x2, y2) is False:
            return False
        diff_x = abs(x1 - x2) 
        diff_y = abs(y1 - y2)
        #diff_x + diff_y == 1 to avoid comparing same coord (0,0)(0,0)
        # or coord in corner (1,1) with (0,0) or (0,2) or (2,0) or (2,2)
        return diff_x <= 1 and diff_y <= 1 and diff_x + diff_y == 1
    
    def dir_neighbour(self, x1: int, y1: int, x2: int, y2: int):
        if self.is_neighbour(x1, y1, x2, y2) is False:
            return None
        diff_x = (x1 - x2) 
        diff_y = (y1 - y2)
        if diff_x == 0 and diff_y == -1:
            return Dir.NORTH
        if diff_x == 1 and diff_y == 0:
            return Dir.EAST
        if diff_x == 0 and diff_y == 1:
            return Dir.SOUTH
        if diff_x == -1 and diff_y == 0:
            return Dir.WEST
        print("problems")
        return None