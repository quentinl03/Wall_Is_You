import struct as strc

def open_map(wis : strc.WallIsYou):
    with open(wis.file , "r", encoding="utf-8") as m:
        for acc_lines, line in enumerate(m):
            # on est dans un ligne de carte
            if line[0] in strc.PIECES:
                wis.board.append(list())
                for carac in line:
                    if carac == '\n': # fin de ligne on fait rien
                        continue

                    room = strc.Room(carac)
                    if room.val is not None:
                        wis.board[acc_lines].append(room)
                    else :
                        raise strc.DocumentError(
                            f"A character is invalid in the {acc_lines + 1}th line"
                        )

            elif line[0] == 'A':
                if wis.adv is not None:
                    raise strc.AdventurerError(
                        "The file can only contain one adventurer"
                    )
                try:
                    x, y, lv = tuple(map(int, line[1:].split()))
                    wis.adv = strc.Adventurer(lv, x, y)
                    wis.board[x][y].got_adv = True
                except ValueError:
                    raise strc.AdventurerError(
                        "The adventurer line is incorrectly written"
                    )

            elif line[0] == 'D':
                try:
                    x, y, lv = tuple(map(int, line[1:].split()))
                    wis.drags.append(strc.Dragon(lv, x, y))
                    wis.board[x][y].got_drag = True
                except ValueError:
                    raise strc.DragonError(
                        f"The {len(wis.drags) + 1}"
                        "th dragon line is incorrectly written"
                    )

            elif line[0] == 'T':
                if wis.treasure is not None:
                    raise strc.TreasureError(
                        "The file can only contain one treasure"
                    )
                try:
                    x, y = tuple(map(int, line[1:].split()))
                    wis.treasure = strc.Treasure(-1, x, y)
                    wis.board[x][y].got_trea = True
                except ValueError:
                    raise strc.TreasureError(
                        "The treasure line is incorrectly written"
                    )
            else:
                raise strc.DocumentError(
                    f"The first character is invalid in the {acc_lines + 1}th line"
                )