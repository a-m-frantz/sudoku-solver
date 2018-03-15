import itertools
import copy
from puzzle import SolutionError

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


def update_clue_peers(puzzle):
    for row, col in itertools.product(range(9), range(9)):
        if puzzle.cell_array[row][col].solved:
            val = puzzle.cell_array[row][col].last_candidate()
            update_peers(puzzle, row, col, val)


# also handles naked singles recursively
def update_peers(puzzle, row, col, val, unit_type=''):
    ### Rows ###
    if unit_type == '' or unit_type == 'row':
        for pos in ROW_ITER[row]:
            if pos[1] != col:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                previously_solved = cell.solved
                cell.remove_candidate(val)
                if cell.solved and not previously_solved:
                    update_peers(puzzle, pos[0], pos[1], cell.last_candidate())

    ### Columns ###
    if unit_type == '' or unit_type == 'column':
        for pos in COL_ITER[col]:
            if pos[0] != row:
                cell = puzzle.cell_array[pos[0]][pos[1]]
                previously_solved = cell.solved
                cell.remove_candidate(val)
                if cell.solved and not previously_solved:
                    update_peers(puzzle, pos[0], pos[1], cell.last_candidate())

    ### Blocks ###
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
            previously_solved = cell.solved
            cell.remove_candidate(val)
            if cell.solved and not previously_solved:
                update_peers(puzzle, x_pos, y_pos, cell.last_candidate())


def find_preemptive_set(puzzle, n):
    for unit_type_id, unit_type in enumerate([ROW_ITER, COL_ITER, BLOCK_ITER]):
        for unit in unit_type:
            for preemptive_set in itertools.combinations(range(1, 9+1), n):
                cells = []
                for row, col in unit:
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
                    unit_list = ['row', 'column', 'block']
                    unit_with_pair = unit_list[unit_type_id]
                    for cell in cells:
                        cell.dont_remove = preemptive_set
                    for cell, val in itertools.product(cells, preemptive_set):
                        update_peers(puzzle, cell.POS[0], cell.POS[1], val, unit_with_pair)
                    for cell in cells:
                        cell.dont_remove = set()


def find_hidden_sets(puzzle, n):
    for unit_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
        for unit in unit_type:
            for val_set in itertools.combinations(range(1, 9+1), n):
                val_set_matches = [set() for _ in range(n)]
                cells = []
                for row, col in unit:
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
                    for cell in cells:
                        cell.set_cell(set(val_set))


def basic_solve(puzzle):
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
    puzzle.changed = True


def supposition(puzzle, recursed_into=False):
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
                    if not cell.solved and len(cell.candidates) <= min_set_length and cell not in checked_cells:
                        checked_cells.add(cell)
                        bad_vals = set()
                        for val in cell.candidates:
                            # if all checked values are bad except last one, last value must be good unless in recursion
                            if len(cell.candidates - set(bad_vals)) == 1 and not recursed_into:
                                break
                            puzzle_copy = copy.deepcopy(puzzle)
                            copied_cell = puzzle_copy.cell_array[row][col]
                            copied_cell.set_cell({val})
                            try:
                                basic_solve(puzzle_copy)
                                try:
                                    supposition(puzzle_copy, recursed_into=True)
                                except SolutionError:
                                    bad_vals.add(val)
                            except SolutionError:
                                bad_vals.add(val)
                        if recursed_into and len(cell.candidates - set(bad_vals)) == 0:
                            raise SolutionError()
                        if (len(bad_vals)) > 0:
                            for val in bad_vals:
                                cell.remove_candidate(val)
                            basic_solve(puzzle)
                            if puzzle.solved:
                                return
    puzzle.changed = True
