# not an object
# contains helper functions

# returns the opposite direction
def opp_dir(dir: int):
    return (dir + 8) % 16


# turn a (r, g, b) tuple into a hex string
def hex_col(col: tuple[int, int, int]):
    r,g,b = [hex(val)[2:] for val in col]
    if len(r) == 1:
        r = '0' + r
    if len(g) == 1:
        g = '0' + g
    if len(b) == 1:
        b = '0' + b
    return f'#{r}{g}{b}'




# loads a section of an image
from tkinter import PhotoImage
def get_part_image(img: PhotoImage, x1: int, y1: int, x2: int, y2: int):
    width = x2 - x1 + 1
    height = y2 - y1 + 1
    part_img = PhotoImage(width=width, height=height)
    row = 0
    colm = 0
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            transparent = img.transparency_get(x,y)
            if transparent:
                part_img.transparency_set(row, colm, True)
            else:
                col_tuple = img.get(x, y)
                col_hex = hex_col(col_tuple)
                part_img.put(col_hex, to=(row,colm))
            row += 1
        row = 0
        colm += 1
    return part_img