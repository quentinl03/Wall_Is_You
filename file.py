import struct

def open_map(wis : struct.WallIsYou) -> None:
    with open(wis.file , "r", encoding="utf-8") as m:
        for acc_lines, line in enumerate(m):

            # We're in a line of the maze
            if line[0] in struct.PIECES:
                wis.board.append(list())
                for carac in line:
                    if carac == '\n': # end of line, do nothing
                        continue

                    room = struct.Room(carac)
                    if room.val is not None:
                        wis.board[acc_lines].append(room)
                    else :
                        raise struct.DocumentError(
                            f"A character is invalid in the {acc_lines + 1}th line"
                        )

            elif line[0] == 'A':
                # There are 2 adventurers
                if wis.adv is not None:
                    raise struct.AdventurerError(
                        "The file can only contain one adventurer"
                    )
                # Read line
                try:
                    t_adv = tuple(map(int, line[1:].split()))
                    if len(t_adv) == 2: #no level for the adv (1st load)
                        y, x = t_adv
                        wis.adv = struct.Adventurer(y, x)
                    else: #level for the adv (save)
                        y, x, lv = t_adv
                        wis.adv = struct.Adventurer(y, x, lv)
                    wis.board[y][x].got_adv = True
                # Line is not correct
                except ValueError:
                    raise struct.AdventurerError(
                        "The adventurer line is incorrectly written"
                    )
                # If the room is already occupated
                if (wis.board[y][x].got_drag is True or
                    wis.board[y][x].got_trea is True):
                    raise struct.AdventurerError(
                        "The adventurer is in a room already occupated"
                    )

            elif line[0] == 'D':
                # Read line
                try:
                    y, x, lv = tuple(map(int, line[1:].split()))
                    wis.drags.append(struct.Dragon(y, x, lv))
                    # There are 2 dragon in the same room
                    if wis.board[y][x].got_drag is True:
                        raise struct.DragonError(
                            "You can place only one dragon per room"
                        )
                    wis.board[y][x].got_drag = True
                # Line is not correct
                except ValueError:
                    raise struct.DragonError(
                        f"The {len(wis.drags) + 1}"
                        "th dragon line is incorrectly written"
                    )
                # If the room is already occupated
                if (wis.board[y][x].got_adv is True or
                    wis.board[y][x].got_trea is True):
                    raise struct.DragonError(
                        "The dragon is in a room already occupated"
                    )

            else:
                raise struct.DocumentError(
                    f"The first character is invalid in the {acc_lines + 1}th line"
                )
    wis.height = len(wis.board)
    wis.width = len(wis.board[0])