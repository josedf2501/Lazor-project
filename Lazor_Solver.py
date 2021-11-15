

import re
from PIL import Image, ImageDraw

def read_file(filename):
    '''This reading function will return a dictionary that will contain 
     information about the gameboard, position of lazers and the directions.
     We will use the re module to search strings in a way that it will 
     facilitate our task of creating a dictionary with all our specifications.'''

    # Check if the user entered a .bff file
    if '.bff' not in filename:
        print('The file you entered is not in .bff format')
        return None
    
        
    bff = open(filename)

    
    read_grid = bff.read()
    # read file and find the grid part
    # Use re.DOTALL to get the part of the file from 'GRID START from *GRID STOP'
    grid = re.search('GRID START.*GRID STOP', read_grid, re.DOTALL)
    grid_text = read_grid[grid.start():grid.end()]
    bff.close()

    # calculate the size of our grid
    rows = 0
    col = 0

    # We will use re.search to find the first row of the grid.
    # The number of columns will be calculated with the number of elements 
    # in the first row.
    row = re.search('([oxABC] *)+[oxABC]', read_grid)
    row = read_grid[row.start():row.end()]
    row=row.replace(' ','')
    col=len(row)
    

    # creat a list and make each line of grid a element
    # to calculate the number of rows
    
  
    board = grid_text.split('\n')
    board.remove('GRID START')
    board.remove('GRID STOP')
    
    rows = len(board)
    

    # Create the list that will be used in the solver function.
    GRID = [
        [0 for i in range(2 * col + 1)]
        for j in range(2 * rows + 1)
    ]

    # change the number of responding position
    a = -1
    for i in board:
        a =a + 1
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

    # Use re.findall to get the points position.
    
    points = re.findall('P \\d \\d', read_grid)
    
   
    
    points_position = []
    #The for loop is used to put the points in form of tuples in a list 
    
    
    for i in points:
        i=i.replace(' ','')
        x = int(i[1])
        y = int(i[2])
        points_position.append((x, y))
      

    # Get the lasers positions and directions from read_grid
    # and then put the information in a dictionary.
    lasers = {}
    laser = re.findall('L \\d \\d .*\\d .*\\d', read_grid)
    
    
    p = []
    d = []
    for i in laser:
        i = i.split(' ')
        x_pos = int(i[1])
        y_pos = int(i[2])
        p.append((x_pos, y_pos))
        lasers['position'] = p
        x_dir = int(i[3])
        y_dir = int(i[4])
        d.append((x_dir, y_dir))
        lasers['direction'] = d

    # Get the blocks information and put it in a dictionary.
    blocks = {}
    block = re.findall('[ABC] \\d', read_grid)
    
    for i in block:
        i=i.replace(' ','')
        blocks[i[0]] = int(i[1])
   

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
        if x>=len(board):
            return False
        if y>=len(board[0]):
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
        point  = (point[1],point[0])
        if point not in all_points_in_path:
            return False
    return True

def run_pro(lasers,points_position,GRID,blocks):
    PATH = []
    for i in range(len(lasers['position'])):
        laser_position = (lasers['position'][i][1],lasers['position'][i][0])
        laser_direction = (lasers['direction'][i][1],lasers['direction'][i][0])
        path = laser_path(laser_position, laser_direction,
                          GRID, blocks)
        PATH.append(path)
    """if (3,3) in blocks['A'] and (9,1) in blocks['A'] and (5,1) in blocks['A'] and (11,3) in blocks['A'] and (7,5) in blocks['A'] and (5,9) in blocks['A'] and (9,9) in blocks['A'] and (11,7) in blocks['A']:
        print(PATH)"""
    return If_Win(points_position, PATH)

def run_all_blocks_comb(blocks,GRID,index,cur_blocks,lasers,points_position):
    lens = len(GRID[0])*len(GRID)
    if ('A' not in blocks or blocks['A']==0) and ('B' not in blocks or blocks['B']==0) and ('C' not in blocks or blocks['C']==0):
        if(run_pro(lasers,points_position,GRID,cur_blocks) == True):
            print(cur_blocks)
        return run_pro(lasers,points_position,GRID,cur_blocks)
    for i in range(index,lens):
        col_index = (int)(i/len(GRID[0]))
        row_index = (int)(i%len(GRID[0]))
        if GRID[col_index][row_index] == 1:
            if 'A' in blocks and blocks['A'] > 0:
                cur_blocks['A'].append((col_index,row_index))
                blocks['A'] -= 1
                if run_all_blocks_comb(blocks,GRID,i+1,cur_blocks,lasers,points_position) == True:
                    return True
                blocks['A'] += 1
                cur_blocks['A'].pop()
            if 'B' in blocks and blocks['B'] > 0:
                cur_blocks['B'].append((col_index,row_index))
                blocks['B'] -= 1
                if run_all_blocks_comb(blocks,GRID,i+1,cur_blocks,lasers,points_position) == True:
                    return True
                blocks['B'] += 1
                cur_blocks['B'].pop()
            if 'C' in blocks and blocks['C'] > 0:
                cur_blocks['C'].append((col_index,row_index))
                blocks['C'] -= 1
                if run_all_blocks_comb(blocks,GRID,i+1,cur_blocks,lasers,points_position) == True:
                    return True
                blocks['C'] += 1
                cur_blocks['C'].pop()
    return False
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


def get_colors():
    # This function returns colors for each block of the grid.
    # 0: Silver for blocks allowed
    # 1: White for no blocks allowed
    # 2: Light steel blue for fixed reflect block
    # 3: Dim grey for fixed opaque block
    # 4: Slate grey for fixed refract block

    return {
        0: (192, 192, 192),
        1: (255, 255, 255),
        2: (176, 196, 222),
        3: (105, 105, 105),
        4: (112, 128, 144),
    }
            

if __name__ == '__main__':

    filename = input('Please enter the filename you want to solve: ')
    Read = read_file(filename)
    if Read != None:
        GRID = Read[0]
        blocks = Read[1]
        lasers = Read[2]
        points_position = Read[3]
        cur_blocks = {}
        cur_blocks['A'] = []
        cur_blocks['B'] = []
        cur_blocks['C'] = []
        for i in range(len(GRID)):
            for j in range(len(GRID[0])):
                if GRID[i][j] == 2:
                    cur_blocks['A'].append((i,j))
                    if GRID[i][j] == 3:
                        cur_blocks['B'].append((i,j))
                        if GRID[i][j] == 4:
                            cur_blocks['C'].append((i,j))
        (run_all_blocks_comb(blocks,GRID,0,cur_blocks,lasers,points_position))
        c=save(GRID,lasers,points_position,cur_blocks)
        
   
