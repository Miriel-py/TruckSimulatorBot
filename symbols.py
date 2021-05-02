LEFT="⬅️"
DOWN="⬇️"
UP="⬆️"
RIGHT="➡️"
STOP="\N{OCTAGONAL SIGN}"
LIST_ITEM=":small_orange_diamond:"

def get_drive_position_symbols(position):
    x = position[0]
    y = position[1]
    max_x = 16
    max_y = 16
    symbols = []
    if x > 0:
        symbols.append(LEFT)
    if y > 0:
        symbols.append(DOWN)
    if y < max_y:
        symbols.append(UP)
    if x < max_x:
        symbols.append(RIGHT)

    symbols.append(STOP)
    return symbols
