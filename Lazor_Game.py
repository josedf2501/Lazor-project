
import re


def read_bff(filename):
    '''
    Read bff files and turn it to a list representing grid, and two
    dictionaries including information about lasers and available blocks
    **Parameters**
        filename: *str*
            The name of bff file
    **Returns**
        GRID: *list*
            A 2D list representing the layout of grid
            0 represent gaps
            1 represent an allowed position for block
            2 represent reflect block
            3 represent opaque block
            4 represent refract block
            5 represent a position can not place block
            6 represent the points that need laser to intersect
        blocks: *dictionary*
            a dictionary includes how many and what kind of block we can use
        lasers: *dictionary*
            a dictionary includes the position and direction of lasers
        points_position: *list*
            a list that contains all the points we need to pass
    '''
    # ensure filename
    if ".bff" in filename:
        filename = filename.split(".bff")[0]
    bff = open(filename + ".bff")

    # read file and find the grid part
    content = bff.read()
    pattern = 'GRID START.*GRID STOP'
    grid = re.search(pattern, content, re.DOTALL)
    grid_text = content[grid.start():grid.end()]
    bff.close()

    # calculate the size of our grid
    rows = 0
    columns = 0

    # find one line of grid, calculate how many columns we need
    row = re.search('([oxABC] *)+[oxABC]', content)
    row = content[row.start():row.end()]
    for i in row:
        if i == 'o' or i == 'x' or i == 'A' or i == 'B' or i == 'C':
            columns += 1

    # creat a list and make each line of grid a element
    # to calculate the number of rows
    Rows = grid_text.split('\n')
    Rows.remove('GRID START')
    Rows.remove('GRID STOP')
    rows = len(Rows)

    # creat the 2d list
    GRID = [
        [0 for i in range(2 * columns + 1)]
        for j in range(2 * rows + 1)
    ]

    # change the number of responding position
    a = -1
    for i in Rows:
        a += 1
        k = 0
        for j in i:
            if j == 'o':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 1
            if j == 'A':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 2
            if j == 'B':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 3
            if j == 'C':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 4
            if j == 'x':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 5

    # obtain the points information of bff files
    # store them to a list and change their position
    # number to 6
    points = re.findall('P \\d \\d', content)
    points_position = []
    for i in points:
        position = i.split(' ')
        x_coord = int(position[1])
        y_coord = int(position[2])
        points_position.append((x_coord, y_coord))
        # GRID[y_coord][x_coord] = 6

    # obtain the lasers information of bff files
    # and combine them to a dictionary
    lasers = {}
    laser = re.findall('L \\d \\d .*\\d .*\\d', content)
    p = []
    d = []
    for i in laser:
        info = i.split(' ')
        x_coord = int(info[1])
        y_coord = int(info[2])
        p.append((x_coord, y_coord))
        lasers['position'] = p
        x_dir = int(info[3])
        y_dir = int(info[4])
        d.append((x_dir, y_dir))
        lasers['direction'] = d

    # obtian the blocks information of bff files
    # and combine them to a dictionary
    blocks = {}
    block = re.findall('[ABC] \\d', content)
    for i in block:
        information = i.split(' ')
        blocks[information[0]] = int(information[1])

    return (GRID, blocks, lasers, points_position)




def laser_path(position, direction, board, blocks):

    x = position[0]
    y = position[1]
    direction_x = direction[0]
    direction_y = direction[1]
    #main lazer path
    lazer_pth = []
    lazer_pth.append((x, y))
    #lazer path from C block
    seperate_path = []
    hit_block_index = ()
    #check if current lazor has next step.
    if x%2 == 0 and [x-1,y] in blocks['A'] and [x+1,y] in blocks['A'] or x%2 == 1 and [x,y-1] in blocks['A'] and [x,y+1] in blocks['A']:
        return lazer_pth
    #check the index of block if current lazor hits blocks.
    if x % 2 == 0:
        hit_block_index = (x + direction_x, y)
    elif x % 2 == 1:
        hit_block_index = (x, y + direction_y)
    #check if this block inside the board.
    def check_if_out_of_board(block,board):
        x = block[0]
        y = block[1]
        if x<0:
            return False
        if y<0:
            return False
        if x>=len(board[0]):
            return False
        if y>=len(board):
            return False
        return True

    #check if current block is inside the board.
    #if block is outside the board then merge main path and seperate path and return the result.
    while check_if_out_of_board(hit_block_index,board):
        #if block is C type, then seperate a lazor path.
        if hit_block_index in blocks['C']:
            seperate_path = laser_path(
                (x + direction_x, y + direction_y), (direction_x, direction_y), board, blocks)
            #merge two paths
            lazer_pth = lazer_pth + seperate_path
            #make points in path to be unique.
            lazer_pth_unique = set()
            for point in lazer_pth:
                lazer_pth_unique.add(point)
            lazer_pth = list(lazer_pth_unique)
        #if block is C or A type, then change the lazor direction
        if hit_block_index in blocks['A'] or hit_block_index in blocks['C']:
            if x%2==0:
                direction_x *= -1
            elif x%2==1:
                direction_y *= -1
        #if block is B type, then path stop
        elif hit_block_index in blocks['B']:
            return lazer_pth
        x = x + direction_x
        y = y + direction_y
        if x % 2 == 0:
            hit_block_index = (x + direction_x, y)
        elif x % 2 == 1:
            hit_block_index = (x, y + direction_y)
        lazer_pth.append((x, y))
    
    return lazer_pth


def If_Win(points_position, lazer_path):
    #merge all lazer_path to all points.
    all_points_in_path = set()
    for path in lazer_path:
        for point in path:
            all_points_in_path.add(point)
    #for each points in points_position, if all points is part of lazor_path then win, otherwise lose.
    for point in points_position:
        if point not in all_points_in_path:
            return False
    return True



if __name__ == '__main__':
    filename = input('Please enter the filename you want to solve: ')
    Read = read_bff(filename)
    GRID = Read[0]
    blocks = Read[1]
    lasers = Read[2]
    points_position = Read[3]
    blocks = {}
    blocks['A'] = [(1, 5), (7, 3)]
    blocks['B'] = []
    blocks['C'] = [(5, 1)]
    PATH = []
    for j in range(len(lasers['position'])):
        laser_position = lasers['position'][j]
        laser_direction = lasers['direction'][j]
        # print(laser_position)
        x_dimension = len(GRID[0]) - 1
        y_dimension = len(GRID) - 1
        # print(y_dimension)
        path = laser_path(laser_position, laser_direction,
                          GRID, blocks)
        PATH.append(path)
    print(PATH)
    print(If_Win(points_position, PATH))
    if If_Win(points_position, PATH) is True:
        answer = blocks

        