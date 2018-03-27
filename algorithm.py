import itertools
import copy
from puzzle import SolutionError

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_peers(puzzle, row, col, val, unit_type=''):
    """
    Remove a value from the candidate lists of a cell's peers.

    If removing a candidate solves a cell, recursively update that cell's peers.

    :param puzzle: Puzzle object
    :param row: int identifying the row the cell is in
    :param col: int identifying the column the cell is in
    :param val: The value that needs to be removed from the cell's peers
    :param unit_type: Optional str argument to only update one of the cell's units. Either 'row', 'column', or 'block'
    """
    # Rows #
    if unit_type == '' or unit_type == 'row':
        for pos in ROW_ITER[row]:
            if pos[1] != col:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, pos[0], pos[1], cell.last_candidate())

    # Columns #
    if unit_type == '' or unit_type == 'column':
        for pos in COL_ITER[col]:
            if pos[0] != row:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, pos[0], pos[1], cell.last_candidate())

    # Blocks #
    if unit_type == '' or unit_type == 'block':
        rows, cols = [], []
        for horizontal_band in BANDS:
            if row in horizontal_band:
                rows = horizontal_band[:]
                break
        for vertical_band in BANDS:
            if col in vertical_band:
                cols = vertical_band[:]
                break
        # 4 of the cells in the block were updated with the row and column. Don't update again
        rows.remove(row)
        cols.remove(col)
        for x_pos, y_pos in itertools.product(rows, cols):
            cell = puzzle.cell_array[x_pos][y_pos]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, x_pos, y_pos, cell.last_candidate())


def update_clue_peers(puzzle):
    """
    Update the candidate lists of the clues' peers.  Clues are cells whose values are known when the puzzle starts.

    Only call after puzzle initialization.

    :param puzzle: Puzzle object
    """
    for row, col in itertools.product(range(9), range(9)):
        if puzzle.cell_array[row][col].is_solved():
            val = puzzle.cell_array[row][col].last_candidate()
            update_peers(puzzle, row, col, val)


def find_preemptive_set(puzzle, n):
    """
    Find preemptive sets and remove them from the candidate lists of other cells in the unit.

    A preemptive set is a set of values, size 'n', that are the only possible values for a set of cells, size 'n',
    within the same unit.  Preemptive sets can be safely removed from any cell in the unit that could be a value not
    inside of the preemptive set.  Preemptive sets are often called naked sets.

    :param puzzle: Puzzle object
    :param n: size of preemptive sets to be found
    """
    for unit_type_id, unit_type in enumerate([ROW_ITER, COL_ITER, BLOCK_ITER]):
        for unit in unit_type:
            for preemptive_set in itertools.combinations(range(1, 9+1), n):
                cells = []
                for row, col in unit:
                    cell = puzzle.cell_array[row][col]

                    # check that all candidates are in preemptive_set
                    if cell.is_solved() or len(cell.candidates - set(preemptive_set)) != 0:  # TODO try speeding this up
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
                        update_peers(puzzle, cell.POS[0], cell.POS[1], val, unit_with_pair)
                    for cell in cells:
                        cell.dont_remove = set()


def find_hidden_sets(puzzle, n):
    """
    Find hidden sets and remove other values from the cells' candidate lists.

    A hidden set is a set of values, size 'n', which only appear in the candidate lists of a set of cells, size 'n',
    within the same unit.  Every value that is not in the hidden set can be safely removed from that cell's
    candidate list.

    :param puzzle: Puzzle object
    :param n: size of hidden sets to be found
    """
    for unit_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for unit in unit_type:
            for val_tup in itertools.combinations(range(1, 9+1), n):
                val_set = set(val_tup)
                val_set_matches = [set() for _ in range(n)]
                cells = []
                for row, col in unit:
                    cell = puzzle.cell_array[row][col]

                    # Check if one of the values is already solved. If one is, break and look at next value set
                    if cell.is_solved() and cell.last_candidate() in val_set:
                        cells.clear()
                        break

                    # If cell is solved or none of val_set appears in it's candidate list, continue to next cell
                    if cell.is_solved() or len(val_set & cell.candidates) == 0:
                        continue

                    for val_index, val in enumerate(val_set):
                        if val in cell.candidates:
                            val_set_matches[val_index].add(cell)
                    # If a value appears in a greater number of cells than the size of the set, break
                    if any(len(matches) > n for matches in val_set_matches):
                        cells.clear()
                        break

                    # If more than n cells have matching values, this val_set is not hidden
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
                    if len(combined_candidates - val_set) == 0:
                        continue
                    for cell in cells:
                        cell.set_cell(val_set)
                        if cell.is_solved():
                            update_peers(puzzle, cell.POS[0], cell.POS[1], cell.last_candidate())


