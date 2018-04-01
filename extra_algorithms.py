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
