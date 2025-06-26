def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # return row, col tuple (None, None) if there is none
    
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    
    return None, None # if no spaces in the puzzle are empty (-1)

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess at the row/col of the ouzzle is a valid guess
    # returns True if is valid, False if not

    #check the rows
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    # check the columns
    col_vals = []
    # for i in range(9):
    #    col_vals.append(puzzle[i][col])
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    
    # check 3x3 square
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    
    return True # valid guess





def solve_soduku(puzzle):
    # solve sudoku using backtracking
    # our puzzle is a list of list, where each inner list is a row in the sudoku puzzle
    # return whether a solution exists
    # mutates puzzle to be the solution (if the solution exists)

    # step 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # step 1.1: if there's nowhere left, then we're done because we only allowed valid inputs
    if row is None:
        return True
    
    # step 2: if there is a place to put a number, then make a guess between 1 and 9

    for guess in range(1, 10):
        # step 3: check if this guess is valid
        if is_valid(puzzle, guess, row, col):
            # step 3.1: if this is valid, then place the guess on the puzzle
            puzzle[row][col] = guess
            # step 4 : recursively call our solver
            if solve_soduku(puzzle):
                return True
        # step 5: if not avlid OR if the guess does not solve the puzzle
        # then we need to reset the guess and try again
        puzzle[row][col] = -1
    # step 6: if none of the numbers between 1 and 9 don't work, then this puzzle is unsolvable
    return False