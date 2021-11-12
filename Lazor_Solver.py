

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



        