from PIL import Image, ImageDraw2

MARGIN = 8


def draw_grid(img_size, draw, big_pen, little_pen):
    for board_num in range(9):
        v_off = int(board_num / 3) * img_size[1] / 3
        h_off = int(board_num % 3) * img_size[0] / 3
        draw.line((img_size[0] / 9 + h_off, v_off, img_size[0] / 9 + h_off, img_size[1] / 3 + v_off), little_pen)
        draw.line(((2*img_size[0]/9) + h_off, v_off, (2*img_size[0]/9) + h_off, img_size[1] / 3 + v_off), little_pen)
        draw.line((h_off, img_size[1] / 9 + v_off, h_off + img_size[0] / 3, img_size[1]/9 + v_off), little_pen)
        draw.line((h_off, (2*img_size[1] / 9 ) + v_off, h_off + img_size[0] / 3, (2*img_size[1]/9) + v_off), little_pen)
    draw.line((img_size[0] / 3, 0, img_size[0] / 3, img_size[1]), big_pen)
    draw.line((2 * img_size[0] / 3, 0, 2 * img_size[0] / 3, img_size[1]), big_pen)
    draw.line((0, img_size[1] / 3, img_size[0], img_size[1] / 3), big_pen)
    draw.line((0, 2 * img_size[1] / 3, img_size[0], 2 * img_size[1] / 3), big_pen)


def make_x(image, draw, sector, location, pen):
    horiz = location % 3
    vert = int(location / 3)
    horiz_chunk = image.size[0] / 18
    vert_chunk = image.size[1] / 18
    h_sec_off = (sector % 3) * image.size[0] / 3
    v_sec_off = int(sector / 3) * image.size[1] / 3

    draw.line((2*horiz*horiz_chunk+MARGIN + h_sec_off, 2*vert*vert_chunk + MARGIN + v_sec_off,
               (2*horiz + 2)*horiz_chunk - MARGIN + h_sec_off, (2*vert + 2)*vert_chunk - MARGIN + v_sec_off), pen)
    draw.line((2*horiz*horiz_chunk+MARGIN + h_sec_off, (2*vert + 2)*vert_chunk - MARGIN + v_sec_off,
               (2*horiz + 2)*horiz_chunk - MARGIN + h_sec_off, 2*vert*vert_chunk + MARGIN + v_sec_off), pen)


def make_o(image, draw, sector, location, pen_in):
    horiz = location % 3
    vert = int(location / 3)
    horiz_chunk = image.size[0] / 18
    vert_chunk = image.size[1] / 18
    h_sec_off = (sector % 3) * image.size[0] / 3
    v_sec_off = int(sector / 3) * image.size[1] / 3
    for offset in range(-2, 2):
        for offset2 in range(-2, 2):
            draw.ellipse((2 * horiz * horiz_chunk + MARGIN-offset + h_sec_off, 2 * vert * vert_chunk + MARGIN-offset2 + v_sec_off,
                    (2 + 2 * horiz) * horiz_chunk - MARGIN+offset+ h_sec_off, (2 + 2 * vert) * vert_chunk - MARGIN+offset2 + v_sec_off), pen_in)
        # draw.ellipse((2 * horiz * horiz_chunk + MARGIN - offset, 2 * vert * vert_chunk + MARGIN - offset,
        #               (2 + 2 * horiz) * horiz_chunk - MARGIN + offset, (2 + 2 * vert) * vert_chunk - MARGIN + offset),
        #              pen_in)


def make_fill(image, draw, sector, pen_in):
    col = pen_in.color
    new_col = tuple([max(0, color - 80) for color in col])
    brush_in = ImageDraw2.Brush(f"rgb{new_col}")
    h_sec_off = (sector % 3) * image.size[0] / 3
    v_sec_off = int(sector / 3) * image.size[1] / 3
    draw.rectangle((h_sec_off, v_sec_off, h_sec_off + image.size[0] / 3, v_sec_off + image.size[1] / 3), brush_in)


def draw_game(moves_list, sectors):
    """
    Draws the game onto an image based on the moves taken
    :param moves_list: list of strings corresponding to moves
    :param sectors: Dict mapping sectors to their status, no winner ("N") or winner ("X" or "O")
    :return: image of tic tac toe board based on given moves
    """
    print(sectors)
    img_size = (500, 500)
    board = Image.new("RGB", img_size, (0, 120, 150))
    drawer = ImageDraw2.Draw(board)

    o_pen = ImageDraw2.Pen("red", width=5)
    x_pen = ImageDraw2.Pen("purple", width=5)
    for sector, val in sectors.items():
        if val == "X":
            make_fill(board, drawer, int(sector), x_pen)
        elif val == "O":
            make_fill(board, drawer, int(sector), o_pen)
    draw_grid(img_size, drawer, ImageDraw2.Pen("white", width=5), ImageDraw2.Pen("gray", width=5))
    for player, sec, loc in moves_list:
        if player == 'O':
            make_o(board, drawer, int(sec), int(loc), o_pen)
        elif player == 'X':
            make_x(board, drawer, int(sec), int(loc), x_pen)
    last_p, last_s, last_l = moves_list[len(moves_list) - 1]
    last_pen = ImageDraw2.Pen("gold", width = 7)
    if last_p == "X":
        make_x(board, drawer, int(last_s), int(last_l), x_pen)
    else:
        make_o(board, drawer, int(last_s), int(last_l), last_pen)
    # TODO: change last coloring to background fill instead of the move
    return board


win_list = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7}]


def check_win(move_list):
    x_spaces = set([])
    o_spaces = set([])
    for player, space in move_list:
        if player == 'X':
            x_spaces.add(int(space)+1)
        elif player == 'O':
            o_spaces.add(int(space)+1)
    for win_cond in win_list:
        if win_cond.issubset(x_spaces):
            return "X"
        if win_cond.issubset(o_spaces):
            return "O"
    return "N"


# img_size = (500, 400)
# board = Image.new("RGB", img_size, (0, 120, 150))
# o_pen = ImageDraw2.Pen("red", width=5)
# x_pen = ImageDraw2.Pen("purple", width=5)
# drawer = ImageDraw2.Draw(board)
#
# make_fill(board, drawer, 3, x_pen)
# draw_grid(img_size, drawer, ImageDraw2.Pen("white", width=5), ImageDraw2.Pen("gray", width=5))
#
# make_x(board, drawer, 6, 4, x_pen)
# make_o(board, drawer, 5, 4, o_pen)
# make_x(board, drawer, 3, 6, x_pen)
# make_o(board, drawer, 0, 2, o_pen)
#
#
# board.show()

# sample_game = ["X:1", "O:4", "X:3", "O:5", "X:6"]

# print(check_win(sample_game))

# img.show()
# img.save("sample_imgs/tic_tac1.png")


