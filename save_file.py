from PIL import Image, ImageDraw

def save(GRID, lasers, points_position, cur_blocks):
    # rBlocks are the number of rows of the grid and cBlocks are the columns

    rBlocks = 0
    lazer = lasers['position']
    row = []
    Block = []

    # This for loop is used to form the Grid like in the lazor app.
    for i in range(0, len(GRID)):
        # The reading function give us a series of numbers.
        # When the list is full of zeros means that t
        if 1 in GRID[i] or 5 in GRID[i]:
            cBlocks = 0
            for k in range(0, len(GRID[i])):

                if GRID[i][k] > 0:

                    cBlocks = cBlocks + 1
                    row.append(GRID[i][k])

            Block.append(row)

        else:
            rBlocks = rBlocks + 1
            # The row list resets every time a row is appended to the GRID
            row = []
    rBlocks = rBlocks - 1
    # A,B,C will store the position of the blocks in form of lists.
    A = cur_blocks['A']
    B = cur_blocks['B']
    C = cur_blocks['C']
    # SolA,B,C will store the position of the blocks in a way they fit on the GRID
    solA = []
    solB = []
    solC = []
    # The for loop will be used to adjust the blocks in the GRID.
    if not A:
        pass
    else:
        for i in A:
            xa = i[0] / 2 - 0.5
            ya = i[1] / 2 - 0.5
            t = (xa, ya)
            solA.append(t)
    if not B:
        pass
    else:
        for i in B:
            xb = i[0] / 2 - 0.5
            yb = i[1] / 2 - 0.5
            t = (xb, yb)
            solB.append(t)

    if not C:
        pass
    else:
        for i in C:
            xc = i[0] / 2 - 0.5
            yc = i[1] / 2 - 0.5
            t = (xc, yc)
            solC.append(t)
    for i in range(rBlocks):
        for j in range(cBlocks):
            if (i, j) in solB:
                Block[i][j] = 3
            if (i, j) in solA:
                Block[i][j] = 2
            if (i, j) in solC:
                Block[i][j] = 4

    # Define size of the image
    blockSize = 100
    # create a list called figure that will store the values for each color.
    figure = [[0 for i in range(cBlocks)] for j in range(rBlocks)]
    dims1 = cBlocks * blockSize
    dims2 = rBlocks * blockSize
    # Assign the color values according to the solution of the GRID.
    for i in range(rBlocks):
        for j in range(cBlocks):
            if Block[i][j] == 1:
                figure[i][j] = 0
            if Block[i][j] == 2:
                figure[i][j] = 2
            if Block[i][j] == 3:
                figure[i][j] = 3
            if Block[i][j] == 4:
                figure[i][j] = 4
            if Block[i][j] == 5:
                figure[i][j] = 1

    # Create a new image.
    img = Image.new("RGBA", (dims1, dims2), color=0)
    for jx in range(cBlocks):
        for jy in range(rBlocks):
            x = jx * blockSize
            y = jy * blockSize

            for i in range(blockSize):
                for j in range(blockSize):
                    colors = get_colors()
                    img.putpixel((x + i, y + j),
                                 colors[figure[jy][jx]])

    draw = ImageDraw.Draw(img)
    step_size1 = int(dims1 / cBlocks)
    step_size2 = int(dims2 / rBlocks)
    y_start = 0
    y_end = dims2

    # Create the vertical lines of the grid.
    for x in range(0, dims1, step_size1):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(0, 0, 0, 255))
    x_start = 0
    x_end = dims1

    # Create the horizontal lines of the grid.
    for y in range(0, dims2, step_size2):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(0, 0, 0, 255))
    line = ((x_start, dims2 - 1), (x_end, dims2 - 1))
    draw.line(line, fill=(0, 0, 0, 255))
    line = ((dims1 - 1, y_start), (dims1 - 1, y_end))
    draw.line(line, fill=(0, 0, 0, 255))

    # Put the lazer points of the grid.
    for i in lazer:
        # i is divided by two to adjust the values of the lazer positions
        # to the range of the image.
        xp = i[0] / 2 * step_size1
        yp = (i[1] / 2) * step_size2
        shape = [(xp - 5, yp - 5), (xp + 5, yp + 5)]
        img1 = ImageDraw.Draw(img)
        img1.ellipse(shape, fill=(255, 0, 0, 255))
    # Put the black points of the grid.
    for i in points_position:
        xp = i[0] / 2 * step_size1
        yp = (i[1] / 2) * step_size2

        shape = [(xp - 10, yp - 10), (xp + 10, yp + 10)]
        img1 = ImageDraw.Draw(img)
        img1.ellipse(shape, fill=(0, 0, 0, 255))

    img.save('mad_7.png')
