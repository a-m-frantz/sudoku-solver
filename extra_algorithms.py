import itertools

import algorithms as alg


def find_preemptive_sets(puzzle, n):
    """Find preemptive sets and remove them from the candidate lists of other cells in the unit.

    A preemptive set is a set of values, size 'n', that are the only possible values for a set of cells, size 'n',
    within the same unit.  Preemptive sets can be safely removed from any cell in the unit that could be a value not
    inside of the preemptive set.  Preemptive sets are often called naked sets.

    :param puzzle: Puzzle object
    :param n: size of preemptive sets to be found
    """
    for unit_type_id, unit_type in enumerate([alg.ROW_ITER, alg.COL_ITER, alg.BLOCK_ITER]):
        for unit in unit_type:
            for preemptive_tup in itertools.combinations(range(1, 9+1), n):
                preemptive_set = set(preemptive_tup)
                cells = []
                for row, col in unit:
                    cell = puzzle.cell_array[row][col]

                    # check that all candidates are in preemptive_set
                    if cell.is_solved() or len(cell.candidates - preemptive_set) != 0:
                        continue
                    if len(cells) < n:
                        cells.append(cell)
                    else:
                        cells.clear()
                        break
                if len(cells) == n:
                    unit_list = ['row', 'column', 'block']
                    unit_with_pair = unit_list[unit_type_id]
                    for cell in cells:
                        cell.dont_remove = preemptive_set
                    for cell, val in itertools.product(cells, preemptive_set):
                        alg.update_peers(puzzle, cell.POS[0], cell.POS[1], val, unit_with_pair)
                    for cell in cells:
                        cell.dont_remove = set()


def find_hidden_sets(puzzle, n):
    """Find hidden sets and remove other values from the cells' candidate lists.

    A hidden set is a set of values, size 'n', which only appear in the candidate lists of a set of cells, size 'n',
    within the same unit.  Every value that is not in the hidden set can be safely removed from that cell's
    candidate list.

    :param puzzle: Puzzle object
    :param n: size of hidden sets to be found
    """
    for unit_type in [alg.ROW_ITER, alg.COL_ITER, alg.BLOCK_ITER]:
        for unit in unit_type:
            for val_tup in itertools.combinations(range(1, 9+1), n):
                val_set = set(val_tup)
                val_set_matches = [set() for _ in range(n)]
                cells = []
                for row, col in unit:
                    cell = puzzle.cell_array[row][col]
                    cell_solved = cell.is_solved()

                    # Check if one of the values is already solved. If one is, break and look at next value set
                    if cell_solved and cell.last_candidate() in val_set:
                        cells.clear()
                        break

                    # If cell is solved or none of val_set appears in it's candidate list, continue to next cell
                    if cell_solved or len(val_set & cell.candidates) == 0:
                        continue

                    for val_index, val in enumerate(val_set):
                        if val in cell.candidates:
                            val_set_matches[val_index].add(cell)
                    # If a value appears in a greater number of cells than the size of the set, break
                    if any(len(matches) > n for matches in val_set_matches):
                        cells.clear()
                        break

                    # If more than n cells have matching values, this val_set is not hidden
                    if len(cells) >= n:
                        cells.clear()
                        break
                    else:
                        cells.append(cell)
                if len(cells) == n:
                    combined_candidates = set()
                    for cell in cells:
                        combined_candidates = combined_candidates | cell.candidates

                    # Check that found set is hidden, not naked
                    if len(combined_candidates - val_set) == 0:
                        continue
                    for cell in cells:
                        cell.set_cell(val_set)
                        if cell.is_solved():
                            alg.update_peers(puzzle, cell.POS[0], cell.POS[1], cell.last_candidate())


def _row_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for row, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_sub_units = []
        # A sub unit is columns [0-2], [3-5], or [6-8] of a row
        for sub_unit_index, sub_unit in enumerate(alg.BANDS):
            for col in sub_unit:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    # if value has been solved, break all loops until the outer val loop
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this sub unit. Don't care how many times it shows up, so don't check the rest.
                        val_in_sub_units.append(sub_unit_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one sub unit, go to next value
        if val_solved or len(val_in_sub_units) != 1:
            break
        sub_unit_num = val_in_sub_units[0]
        rows, cols = [], []
        # Find which horizontal band 'row' is in (horizontal in regards to whole puzzle)
        for horizontal_band in alg.BANDS:
            if row in horizontal_band:
                rows = horizontal_band[:]
                break
        rows.remove(row)
        cols = alg.BANDS[sub_unit_num]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                alg.update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _col_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for col, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_sub_units = []
        # A sub unit is rows [0-2], [3-5], or [6-8] of a column
        for sub_unit_index, sub_unit in enumerate(alg.BANDS):
            for row in sub_unit:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    # if value has been solved, break all loops until the outer val loop
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this sub unit. Don't care how many times it shows up, so don't check the rest.
                        val_in_sub_units.append(sub_unit_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one sub unit, go to next value
        if val_solved or len(val_in_sub_units) != 1:
            break
        sub_unit_num = val_in_sub_units[0]
        rows, cols = [], []
        # Find which vertical band 'col' is in (vertical in regards to whole puzzle)
        for vertical_band in alg.BANDS:
            if col in vertical_band:
                cols = vertical_band[:]
                break
        cols.remove(col)
        rows = alg.BANDS[sub_unit_num]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                alg.update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _horizontal_block_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for block_rows, block_cols, val in itertools.product(alg.BANDS, alg.BANDS, range(1, 9+1)):
        val_solved = False
        val_in_rows = []
        for row_index, row in enumerate(block_rows):
            for col in block_cols:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this row. Don't care how many times it shows up, so don't check the rest
                        val_in_rows.append(row_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one row, go to next block
        if val_solved or len(val_in_rows) != 1:
            break
        row_index = val_in_rows[0]
        row_to_update = block_rows[row_index]
        cols = []
        [[cols.append(col) for col in vertical_band
          if vertical_band != block_cols] for vertical_band in alg.BANDS]
        for col in cols:
            cell = puzzle.cell_array[row_to_update][col]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                alg.update_peers(puzzle, row_to_update, col, cell.last_candidate())


def _vertical_block_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for block_rows, block_cols, val in itertools.product(alg.BANDS, alg.BANDS, range(1, 9+1)):
        val_solved = False
        val_in_cols = []
        for col_index, col in enumerate(block_cols):
            for row in block_rows:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this col. Don't care how many times it shows up, so don't check the rest
                        val_in_cols.append(col_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one row, go to next block
        if val_solved or len(val_in_cols) != 1:
            break
        col_index = val_in_cols[0]
        col_to_update = block_cols[col_index]
        rows = []
        [[rows.append(row) for row in horizontal_band
          if horizontal_band != block_rows] for horizontal_band in alg.BANDS]
        for row in rows:
            cell = puzzle.cell_array[row][col_to_update]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                alg.update_peers(puzzle, row, col_to_update, cell.last_candidate())


def find_sub_unit_exclusions(puzzle):
    """Search each unit for values that only appear in one sub unit
    and remove them from the rest of the overlapping unit.

    :param puzzle: Puzzle object
    """
    _row_sub_unit_exclusions(puzzle)
    _col_sub_unit_exclusions(puzzle)
    _horizontal_block_sub_unit_exclusions(puzzle)
    _vertical_block_sub_unit_exclusions(puzzle)
