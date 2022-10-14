import random
import numpy as np

#checks if a number is allowed to be on a specific index linewise
def check_line(grid, number, index):
    for i in range(9):
        if number == grid[index[0], i]:
            return False
    return True

#checks if a number is allowed to be on a specific index columnwise
def check_column(grid, number, index):
    for i in range(9):
        if number == grid[i, index[1]]:
            return False
    return True

#checks if a number is allowed to be on a specific index square wise
def check_square(grid, number, index):
    x0 = index[0]-index[0]%3
    x1 = index[1]-index[1]%3
    for i in range(3):
        for j in range(3):
            if number == grid[i+x0, j+x1]:
                return False
    return True

#using the three above, checks if a number is allowed on a specific index
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
    for i in range(9):
        for j in range(9):
            if grid[i,j] == 0:
                zeros.append((i,j))
    return zeros

#returns all the numbers that are allowed to be placed at a coordinate
def which_numbers(grid, index):
    possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for i in range(1,10):
        if not check_line(grid, i, index) or not check_column(grid, i, index) or not check_square(grid, i ,index):
            possible_numbers.remove(i)
    
    return possible_numbers


#recursive solution finder
def solve_sudoku(grid):

    #if there are no more empty places, we found a solution!
    zeros = find_zeros(grid)
    if zeros == []:
        return True
    
    #otherwise, we find the first empty index:
    index = zeros[0]

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

#a function to remove numbers from a full sudoku grid at random
#(for now without checking for uniqueness or even making sure the numbers are removed in a "nice" way)
def remove_numbers(grid, amount):
    while amount:
        r=random.randint(0,80)
        x=r//9
        y=r%9

        if grid[x,y] != 0:
            grid[x,y] = 0
            amount -= 1

#generate a sudoku of chosen difficulty
def make_me_a_sudoku(difficulty="random"):
    your_sudoku_sir = np.zeros((9,9), dtype=np.int8)
    solve_sudoku(your_sudoku_sir)

    if difficulty == "Easy":
        #n = 80
        n = random.randint(36,45)
    elif difficulty == "Intermediate":
        n = random.randint(32,35)
    elif difficulty == "Hard":
        n = random.randint(28,31)
    else:
        n = random.randint(28, 45)

    #yeah I know it's weird. I just did it the other way round. I want to keep n numbers, so I'm removing 81 - n
    amount = 81 - n
    remove_numbers(your_sudoku_sir, amount)
    return your_sudoku_sir



#some testing procedures
if __name__=="__main__":

    """
    #test on an empty grid
    empty_grid = np.zeros((9,9), dtype=np.int8)
    if solve_sudoku(empty_grid):
        print(empty_grid)
    else:
        print("Can't be solved...")

    grid = np.zeros((9,9), dtype=np.int0)
    solve_sudoku(grid)
    #print(grid)
    """

    """
    #generate a bunch of sudokus:
    sudokus={}
    for i in range(20):
        sudokus[i]=np.zeros((9,9), dtype=np.int8)

    for i in range(len(sudokus)):
        solve_sudoku(sudokus[i])
        print(sudokus[i])
    """

    print(make_me_a_sudoku("hard"))

