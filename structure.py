from functools import total_ordering
import colorama as clrm
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
        if c in PIECES.keys():  # .keys not obligatory
            self.val = PIECES[c]

    def __repr__(self) -> str:
        if self.got_adv:
            return f"{clrm.Fore.GREEN}{self.c}{clrm.Style.RESET_ALL}"
        if self.got_drag:
            return f"{clrm.Fore.RED}{self.c}{clrm.Style.RESET_ALL}"
        if self.got_trea:
            return f"{clrm.Fore.YELLOW}{self.c}{clrm.Style.RESET_ALL}"
        return self.c

    def rotate(self) -> None:
        self.val = (self.val[3], self.val[0], self.val[1], self.val[2])
        self.c = PIECES_R[self.val]

    def is_connected(self, other, d: Dir) -> bool:
        return (
            (d == Dir.NORTH and self.val[0] is True
             and other.val[2] is True) or

            (d == Dir.EAST and self.val[1] is True
             and other.val[3] is True) or

            (d == Dir.SOUTH and self.val[2] is True
             and other.val[0] is True) or

            (d == Dir.WEST and self.val[3] is True
             and other.val[1] is True)
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

    def __lt__(self, other) -> bool:
        return self.level < other.level

    def __eq__(self, other) -> bool:
        return self.level == other.level


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

    def level_drag(self, x: int, y: int) -> int:
        for elem in self.drags:
            if x == elem.x and y == elem.y:
                return elem.level
        return 0

    def is_in_board(self, x: int, y: int) -> bool:
        return not (
            x < 0 or y < 0 or
            x >= self.width or
            y >= self.height)

    def victory(self) -> bool:
        return len(self.drags) == 0

    def defeat(self, x: int, y: int) -> bool:
        lv_drag = self.level_drag(x, y)
        if (self.is_in_board(x, y) is False or
            self.board[y][x].got_drag is False or
                lv_drag == 0):
            return False
        return self.adv.level < lv_drag

    def play(self, dest_x: int, dest_y: int):
        """
        You have to check loose before
        """
        if (self.is_in_board(dest_x, dest_y) is False or
                self.level_drag(dest_x, dest_y) == 0):
            return

        self.board[self.adv.y][self.adv.x].got_adv = False

        self.board[dest_y][dest_x].got_adv = True
        self.board[dest_y][dest_x].got_drag = False
        self.board[dest_y][dest_x].got_trea = False
        self.adv.x = dest_x
        self.adv.y = dest_y
        self.adv.level += 1

        for elem in self.drags:
            if elem.x == dest_x and elem.y == dest_y:
                self.drags.remove(elem)
