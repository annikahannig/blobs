

"""
Implement some marching square renderer
"""



def _dfield_at(dfield, x, y):
    """Get density at coords provided by x, y"""
    # Clamp coordinates
    if x < 0:
        x = 0
    if y < 0:
        y = 0

    if y >= len(dfield):
        y = len(dfield) - 1

    row = dfield[y]

    if x >= len(row):
        x = len(row) - 1

    return row[x]


def _dfield_sample_box(dfield, x, y):
    top_left = _dfield_at(dfield, x, y)
    top_right = _dfield_at(dfield, x + 1, y)
    bottom_right = _dfield_at(dfield, x + 1, y + 1)
    bottom_left = _dfield_at(dfield, x, y + 1)

    return (top_left, top_right,
            bottom_left, bottom_right)


def _box_apply_threshold(box, th):
    return (box[0] >= th, box[1] >= th,
            box[2] >= th, box[3] >= th)



def shade_box_lines(box):
    if box == (False, False, False, False):
        return "_" # Empty
    if box == (True, True, True, True):
        return " " # Full
    if box == (True, False, True, False):
        return "|" # Right edge
    if box == (False, True, False, True):
        return "|" # Left edge
    if box == (False, False, True, True):
        return "_" # Bottom edge
    if box == (True, True, False, False):
        return "▔" # Upper edge
    if box == (False, True, True, True):
        return "/"
    if box == (True, True, True, False):
        return "/"
    if box == (True, True, False, True):
        return "\\"
    if box == (True, False, True, True):
        return "\\"

    return "_"


def shade_box_dots(box):
    if box == (False, False, False, False):
        return " "
    if box == (True, True, True, True):
        return "█"
    if box == (True, False, True, False):
        return "▏"
    if box == (False, True, False, True):
        return "▕"
    if box == (False, False, True, True):
        return "▃"
    if box == (True, True, False, False):
        return "▀"
    if box == (False, True, True, True):
        return "▟"
    if box == (True, True, True, False):
        return "▛"
    if box == (True, True, False, True):
        return "▜"
    if box == (True, False, True, True):
        return "▙"

    return " "


def render(dfield, shader):
    vres = len(dfield)
    hres = len(dfield[0])

    for y in range(vres - 1):
        for x in range(hres - 1):
            samples = _dfield_sample_box(dfield, x, y)
            box = _box_apply_threshold(samples, 0.05)
            c = shader(box)
            print(c, end="")
        print()


