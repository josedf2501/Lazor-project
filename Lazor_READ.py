import sys
import re

class File:
    '''This class File will return a dictionary that will contain 
     information about the gameboard, position of lazers and the directions.
     We will use the re module to search strings in a way that it will 
     facilitate our task of creating a dictionary with all our specifications.'''

    def __init__(self, filename):

        if '.bff' not in filename:
            print('The file you entered is not in .bff format')
            sys.exit()
        self.ftpr = open(filename)

    def read_file(self):
        read_grid = self.ftpr.read()
        grid = re.search('GRID START.*GRID STOP', read_grid, re.DOTALL)
        
        # read file and find the grid part
        # Use re.DOTALL to get the part of the file from 'GRID START from *GRID STOP'
        
        grid_text = read_grid[grid.start():grid.end()]
        self.ftpr.close()
        
        # calculate the size of our grid
        rows = 0
        col = 0
        
        # We will use re.search to find the first row of the grid.
        # The number of columns will be calculated with the number of elements
        # in the first row.
        
        row = re.search('([oxABC] *)+[oxABC]', read_grid)
        row = read_grid[row.start():row.end()]
        row = row.replace(' ', '')
        col = len(row)
        
        # creat a list and make each line of grid a element
        # to calculate the number of rows
        
        board = grid_text.split('\n')
        board.remove('GRID START')
        board.remove('GRID STOP')
        rows = len(board)
        
        # Create the list that will be used in the solver function.

        GRID = [[0 for i in range(2 * col + 1)]
                for j in range(2 * rows + 1)]
        
        # change the number of responding position

        a = -1
        for i in board:
            a = a + 1
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

        points = re.findall('P \\d \\d', read_grid)
        points_position = []
        
        # Use re.findall to get the points position.
        
        for i in points:
            i = i.replace(' ', '')
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
            i = i.replace(' ', '')
            blocks[i[0]] = int(i[1])
        return (GRID, blocks, lasers, points_position)

