import itertools

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_clue_regions(puzzle):
    print('Removing clues from candidate lists')
    for row in range(9):
        for col in range(9):
            if puzzle.cell_array[row][col].solved():
                val = puzzle.cell_array[row][col].last_candidate()
                update_regions(puzzle, row, col, val)
    print('Done removing clues from candidate lists', end='\n\n')
    puzzle.print_puzzle()
    return


# also handles naked singles recursively
def update_regions(puzzle, row, col, val):
    print('Removing {} from candidate lists of cell ({}, {})\'s buddies'.format(val, row, col))

    ### Rows ###
    for pos in ROW_ITER[row]:
        if pos[1] != col:
            cell = puzzle.cell_array[pos[0]][pos[1]]
            just_solved = cell.remove_candidate(val)
            if just_solved:
                print('Recursing in update_regions()')
                update_regions(puzzle, pos[0], pos[1], cell.last_candidate())

    ### Columns ###
    for pos in COL_ITER[col]:
        if pos[0] != row:
            cell = puzzle.cell_array[pos[0]][pos[1]]
            just_solved = cell.remove_candidate(val)
            if just_solved:
                print('Recursing in update_regions()')
                update_regions(puzzle, pos[0], pos[1], cell.last_candidate())

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
                update_regions(puzzle, x_pos, y_pos, cell.last_candidate())


def find_hidden_singles(puzzle):
    for region_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for region in region_type:
            for val in range(1, 9+1):
                only_occurrence = None
                for row, col in region:
                    cell = puzzle.cell_array[row][col]
                    if cell.solved() or val not in cell.candidates:
                        continue
                    if not only_occurrence:     # val has not occurred yet
                        only_occurrence = cell
                    else:                       # val has already occurred
                        only_occurrence = None
                        break
                if only_occurrence:
                    only_occurrence.solve(val)
                    update_regions(puzzle, only_occurrence.POS[0], only_occurrence.POS[1], val)


def find_pairs(puzzle):
    for region_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for region in region_type:
            for val_pair in itertools.combinations(range(1, 9+1), 2):
                cell_pair = []
                for row, col in region:
                    cell = puzzle.cell_array[row][col]
                    if cell.solved() or not all(candidate in cell.candidates for candidate in val_pair):
                        continue
                    if len(cell_pair) < 2:
                        cell_pair.append(cell)
                    else:
                        cell_pair.clear()
                        break
                if len(cell_pair) == 2:
                    cell_pair[0].candidates = {'dummy'}
                    cell_pair[1].candidates = {'dummy'}
                    for cell in cell_pair:
                        update_regions(puzzle, cell.POS[0], cell.POS[1], val_pair[0])
                        update_regions(puzzle, cell.POS[0], cell.POS[1], val_pair[1])
                    cell_pair[0].candidates = set(val_pair)
                    cell_pair[1].candidates = set(val_pair)


def find_triples(puzzle):
    for region_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for region in region_type:
            for val_trip in itertools.combinations(range(1, 9+1), 3):
                cell_trip = []
                for row, col in region:
                    cell = puzzle.cell_array[row][col]
                    if cell.solved() or len(set(val_trip) & cell.candidates) < 2:
                        continue
                    if len(cell_trip) < 3:
                        cell_trip.append(cell)
                    else:
                        cell_trip.clear()
                        break
                if len(cell_trip) == 3:
                    for cell in cell_trip:
                        cell.candidates = {'dummy'}
                    for cell, val in itertools.product(cell_trip, val_trip):
                        update_regions(puzzle, cell.POS[0], cell.POS[1], val)
                    for cell in cell_trip:
                        cell.candidates = set(val_trip)
