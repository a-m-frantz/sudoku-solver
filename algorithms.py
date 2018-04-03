import copy
import itertools

from puzzle import SolutionError

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_peers(puzzle, row, col, val, unit_type=''):
    """Remove a value from the candidate lists of a cell's peers.

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
    """Update the candidate lists of the clues' peers.  Clues are cells whose values are known when the puzzle starts.

    Only call after puzzle initialization.

    :param puzzle: Puzzle object
    """
    for row, col in itertools.product(range(9), range(9)):
        if puzzle.cell_array[row][col].is_solved():
            val = puzzle.cell_array[row][col].last_candidate()
            update_peers(puzzle, row, col, val)


def find_hidden_singles(puzzle):
    """Find hidden singles and remove other values from the cell's candidate lists to solve it.

    A hidden single is a value which only appears in the candidate list of one cell in a unit.

    :param puzzle: Puzzle object
    """
    for unit_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for unit in unit_type:
            for val in range(1, 9+1):
                potential_single = None
                for row, col in unit:
                    cell = puzzle.cell_array[row][col]
                    cell_solved = cell.is_solved()

                    # Check if the value is already solved. If it is, break and look at next value
                    if cell_solved and cell.last_candidate() == val:
                        break

                    if cell_solved or val not in cell.candidates:
                        continue

                    if not potential_single:
                        potential_single = cell
                    else:
                        potential_single = None
                        break

                if potential_single:
                    single = potential_single
                    single.set_cell({val})
                    update_peers(puzzle, single.POS[0], single.POS[1], single.last_candidate())


def _row_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for row, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_sub_units = []
        # A sub unit is columns [0-2], [3-5], or [6-8] of a row
        for sub_unit_index, sub_unit in enumerate(BANDS):
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
            continue
        sub_unit_num = val_in_sub_units[0]
        rows, cols = [], []
        # Find which horizontal band 'row' is in (horizontal in regards to whole puzzle)
        for horizontal_band in BANDS:
            if row in horizontal_band:
                rows = horizontal_band[:]
                break
        rows.remove(row)
        cols = BANDS[sub_unit_num]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _col_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for col, val in itertools.product(range(9), range(1, 9+1)):
        val_solved = False
        val_in_sub_units = []
        # A sub unit is rows [0-2], [3-5], or [6-8] of a column
        for sub_unit_index, sub_unit in enumerate(BANDS):
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
            continue
        sub_unit_num = val_in_sub_units[0]
        rows, cols = [], []
        # Find which vertical band 'col' is in (vertical in regards to whole puzzle)
        for vertical_band in BANDS:
            if col in vertical_band:
                cols = vertical_band[:]
                break
        cols.remove(col)
        rows = BANDS[sub_unit_num]
        for row_num, col_num in itertools.product(rows, cols):
            cell = puzzle.cell_array[row_num][col_num]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row_num, col_num, cell.last_candidate())


def _horizontal_block_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for block_rows, block_cols, val in itertools.product(BANDS, BANDS, range(1, 9+1)):
        val_solved = False
        val_in_rows = []
        for row in block_rows:
            for col in block_cols:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this row. Don't care how many times it shows up, so don't check the rest
                        val_in_rows.append(row)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one row, go to next val
        if val_solved or len(val_in_rows) != 1:
            continue
        row_to_update = val_in_rows[0]
        cols = []
        [[cols.append(col) for col in vertical_band
          if vertical_band != block_cols] for vertical_band in BANDS]
        for col in cols:
            cell = puzzle.cell_array[row_to_update][col]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row_to_update, col, cell.last_candidate())


def _vertical_block_sub_unit_exclusions(puzzle):
    """Private find_sub_unit_exclusions() function."""
    for block_rows, block_cols, val in itertools.product(BANDS, BANDS, range(1, 9+1)):
        val_solved = False
        val_in_cols = []
        for col in block_cols:
            for row in block_rows:
                cell = puzzle.cell_array[row][col]
                if val in cell.candidates:
                    if cell.is_solved():
                        val_solved = True
                        break
                    else:
                        # value is in this col. Don't care how many times it shows up, so don't check the rest
                        val_in_cols.append(col)
                        break
            if val_solved:
                break
        # If value is solved or appears in more than one row, go to next val
        if val_solved or len(val_in_cols) != 1:
            continue
        col_to_update = val_in_cols[0]
        rows = []
        [[rows.append(row) for row in horizontal_band
          if horizontal_band != block_rows] for horizontal_band in BANDS]
        for row in rows:
            cell = puzzle.cell_array[row][col_to_update]
            previously_solved = cell.is_solved()
            cell.remove_candidate(val)
            if cell.is_solved() and not previously_solved:
                update_peers(puzzle, row, col_to_update, cell.last_candidate())


def find_sub_unit_exclusions(puzzle):
    """Search each unit for values that only appear in one sub unit
    and remove them from the rest of the overlapping unit.

    :param puzzle: Puzzle object
    """
    _row_sub_unit_exclusions(puzzle)
    _col_sub_unit_exclusions(puzzle)
    _horizontal_block_sub_unit_exclusions(puzzle)
    _vertical_block_sub_unit_exclusions(puzzle)


def basic_solve(puzzle):
    """Solve puzzle using non-recursive techniques.

    :param puzzle: Puzzle object
    """
    while puzzle.changed:
        puzzle.changed = False

        find_hidden_singles(puzzle)
        puzzle.check()
        find_sub_unit_exclusions(puzzle)
        puzzle.check()


def guess_and_check(puzzle, recursed_into=False):
    """Solve puzzle by assigning a random valid value to unsolved cells and removing candidates which result in errors.

    :param puzzle: Puzzle object
    :param recursed_into: bool identifying this as a top level or recursive call
    :return: solved Puzzle object or None if puzzle still unsolved
    """
    # guess_and_check() is always called after basic_solve, which always exits with puzzle.changed == False
    puzzle.changed = True
    while puzzle.changed:
        puzzle.changed = False
        checked_cells = set()
        largest_set_length = 1
        largest_set_length_increased = True
        for min_set_length in range(2, 9):  # TODO comment what set_length variables are doing
            if not largest_set_length_increased and min_set_length > largest_set_length:
                break
            largest_set_length_increased = False
            for row, col in itertools.product(range(9), repeat=2):
                cell = puzzle.cell_array[row][col]
                if len(cell.candidates) > largest_set_length:
                    largest_set_length = len(cell.candidates)
                    largest_set_length_increased = True
                if not cell.is_solved() and len(cell.candidates) <= min_set_length and cell not in checked_cells:
                    checked_cells.add(cell)
                    bad_vals = set()
                    for val in cell.candidates:
                        # if all checked values are bad except last one, last value must be good unless in recursion
                        if len(cell.candidates - bad_vals) == 1 and not recursed_into:
                            break
                        puzzle_copy = copy.deepcopy(puzzle)
                        copied_cell = puzzle_copy.cell_array[row][col]
                        copied_cell.set_cell({val})
                        try:
                            update_peers(puzzle_copy, row, col, val)
                            basic_solve(puzzle_copy)
                            solved_puzzle = guess_and_check(puzzle_copy, recursed_into=True)
                            if solved_puzzle:
                                return solved_puzzle
                            else:
                                del solved_puzzle
                        except SolutionError:
                            bad_vals.add(val)
                    if (len(bad_vals)) > 0:
                        for val in bad_vals:
                            cell.remove_candidate(val)
                        if cell.is_solved():
                            update_peers(puzzle, cell.POS[0], cell.POS[1], cell.last_candidate())
                        basic_solve(puzzle)
                        if puzzle.solved:
                            return puzzle
    return None
