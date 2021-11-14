import math
import numpy as np

def read_bff_file(file_name):
    
   # This function reads a .bff file and makes it readable

    # Parameters 
        #file_name: *str*
            name of lazor puzzle input file.

    # Returns 
        board_info: *list* *str*
            list of all relevant lines of input file to be used in board
            generation
    
    if ".bff" not in file_name:
        file_name += ".bff"  # Adds extension to open file with .bff extension.

    print("Hello, welcome to the gameboard reader.")
    my_file = open(file_name, "r")

    board_info = [i.split("\n") for i in my_file]
    for each_line in board_info:
        if len(each_line) > 1:
            # Remove the \n Except for last line which has no \n
            del each_line[-1]

    board_info = [i for i in board_info if i != [""]] 

    # turning list of lists to list of strings
    board_info = [j for i in board_info for j in i]
    board_info = [i for i in board_info if i[0] != "#"]  # remove comments
    my_file.close()

    return board_info


def board_interpretor(board_information, verbose=False):
    '''
    This function interprets a list of input lines from read_bff_file() and
    creates a board for the lazor puzzle
    # Parameters 
        board_information: *list* *str*
            list of input lines (as strings) from .bff input file
     
    '''
    board_layout = []
    blocks = []
    lasers = []
    points = []
    tries = 0

    for each_line in board_information:  # find GRID START
        if each_line.lower() == "grid start":

            while tries < 1:
                for i in board_information:
                    if i.lower() == "grid stop":
                        print("ok!")
                        tries += 1
                        break

                    else:
                        board_layout.append(i.split())

        # account for numbers of available block types
        elif (each_line[0].lower() in ["a", "b", "c"] and
              each_line[2].isdigit()):

            if each_line in board_layout:
                pass
                # letters does not go in this list e.g: B o o
            else:
                blocks.append(each_line.replace(" ", ""))

        # account for laser positions and velocities
        elif each_line[0].lower() == "l":
            lasers.append(list(map(int, each_line.split()[1:])))

        # account for points that must be crossed to complete the puzzle
        elif each_line[0].lower() == "p":
            points.append(tuple(list(map(int, each_line.split()[1:]))))

    board_layout = board_layout[1:]  # Remove Grid start that was appended

    # initialize and populate playGrid
    playGrid = [["-" for col in range(2 * len(board_layout[0]) + 1)]
                for row in range(2 * len(board_layout) + 1)]

    for row in range(len(board_layout)):
        for col in range(len(board_layout[row])):
            playGrid[2 * row + 1][2 * col + 1] = board_layout[row][col]

    for i in points:
        playGrid[i[1]][i[0]] = "P"

    for i in lasers:
        playGrid[i[1]][i[0]] = "L"

    if verbose:
        print("blocks: " + f"{blocks}")
        print("lasers: " + f"{lasers}")
        print("points: " + f"{points}")
        print("board layout: " + f"{board_layout}")
        print("playGrid: ")
        for i in playGrid:
            print(i)
        print("\n")

    return board_layout, blocks, lasers, points, playGrid