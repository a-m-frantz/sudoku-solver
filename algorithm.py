BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_clue_regions(puzzle):
    for row in range(9):
        for col in range(9):
            if len(puzzle.cell_array[row][col].candidates) == 1:
                val = next(iter(puzzle.cell_array[row][col].candidates))
                update_regions(puzzle, row, col, val)
    return


def update_regions(puzzle, row, col, val):
    print('Removing {} from candidate lists of cell ({}, {})\'s buddies'.format(val, row, col))
    for cell in ROW_ITER[row]:
        if cell[1] != col:
            puzzle.cell_array[cell[0]][cell[1]].remove_candidate(val)
    for cell in COL_ITER[col]:
        if cell[0] != row:
            puzzle.cell_array[cell[0]][cell[1]].remove_candidate(val)

