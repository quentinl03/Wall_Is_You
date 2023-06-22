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
    """Class to make loops with directions more understandable.
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class DocumentError(Exception):
    """Class for document errors.
    """
    pass


class EntityError(DocumentError):
    """Class for any entities errors.
    """
    pass


class AdventurerError(EntityError):
    """Class for Adventurer errors only.
    """
    pass


class TreasureError(EntityError):
    """Class for Treasure errors only.
    """
    pass


class DragonError(EntityError):
    """Class for Dragon error only.
    """
    pass


class Room:
    """Class representing a room in the board.
    """
    def __init__(self, c: str) -> None:
        """Initializes room class.

        Args:
            c (str): character representing the room

        Attributes:
            got_adv (bool): The room contain the adventurer.
            got_drag (bool): The room contain a dragon.
            got_trea (bool): The room contain the treasure.
            c (str): The character representing the room.
            val (Tuple[bool, bool, bool, bool]): (Top, Right, Bottom, Left)
                    Represents which sides are open.
        """
        self.got_adv = False
        self.got_drag = False
        self.got_trea = False
        self.c = c
        self.val = None
        if c in PIECES.keys():  # .keys not obligatory
            self.val = PIECES[c]

    def __repr__(self) -> str:
        """Return a character representing the room.

        White: Empty
        Red: Dragon
        Green: Adventurer
        Yellow: Treasure

        Returns:
            str: Colored character that represents the room
        """
        if self.got_adv:
            return f"{clrm.Fore.GREEN}{self.c}{clrm.Style.RESET_ALL}"
        if self.got_drag:
            return f"{clrm.Fore.RED}{self.c}{clrm.Style.RESET_ALL}"
        if self.got_trea:
            return f"{clrm.Fore.YELLOW}{self.c}{clrm.Style.RESET_ALL}"
        return self.c

    def rotate(self) -> None:
        """Rotates the room clockwise one step.
        """
        self.val = (self.val[3], self.val[0], self.val[1], self.val[2])
        self.c = PIECES_R[self.val]

    def is_connected(self, other, d: Dir) -> bool:
        """Tell if 2 rooms are connected.

        Args:
            other (Room): Second room
            d (Dir): Position of the second room in comparison to the first

        Returns:
            bool: True if romms are connected
                else False
        """
        return (
            (d == Dir.NORTH and self.val[0] and other.val[2]) or

            (d == Dir.EAST and self.val[1] and other.val[3]) or

            (d == Dir.SOUTH and self.val[2] and other.val[0]) or

            (d == Dir.WEST and self.val[3] and other.val[1])
        )


@total_ordering
class Entity:
    """General class for all entities in the game.
    """
    def __init__(self, y: int, x: int, level: int = 1) -> None:
        """Initializes entity class.

        Args:
            y (int): coordinate (height)
            x (int): coordinate (width)
            level (int, optional): Level of the entity . Defaults to 1.

        Raises:
            EntityError: Level must be >=1
            EntityError: x > 0 or x > y
        """
        if level < 1:
            raise EntityError("Entity level must be positive")
        self.level = level

        if x < 0 or y < 0:
            raise EntityError("Coordinates must be positive")
        self.x = x
        self.y = y

    def __lt__(self, other) -> bool:
        """Compares entity levels

        Args:
            other (Entity): Entity to compare

        Returns:
            bool: if 1st level < 2nd level
        """
        return self.level < other.level

    def __eq__(self, other) -> bool:
        """Compares entity levels

        Args:
            other (Entity): Entity to compare

        Returns:
            bool: if 1st level == 2nd level
        """
        return self.level == other.level


class Dragon(Entity):
    """ Inherit from the entity class.

    Reserved for dragons.
    """
    def __repr__(self) -> str:
        """Return a string representing the dragon with his level and his coordinate.

        Returns:
            str: Representative string
        """
        return f"Dragon: lv{self.level} {self.x, self.y}"


class Treasure(Entity):
    """ Inherit from the entity class.

    Reserved for treasure.
    """
    def __repr__(self) -> str:
        """Return a string representing the Treasure whith his coordinate.

        Returns:
            str: Representative string
        """
        return f"Treasure: {self.x, self.y}"


class Adventurer(Entity):
    """ Inherit from the entity class.

    Reserved for Adventurer.
    """
    def __repr__(self) -> str:
        """Return a string representing the Adventurer with his level and his coordinate.

        Returns:
            str: Representative string
        """
        return f"Charcater: lv{self.level} {self.x, self.y}"


class WallIsYou:
    """Class representing the entire game
    """
    def __init__(self, file: str) -> None:
        """Initializes WallIsYou class.

        Args:
            file (str): Path to the file to read

        Attributes:
            height (int >= 0): Height of the board.
            width (int >= 0): Width of the board.
            file (str): Path to the file to read.
            c (str): The character representing the room.
            board (list[list[Room]]): Board thats represents the game
            adv (Adventurer): Store adventurer info.
            drags (list[Dragon]): Store the list of dragons info.
            treasure (Optional[Treasure]): Store treasure info.
        """
        self.height = 0
        self.width = 0
        self.file = file
        self.board = list()
        self.adv = None
        self.drags = list()
        self.treasure = None

    def level_drag(self, x: int, y: int) -> int:
        """Get the level of the dragon for his coordinate.
        If there is no dragon return 0

        Args:
            x (int): coordinate (width)
            y (int): coordinate (height)

        Returns:
            int: Dragon's level or 0
        """
        for elem in self.drags:
            if x == elem.x and y == elem.y:
                return elem.level
        return 0

    def is_in_board(self, x: int, y: int) -> bool:
        """Return if the coordinates are inside the board.
        (0 <= x < width) (0 <= y < height)

        Args:
            x (int): coordinate (width)
            y (int): coordinate (height)

        Returns:
            bool: True if the coordinate are inside the board.
            else False
        """
        return not (
            x < 0 or y < 0 or
            x >= self.width or
            y >= self.height)

    def victory(self) -> bool:
        """Return if the state of the game is win.

        All dragon are dead.
        Returns:
            bool: True if the game is win
                else False
        """
        return len(self.drags) == 0

    def defeat(self, x: int, y: int) -> bool:
        """Return if the state of the game is loose.

        The adventurer fighting a higher level dragon.

        Returns:
            bool: True if the game is loose
                else False
        """
        lv_drag = self.level_drag(x, y)
        if (not self.is_in_board(x, y) or
            not self.board[y][x].got_drag or
                lv_drag == 0):
            return False
        return self.adv.level < lv_drag

    def play(self, dest_x: int, dest_y: int) -> None:
        """Moove the adventurer to the destination coordinates.

        You have to check loose before.
        Args:
            x (int): coordinate (width)
            y (int): coordinate (height)
        """
        if (not self.is_in_board(dest_x, dest_y) or
                (not self.board[dest_y][dest_x].got_drag and
                 not self.board[dest_y][dest_x].got_trea)):
            return

        self.board[self.adv.y][self.adv.x].got_adv = False

        self.board[dest_y][dest_x].got_adv = True
        self.board[dest_y][dest_x].got_drag = False
        self.board[dest_y][dest_x].got_trea = False
        self.adv.x = dest_x
        self.adv.y = dest_y

        for elem in self.drags:
            if elem.x == dest_x and elem.y == dest_y:
                self.drags.remove(elem)
                self.adv.level += 1
        if self.treasure and self.treasure.x == dest_x and self.treasure.y == dest_y:
            self.treasure = None
