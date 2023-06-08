import sys
from functools import total_ordering
from pprint import pprint
import colorama

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
        self.c = [k for k, v in PIECES.items() if v == self.val][0]
        # si definitif passer au reverse dico car 0(1) (act O(n))

@total_ordering
class Entity:
    def __init__(self, level: int, x: int, y: int) -> None:
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
    def __init__(self, level: int, x: int, y: int) -> None:
        if level < 1:
            raise DragonError("Dragon level must be higher than 1")
        super().__init__(level, x, y)

    def __repr__(self) -> str:
        return f"Dragon: lv{self.level} {self.x, self.y}"

class Treasure(Entity):
    def __repr__(self) -> str:
        return f"Treasure: {self.x, self.y}"

class Adventurer(Entity):
    def __init__(self, level: int, x: int, y: int) -> None:
        if level < 0:
            raise DragonError("Adventurer level must be positive")
        super().__init__(level, x, y)

    def __repr__(self) -> str:
        return f"Charcater: lv{self.level} {self.x, self.y}"

class WallIsYou:
    def __init__(self, file: str) -> None:
        self.board = list()
        self.adv = None
        self.drags = list()
        self.treasure_limit = None
        self.treasure = None
        self.open_map(file)

    def open_map(self, file: str):
        with open(file, "r", encoding="utf-8") as m:
            for acc_lines, line in enumerate(m):
                # on est dans un ligne de carte
                if line[0] in PIECES:
                    self.board.append(list())
                    for carac in line:
                        if carac == '\n': # fin de ligne on fait rien
                            continue

                        room = Room(carac)
                        if room.val is not None:
                            self.board[acc_lines].append(room)
                        else :
                           raise DocumentError(
                               f"A character is invalid in the {acc_lines + 1}th line"
                           )

                elif line[0] == 'A':
                    if self.adv is not None:
                        raise AdventurerError(
                            "The file can only contain one adventurer"
                        )
                    try:
                        x, y, lv = tuple(map(int, line[1:].split()))
                        self.adv = Adventurer(lv, x, y)
                        self.board[x][y].got_adv = True
                    except ValueError:
                        raise AdventurerError(
                            "The adventurer line is incorrectly written"
                        )

                elif line[0] == 'D':
                    try:
                        x, y, lv = tuple(map(int, line[1:].split()))
                        self.drags.append(Dragon(lv, x, y))
                        self.board[x][y].got_drag = True
                    except ValueError:
                        raise DragonError(
                            f"The {len(self.drags) + 1}"
                            "th dragon line is incorrectly written"
                        )

                elif line[0] == 'T':
                    if self.treasure is not None:
                        raise TreasureError(
                            "The file can only contain one treasure"
                        )
                    try:
                        x, y = tuple(map(int, line[1:].split()))
                        self.treasure = Treasure(-1, x, y)
                        self.board[x][y].got_trea = True
                    except ValueError:
                        raise TreasureError(
                            "The treasure line is incorrectly written"
                        )
                else:
                    raise DocumentError(
                        f"The first character is invalid in the {acc_lines + 1}th line"
                    )

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You have to choose a valid map")
        exit()
    game = WallIsYou(sys.argv[1])
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)