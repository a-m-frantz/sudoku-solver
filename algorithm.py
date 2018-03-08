BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_clue_regions(puzzle):
    print('Removing clues from candidate lists')
    for row in range(9):
        for col in range(9):
            if puzzle.cell_array[row][col].solved:
                val = puzzle.cell_array[row][col].last_candidate
                update_regions(puzzle, row, col, val)
    print('Done removing clues from candidate lists', end='\n\n')
    puzzle.print_puzzle()
    return


def update_regions(puzzle, row, col, val):
    print('Removing {} from candidate lists of cell ({}, {})\'s buddies'.format(val, row, col))

    ### Rows ###
    for pos in ROW_ITER[row]:
        if pos[1] != col:
            cell = puzzle.cell_array[pos[0]][pos[1]]
            just_solved = cell.remove_candidate(val)
            if just_solved:
                print('Recursing in update_regions()')
                update_regions(puzzle, pos[0], pos[1], cell.last_candidate)

    ### Columns ###
    for pos in COL_ITER[col]:
        if pos[0] != row:
            cell = puzzle.cell_array[pos[0]][pos[1]]
            just_solved = cell.remove_candidate(val)
            if just_solved:
                print('Recursing in update_regions()')
                update_regions(puzzle, pos[0], pos[1], cell.last_candidate)

    ### Blocks ###
    for horiz_band in BANDS:
        if row in horiz_band:
            rows = horiz_band[:]
    for vert_band in BANDS:
        if col in vert_band:
            cols = vert_band[:]
    # 4 of the cells in the block were updated with the row and column. Don't update again
    rows.remove(row)
    cols.remove(col)
    for x_pos in rows:
        for y_pos in cols:
            cell = puzzle.cell_array[x_pos][y_pos]
            just_solved = cell.remove_candidate(val)
            if just_solved:
                print('Recursing in update_regions()')
                update_regions(puzzle, x_pos, y_pos, cell.last_candidate)
