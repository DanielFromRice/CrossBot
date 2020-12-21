from PIL import Image, ImageDraw2

MARGIN = 8


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


img_size = (300, 300)

img = Image.new("RGB", img_size, (0, 120, 150))

drawer = ImageDraw2.Draw(img)
pen = ImageDraw2.Pen("white", width=5)
p1 = ImageDraw2.Pen("red", width=5)
p2 = ImageDraw2.Pen("purple", width=5)

# Make Grid
draw_grid(img_size, drawer, pen)

make_x(img, drawer, 7, p1)
make_o(img, drawer, 5, p2)
make_x(img, drawer, 4, p1)
make_o(img, drawer, 6, p2)

img.show()
img.save("sample_imgs/tic_tac1.png")