def _overlap_rows(puzzle):
    for row, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_bands = []
        # band is vertical in regards to whole puzzle. Contents of vertical_band are columns on same row
        for band_index, vertical_band in enumerate(BANDS):
            for col in vertical_band:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    # if value has been solved, break all loops until outer val loop
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this vertical band. Don't care how many times it shows up, so don't check the rest
                        val_in_bands.append(band_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one band, go to next value
        if val_solved or len(val_in_bands) != 1:
            break
        vertical_band_index = val_in_bands[0]
        rows, cols = [], []
        # Find which horizontal band 'row' is in (horizontal in regards to whole puzzle)
        for horizontal_band in BANDS:
            if row in horizontal_band:
                rows = horizontal_band[:]
                break
        rows.remove(row)
        cols = BANDS[vertical_band_index]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _overlap_cols(puzzle):
    for col, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_bands = []
        # band is horizontal in regards to whole puzzle. Contents of horizontal_band are columns on same row
        for band_index, horizontal_band in enumerate(BANDS):
            for row in horizontal_band:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    # if value has been solved, break all loops until outer val loop
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # val is in this horizontal band. Don't care how many times it shows up, so don't check the rest
                        val_in_bands.append(band_index)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one band, go to next value
        if val_solved or len(val_in_bands) != 1:
            break
        horizontal_band_index = val_in_bands[0]
        rows, cols = [], []
        # Find which vertical band 'col' is in (vertical in regards to whole puzzle)
        for vertical_band in BANDS:
            if col in vertical_band:
                cols = vertical_band[:]
                break
        cols.remove(col)
        rows = BANDS[horizontal_band_index]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _overlap_blocks_horizontal(puzzle):
    for val in range(1, 9+1):
        for block_horizontal_band, block_vertical_band in itertools.product(BANDS, repeat=2):
            val_solved = False
            val_in_rows = []
            for row_index, row in enumerate(block_horizontal_band):
                for col in block_vertical_band:
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
            row_to_update = block_horizontal_band[row_index]
            cols = []
            [[cols.append(col) for col in vertical_band
              if vertical_band != block_vertical_band] for vertical_band in BANDS]
            for col in cols:
                cell = puzzle.cell_array[row_to_update][col]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, row_to_update, col, cell.last_candidate())


def _overlap_blocks_vertical(puzzle):
    for val in range(1, 9+1):
        for block_vertical_band, block_horizontal_band in itertools.product(BANDS, repeat=2):
            val_solved = False
            val_in_cols = []
            for col_index, col in enumerate(block_vertical_band):
                for row in block_horizontal_band:
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
            col_to_update = block_vertical_band[col_index]
            rows = []
            [[rows.append(row) for row in horizontal_band
              if horizontal_band != block_horizontal_band] for horizontal_band in BANDS]
            for row in rows:
                cell = puzzle.cell_array[row][col_to_update]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, row, col_to_update, cell.last_candidate())


def find_overlapping_units(puzzle):
    """
    Search each unit for values that only appear in one overlapping unit and remove that value from the other cells
    in the overlapping unit.

    :param puzzle: Puzzle object
    """
    _overlap_rows(puzzle)
    _overlap_cols(puzzle)
    _overlap_blocks_horizontal(puzzle)
    _overlap_blocks_vertical(puzzle)


def basic_solve(puzzle):
    """
    Solve puzzle using non-recursive techniques.

    :param puzzle: Puzzle object
    """
    while puzzle.changed:
        puzzle.changed = False

        find_hidden_sets(puzzle, 1)
        puzzle.check()
        find_preemptive_set(puzzle, 2)
        puzzle.check()
        find_hidden_sets(puzzle, 2)
        puzzle.check()
        find_preemptive_set(puzzle, 3)
        puzzle.check()
        find_hidden_sets(puzzle, 3)
        puzzle.check()
        find_preemptive_set(puzzle, 4)
        puzzle.check()
        find_hidden_sets(puzzle, 4)
        puzzle.check()
        find_overlapping_units(puzzle)
        puzzle.check()


def guess_and_check(puzzle, recursed_into=False):
    """
    Solve puzzle by assigning a random valid value to unsolved cells and removing candidates which result in errors.

    :param puzzle: Puzzle object
    :param recursed_into: bool identifying this as a top level or recursive call
    """
    # guess_and_check() is always called after basic_solve, which always exits with puzzle.changed == False
    puzzle.changed = True
    while puzzle.changed:
        puzzle.changed = False
        checked_cells = set()
        largest_set_length = 1
        largest_set_length_increased = True
        for min_set_length in range(2, 9+1):
            if not largest_set_length_increased and min_set_length > largest_set_length:
                break
            largest_set_length_increased = False
            for row in range(9):
                for col in range(9):
                    cell = puzzle.cell_array[row][col]
                    if len(cell.candidates) > largest_set_length:
                        largest_set_length = len(cell.candidates)
                        largest_set_length_increased = True
                    if not cell.is_solved() and len(cell.candidates) <= min_set_length and cell not in checked_cells:
                        checked_cells.add(cell)
                        bad_vals = set()
                        for val in cell.candidates:
                            # if all checked values are bad except last one, last value must be good unless in recursion
                            if len(cell.candidates - set(bad_vals)) == 1 and not recursed_into:
                                break
                            puzzle_copy = copy.deepcopy(puzzle)
                            copied_cell = puzzle_copy.cell_array[row][col]
                            copied_cell.set_cell({val})
                            update_peers(puzzle_copy, row, col, val)
                            try:
                                basic_solve(puzzle_copy)
                                try:
                                    guess_and_check(puzzle_copy, recursed_into=True)
                                except SolutionError:
                                    bad_vals.add(val)
                            except SolutionError:
                                bad_vals.add(val)
                        if recursed_into and len(cell.candidates - set(bad_vals)) == 0:
                            raise SolutionError()
                        if (len(bad_vals)) > 0:
                            for val in bad_vals:
                                cell.remove_candidate(val)
                            if cell.is_solved():
                                update_peers(puzzle, cell.POS[0], cell.POS[1], cell.last_candidate())
                            basic_solve(puzzle)
                            if puzzle.solved:
                                return  # TODO find way to send solved puzzle up call stack
