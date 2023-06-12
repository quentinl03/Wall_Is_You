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
                    t_adv = tuple(map(int, line[1:].split()))
                    if len(t_adv) == 2: #no level for the adv (1st load)
                        y, x = t_adv
                        wis.adv = strc.Adventurer(y, x)
                    else: #level for the adv (save)
                        y, x, lv = t_adv
                        wis.adv = strc.Adventurer(y, x, lv)
                    wis.board[y][x].got_adv = True
                except ValueError:
                    raise strc.AdventurerError(
                        "The adventurer line is incorrectly written"
                    )

            elif line[0] == 'D':
                try:
                    y, x, lv = tuple(map(int, line[1:].split()))
                    wis.drags.append(strc.Dragon(y, x, lv))
                    wis.board[y][x].got_drag = True
                except ValueError:
                    raise strc.DragonError(
                        f"The {len(wis.drags) + 1}"
                        "th dragon line is incorrectly written"
                    )
            else:
                raise strc.DocumentError(
                    f"The first character is invalid in the {acc_lines + 1}th line"
                )
    wis.height = len(wis.board)
    wis.width = len(wis.board[0])