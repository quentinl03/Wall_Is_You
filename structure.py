import sys
from pprint import pprint

class DocumentError(Exception):
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

class WallIsYou:
    def __init__(self, map: str) -> None:
        self.board = list()
        self.open_map(map)

    def open_map(self, map: str):
        with open(map, "r", encoding="utf-8") as m:
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


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit()
    game = WallIsYou(sys.argv[1])
    pprint(game.board)