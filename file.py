import structure as struct


def open_map(wiy: struct.WallIsYou) -> None:
    """Read the map in wiy.file,
    which tell you the path to the file to read.


    Args:
        wiy (struct.WallIsYou): game to read

    Raises:
        struct.DocumentError: When the first charater of a line is not valid,
        other functions will check inline issues.
    """
    with open(wiy.file, "r", encoding="utf-8") as m:
        for acc_lines, line in enumerate(m):

            # We're in a line of the maze
            if line[0] in struct.PIECES:
                readline_maze(wiy, line, acc_lines)

            elif line[0] == 'A':
                readline_adventurer(wiy, line)

            elif line[0] == 'D':
                readline_dragon(wiy, line)

            else:
                raise struct.DocumentError(
                    f"The first character is invalid in the {acc_lines + 1}th line"
                )
    wiy.height = len(wiy.board)
    wiy.width = len(wiy.board[0])


def readline_maze(wiy: struct.WallIsYou, line: str, nb_line: int) -> None:
    """Read a line where the first character represent a room.

    Args:
        wiy (struct.WallIsYou): game modified
        line (str): line to read
        nb_line (int): number of line to help in case of issues

    Raises:
        struct.DocumentError: In case of a an unexpected character.
    """
    lst_res = list()
    for carac in line:
        if carac == '\n':  # end of line, do nothing
            continue

        room = struct.Room(carac)
        if room.val is not None:
            lst_res.append(room)
        else:
            raise struct.DocumentError(
                f"A character is invalid in the {nb_line + 1}th line"
            )
    wiy.board.append(lst_res)


def readline_adventurer(wiy: struct.WallIsYou, line: str) -> None:
    """Read a line where the first character represent a adventurer

    Args:
        wiy (struct.WallIsYou): game modified
        line (str): line to read

    Raises:
        struct.AdventurerError: If there are 2 adventurer
        struct.AdventurerError: If the line is not valid
        struct.AdventurerError: If the room is occupated by another entity
    """
    # There are 2 adventurers
    if wiy.adv is not None:
        raise struct.AdventurerError(
            "The file can only contain one adventurer"
        )
    # Read line
    try:
        t_adv = tuple(map(int, line[1:].split()))
        if len(t_adv) == 2:  # no level for the adv (1st load)
            y, x = t_adv
            wiy.adv = struct.Adventurer(y, x)
        else:  # level for the adv (save)
            y, x, lv = t_adv
            wiy.adv = struct.Adventurer(y, x, lv)
        wiy.board[y][x].got_adv = True
    # Line is not correct
    except ValueError:
        raise struct.AdventurerError(
            "The adventurer line is incorrectly written"
        )
    # If the room is already occupated
    if (wiy.board[y][x].got_drag or
            wiy.board[y][x].got_trea):
        raise struct.AdventurerError(
            "The adventurer is in a room already occupated"
        )


def readline_dragon(wiy: struct.WallIsYou, line: str) -> None:
    """Read a line where the first character represent a dragon.

    Args:
        wiy (struct.WallIsYou): game modified
        line (str): line to read

    Raises:
        struct.DragonError: If there are 2 dragon in the same room
        struct.DragonError: If the line is not valid
        struct.DragonError: If the room is occupated by another entity
    """
    # Read line
    try:
        y, x, lv = tuple(map(int, line[1:].split()))
        wiy.drags.append(struct.Dragon(y, x, lv))
        # There are 2 dragon in the same room
        if wiy.board[y][x].got_drag is True:
            raise struct.DragonError(
                "You can place only one dragon per room"
            )
        wiy.board[y][x].got_drag = True
    # Line is not correct
    except ValueError:
        raise struct.DragonError(
            f"The {len(wiy.drags) + 1}"
            "th dragon line is incorrectly written"
        )
    # If the room is already occupated
    if (wiy.board[y][x].got_adv or
            wiy.board[y][x].got_trea):
        raise struct.DragonError(
            "The dragon is in a room already occupated"
        )


def save(wiy: struct.WallIsYou, is_save: bool) -> None:
    """Saves the actual state of the game.

    Args:
        wiy (struct.WallIsYou): Game to save
        is_save (bool): If manual save please choose True
                        false is for the map editor
    """
    to_add = ".wiy"
    if is_save:
        to_add = "_save" + to_add
    with open(wiy.file[:-4] + to_add, "w", encoding="utf-8") as f:
        for line in wiy.board:
            f.write(save_line_maze(line) + "\n")

        f.write(f"A {wiy.adv.y} {wiy.adv.x} {wiy.adv.level}\n")

        for elem in wiy.drags:
            f.write(f"D {elem.y} {elem.x} {elem.level}\n")


def save_line_maze(line: list[struct.Room]) -> str:
    """Generate a string which represent a line of the maze.

    Args:
        line (list[struct.Room]): Line of the maze

    Returns:
        str: string representing the line given in parameter
    """
    return ''.join(elem.c for elem in line)
