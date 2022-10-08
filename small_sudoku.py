import random
import numpy as np

#checks if a number is allowed to be on a specific index linewise
def check_line(grid, number, index):
    for i in range(4):
        if number == grid[index[0], i]:
            return False
    return True

#checks if a number is allowed to be on a specific index columnwise
def check_column(grid, number, index):
    for i in range(4):
        if number == grid[i, index[1]]:
            return False
    return True

#checks if a number is allowed to be on a specific index square wise
def check_square(grid, number, index):
    x0 = index[0]-index[0]%2
    x1 = index[1]-index[1]%2
    for i in range(2):
        for j in range(2):
            if number == grid[i+x0, j+x1]:
                return False
    return True

#using the three aboce, checks if a number is allowed on a specific index
def check_index(grid, number, index):
    if (not check_line(grid, number, index)) or (not check_column(grid, number, index)) or (not check_square(grid, number, index)):
        return False
    else:
        return True

#chooses a random cooridnate based on grid size
#note: randint works outer bounds included, which is why we need to subtract 1
def rand_coord(size):
    x0 = random.randint(0,size-1)
    x1 = random.randint(0,size-1)
    return((x0,x1))

#return a list of empty coordinates, return False if there are none
def find_zeros(grid):
    zeros=[]
    for i in range(4):
        for j in range(4):
            if grid[i,j] == 0:
                zeros.append((i,j))
    return zeros

#returns all the numbers that are allowed to be placed at a coordinate
def which_numbers(grid, index):
    possible_numbers = [1, 2, 3, 4]

    for i in range(1,5):
        if not check_line(grid, i, index) or not check_column(grid, i, index) or not check_square(grid, i ,index):
            possible_numbers.remove(i)
    
    return possible_numbers


#recursive solution finder
def solve_sudoku(grid):
    print(grid)

    #if there are no more empty places, we found a solution!
    zeros = find_zeros(grid)
    if zeros == []:
        return True
    
    #otherwise, we find a random empty index:
    index = random.choice(zeros)
    print(index)

    #find all legal numbers at the index
    legal_numbers = which_numbers(grid, index)

    #shuffle them to find random solutions (we also use this to generate Sudokus)
    random.shuffle(legal_numbers)

    for number in legal_numbers:
        #update grid with randomly chosen legal number
        grid[index] = number

        #try to solve with the updated grid
        if solve_sudoku(grid):
            return True

        #backtrack if failed
        grid[index] = 0

    return False


empty_grid = np.zeros((4,4), dtype=np.int8)

#test on an empty grid
if solve_sudoku(empty_grid):
    print(empty_grid)
else:
    print("Can't be solved...")

