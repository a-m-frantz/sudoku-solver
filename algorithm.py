import itertools

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_clue_regions(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle.cell_array[row][col].solved:
                val = puzzle.cell_array[row][col].last_candidate()
                update_regions(puzzle, row, col, val)
    return


# also handles naked singles recursively
def update_regions(puzzle, row, col, val, region=''):
    print('Removing {} from candidate lists of cell ({}, {})\'s {} buddies'.format(val, row, col, region))

    ### Rows ###
    if region == '' or region == 'row':
        for pos in ROW_ITER[row]:
            if pos[1] != col:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                if cell.solved:
                    continue
                cell.remove_candidate(val)
                if cell.solved:
                    print('Recursing in update_regions()')
                    update_regions(puzzle, pos[0], pos[1], cell.last_candidate())

    ### Columns ###
    if region == '' or region == 'column':
        for pos in COL_ITER[col]:
            if pos[0] != row:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                if cell.solved:
                    continue
                cell.remove_candidate(val)
                if cell.solved:
                    print('Recursing in update_regions()')
                    update_regions(puzzle, pos[0], pos[1], cell.last_candidate())

    ### Blocks ###
    if region == '' or region == 'block':
        rows, cols = [], []
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
                if cell.solved:
                    continue
                cell.remove_candidate(val)
                if cell.solved:
                    print('Recursing in update_regions()')
                    update_regions(puzzle, x_pos, y_pos, cell.last_candidate())


def find_preemptive_set(puzzle, n):
    for region_type_id, region_type in enumerate([ROW_ITER, COL_ITER, BLOCK_ITER]):
        for region in region_type:
            for preemptive_set in itertools.combinations(range(1, 9+1), n):
                cells = []
                for row, col in region:
                    cell = puzzle.cell_array[row][col]

                    # check that all candidates are in preemptive_set
                    if cell.solved or len(cell.candidates - set(preemptive_set)) != 0:
                        continue
                    if len(cells) < n:
                        cells.append(cell)
                    else:
                        cells.clear()
                        break
                if len(cells) == n:
                    print('Found a preemptive set!')
                    print('Set is: {}'.format(preemptive_set))
                    for cell in cells:
                        cell.print_cell()

                    region_list = ['row', 'column', 'block']
                    region_with_pair = region_list[region_type_id]
                    for cell in cells:
                        cell.dont_update = True
                    for cell, val in itertools.product(cells, preemptive_set):
                        update_regions(puzzle, cell.POS[0], cell.POS[1], val, region_with_pair)
                    for cell in cells:
                        cell.dont_update = False


def find_hidden_sets(puzzle, n):
    for region_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for region in region_type:
            for val_set in itertools.combinations(range(1, 9+1), n):
                val_set_matches = []
                for _ in range(n):
                    val_set_matches.append(set())
                cells = []
                for row, col in region:
                    cell = puzzle.cell_array[row][col]

                    # Check if one of the values is already solved
                    if cell.solved and cell.last_candidate() in val_set:
                        cells.clear()
                        break

                    if cell.solved or not any(val in cell.candidates for val in val_set):
                        continue

                    for val_index, val in enumerate(val_set):
                        if val in cell.candidates:
                            val_set_matches[val_index].add(cell)
                    if any(len(matches) > n for matches in val_set_matches):
                        cells.clear()
                        break

                    if len(cells) < n:
                        cells.append(cell)
                    else:
                        cells.clear()
                        break
                if len(cells) == n:
                    combined_candidates = set()
                    for cell in cells:
                        combined_candidates = combined_candidates | cell.candidates

                    # Check that found trip is hidden, not naked
                    if len(combined_candidates - set(val_set)) == 0:
                        continue

                    print('Found hidden set!')
                    print('Set is: {}'.format(val_set))
                    for cell in cells:
                        cell.print_cell()
                    for cell in cells:
                        cell.set_cell(set(val_set))

# def supposition(puzzle):

