import copy
import itertools

from puzzle import SolutionError, DIGITS, BANDS, ROW_ITER, COL_ITER, BLOCK_ITER


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
        for inner_row, inner_col in ROW_ITER[row]:
            if inner_col != col:
                cell = puzzle.cell_array[inner_row][inner_col]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, inner_row, inner_col, cell.last_candidate())

    # Columns #
    if unit_type == '' or unit_type == 'column':
        for inner_row, inner_col in COL_ITER[col]:
            if inner_row != row:
                cell = puzzle.cell_array[inner_row][inner_col]
                previously_solved = cell.is_solved()
                cell.remove_candidate(val)
                if cell.is_solved() and not previously_solved:
                    update_peers(puzzle, inner_row, inner_col, cell.last_candidate())

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
            for val in DIGITS:
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
                    else:  # more than one cell can be val. break to next value
                        potential_single = None
                        break

                if potential_single:
                    single = potential_single
                    single.set_cell(val)
                    update_peers(puzzle, single.POS[0], single.POS[1], single.last_candidate())


def basic_solve(puzzle):
    """Solve puzzle using a non-recursive technique, finding hidden singles.

    :param puzzle: Puzzle object
    """
    while puzzle.changed:
        puzzle.changed = False

        find_hidden_singles(puzzle)
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
        longest_list = 1
        # min_list_length is used to begin guessing and checking on cells with the smallest candidate lists
        for min_list_length in range(2, 9+1):
            # Efficient way to check if all cells have been checked
            # Largest list length will have been found after first pass through when min_list_length == 2
            if min_list_length > longest_list and min_list_length > 2:
                break
            for row, col in itertools.product(range(9), repeat=2):
                cell = puzzle.cell_array[row][col]
                list_length = len(cell.candidates)
                if list_length > longest_list:
                    longest_list = len(cell.candidates)
                if not cell.is_solved() and list_length <= min_list_length and cell not in checked_cells:
                    checked_cells.add(cell)
                    bad_vals = ''
                    for val in cell.candidates:
                        # if all checked values are bad except last one, last value must be good unless in recursion
                        if not recursed_into and list_length - len(bad_vals) == 1:
                            break
                        puzzle_copy = copy.deepcopy(puzzle)
                        copied_cell = puzzle_copy.cell_array[row][col]
                        copied_cell.set_cell(val)
                        try:
                            update_peers(puzzle_copy, row, col, val)
                            basic_solve(puzzle_copy)
                            solved_puzzle = guess_and_check(puzzle_copy, recursed_into=True)
                            # guess_and_check returns None if the puzzle wasn't solved
                            if solved_puzzle:
                                return solved_puzzle
                        except SolutionError:
                            bad_vals += val
                    if len(bad_vals) > 0:
                        for val in bad_vals:
                            cell.remove_candidate(val)
                        if cell.is_solved():
                            update_peers(puzzle, cell.POS[0], cell.POS[1], cell.last_candidate())
                        basic_solve(puzzle)
                        if puzzle.solved:
                            return puzzle
    return None
