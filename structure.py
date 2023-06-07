import sys
from pprint import pprint

class DocumentError(Exception):
    pass

class AdventurerError(DocumentError):
    pass

class TreasureError(DocumentError):
    pass

class DragonError(DocumentError):
    pass

class Room:
    def __init__(self, c: str) -> None:
        self.is_ocupated = False
        match c:
            case "╨":
                self.c = "╨"
                self.val = (True, False, False, False)
            case "╞":
                self.c = "╞"
                self.val = (False, True, False, False)
            case "╥":
                self.c = "╥"
                self.val = (False, False, True, False)
            case "╡":
                self.c = "╡"
                self.val = (False, False, False, True)
            case "╚":
                self.c = "╚"
                self.val = (True, True, False, False)
            case "╔":
                self.c = "╔"
                self.val = (False, True, True, False)
            case "╗":
                self.c = "╗"
                self.val = (False, False, True, True)
            case "╝":
                self.c = "╝"
                self.val = (True, False, False, True)
            case "╠":
                self.c = "╠"
                self.val = (True, True, True, False)
            case "╦":
                self.c = "╦"
                self.val = (False, True, True, True)
            case "╣":
                self.c = "╣"
                self.val = (True, False, True, True)
            case "╩":
                self.c = "╩"
                self.val = (True, True, False, True)
            case "║":
                self.c = "║"
                self.val = (True, False, True, False)
            case "═":
                self.c = "═"
                self.val = (False, True, False, True)
            case "╬":
                self.c = "╬"
                self.val = (True, True, True, True)
            case _:
                self.c = c
                self.val = None

    def __str__(self) -> str:
        return self.c
    
    def __repr__(self) -> str:
        return self.c
    
    def rotate(self):
        self.val = (self.val[3], self.val[0], self.val[1], self.val[2])
        self.c = self.c + "1rota" # a motif

class Entity:
    def __init__(self, level: int, x: int, y: int) -> None:
        self.level = level
        self.x = x
        self.y = y

class Dragon(Entity):
    def __init__(self, level: int, x: int, y: int) -> None:
        super().__init__(level, x, y)

    def __repr__(self) -> str:
        return f"Dragon lv: {self.level, (self.x, self.y)}"

class Treasure(Entity):
    def __init__(self, level: int, x: int, y: int) -> None:
        super().__init__(level, x, y)

    def __repr__(self) -> str:
        return f"Treasure lv: {self.level, (self.x, self.y)}"

class Adventurer(Entity):
    def __init__(self, level: int, x: int, y: int) -> None:
        super().__init__(level, x, y)

    def __repr__(self) -> str:
        return f"Charcater lv: {self.level, (self.x, self.y)}"


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
                if Room(line[0]).val is not None:
                    self.board.append(list())
                    for carac in line:
                        if carac == '\n': # fin de ligne on fait rien
                            continue

                        room = Room(carac)
                        if room.val is not None:
                            self.board[acc_lines].append(room)
                        else :
                           raise DocumentError

                elif line[0] == 'A':
                    if self.adv is not None:
                        raise AdventurerError(
                            "The file can only contain one adventurer"
                        )
                    try:
                        lv, x, y = tuple(map(int, line[1:].split()))
                        self.adv = Adventurer(lv, x, y)
                    except ValueError:
                        raise AdventurerError(
                            "The adventurer line is incorrectly written"
                        )
                    
                elif line[0] == 'D':
                    try:
                        lv, x, y = tuple(map(int, line[1:].split()))
                        self.drags.append(Dragon(lv, x, y))
                    except ValueError:
                        raise DragonError(
                            f"The {len(self.drag)} dragon line is incorrectly written"
                        )
       

                elif line[0] == 'T':
                    if self.treasure is not None:
                        raise TreasureError(
                            "The file can only contain one treasure"
                        )
                    try:
                        x, y = tuple(map(int, line[1:].split()))
                        self.treasure = Treasure(-1, x, y)
                    except ValueError:
                        raise TreasureError(
                            "The treasure line is incorrectly written"
                        )
                else:
                    raise DocumentError

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit()
    game = WallIsYou(sys.argv[1])
    pprint(game.board)
    print(game.adv)
    print(game.drags)
    print(game.treasure)