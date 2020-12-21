from PIL import Image, ImageDraw2

MARGIN = 10


def draw_grid(img_size, draw, pen):
    draw.line((img_size[0] / 3, 0, img_size[0] / 3, img_size[1]), pen)
    draw.line((2 * img_size[0] / 3, 0, 2 * img_size[0] / 3, img_size[1]), pen)
    draw.line((0, img_size[1] / 3, img_size[0], img_size[1] / 3), pen)
    draw.line((0, 2 * img_size[1] / 3, img_size[0], 2 * img_size[1] / 3), pen)


def make_x(image, draw, space, pen):
    horiz = space % 3
    vert = int(space / 3)
    horiz_chunk = image.size[0] / 6
    vert_chunk = image.size[1] / 6
    draw.line((2*horiz*horiz_chunk+MARGIN, 2*vert*vert_chunk + MARGIN,
               (2*horiz + 2)*horiz_chunk - MARGIN, (2*vert + 2)*vert_chunk - MARGIN), pen)
    draw.line((2*horiz*horiz_chunk+MARGIN, (2*vert + 2)*vert_chunk - MARGIN,
               (2*horiz + 2)*horiz_chunk - MARGIN, 2*vert*vert_chunk + MARGIN), pen)


def make_o(image, draw, space, pen_in):
    horiz = space % 3
    vert = int(space / 3)
    horiz_chunk = image.size[0] / 6
    vert_chunk = image.size[1] / 6
    for offset in range(-3, 3):
        draw.ellipse((2 * horiz * horiz_chunk + MARGIN-offset, 2 * vert * vert_chunk + MARGIN-offset,
                    (2 + 2 * horiz) * horiz_chunk - MARGIN+offset, (2 + 2 * vert) * vert_chunk - MARGIN+offset), pen_in)


def draw_game(moves_list):
    """
    Draws the game onto an image based on the moves taken
    :param moves_list: list of strings corresponding to moves
    :return: image of tic tac toe board based on given moves
    """
    img_size = (300, 300)
    board = Image.new("RGB", img_size, (0, 120, 150))
    drawer = ImageDraw2.Draw(board)
    draw_grid(img_size, drawer, ImageDraw2.Pen("white", width=5))
    o_pen = ImageDraw2.Pen("red", width=5)
    x_pen = ImageDraw2.Pen("purple", width=5)
    for player, space in moves_list:
        if player == 'O':
            make_o(board, drawer, int(space), o_pen)
        elif player == 'X':
            make_x(board, drawer, int(space), x_pen)
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


sample_game = [("X", 0), ("O", 3), ("X", 3), ("O", 8), ("X", 6)]

test = draw_game(sample_game)

test.show()

# print(check_win(sample_game))

# img.show()
# img.save("sample_imgs/tic_tac1.png")


