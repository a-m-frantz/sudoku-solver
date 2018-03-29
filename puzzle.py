import itertools
import copy


class SolutionError(Exception):
    """Exception thrown when a puzzle board becomes invalid."""
    pass


class Cell:
    """A single cell of a sudoku puzzle"""
    def __init__(self, row, col, val=None):
        """Initialize a cell.

        :param row: cell's row
        :param col: cell's column
        :param val: int of a clue's value, None for a cell with an unknown value
        """
        self.POS = (row, col)
        self._changed = False
        self.dont_remove = set()
        if val:
            self.candidates = {val}
            self._solved = True
            self._last_candidate = val
        else:
            self.candidates = {val for val in range(1, 9+1)}
            self._solved = False
            self._last_candidate = None

    def __deepcopy__(self, memodict={}):
        """Make a deepcopy of a cell."""
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        result.POS = self.POS
        result._changed = False
        result.dont_remove = set()
        result.candidates = copy.deepcopy(self.candidates)
        if len(result.candidates) == 1:
            result._solved = True
            result._last_candidate = next(iter(result.candidates))
        else:
            result._solved = False
            result._last_candidate = None
        return result

    def is_changed(self):
        """Return whether this cell has had it's candidate set changed."""
        return self._changed

    def is_solved(self):
        """Return whether this cell has been solved."""
        return self._solved

    def last_candidate(self):
        """Return this cell's solved value."""
        return self._last_candidate

    def remove_candidate(self, candidate):
        """Remove value from this cell's candidate set. Raise SolutionError if trying to remove the last candidate."""
        if candidate in self.candidates and candidate not in self.dont_remove:
            if self.is_solved():
                raise SolutionError()
            self.candidates.remove(candidate)
            self._changed = True
            if len(self.candidates) == 1:
                self._solved = True
                self._last_candidate = next(iter(self.candidates))

    def set_cell(self, val_set):
        """Set this cell's candidate set to the union of it's candidate set and the set of provided values."""
        new_candidates = self.candidates & val_set  # don't add candidates already ruled out
        if self.candidates == new_candidates:  # candidates already equal to new values
            return
        self.candidates = new_candidates
        self._changed = True
        if len(self.candidates) == 1:
            self._solved = True
            self._last_candidate = next(iter(self.candidates))

    def print_cell(self):
        """Print this cell's position and candidate set for debugging."""
        print('Cell: ({}, {})'.format(self.POS[0], self.POS[1]))
        print(self.candidates)


class Puzzle:
    """A sudoku puzzle."""
    def __init__(self, raw_puzzle):
        """Initialize the puzzle.

        :param raw_puzzle: 81 char string with '.' or '0' for unknown cells and 1-9 for clues.
                           First 9 chars are first row, second 9 chars are second row, etc.
        """
        self.cell_array = [[] for _ in range(9)]
        pos = 0
        num_clues = 0
        for row, col in itertools.product(range(9), repeat=2):
            if raw_puzzle[pos] != '.' and raw_puzzle[pos] != '0':
                num_clues += 1
                self.cell_array[row].append(Cell(row, col, int(raw_puzzle[pos])))
            else:
                self.cell_array[row].append(Cell(row, col))
            pos += 1
        # print('Number of clues: {}'.format(num_clues), end='\n\n')

    def __deepcopy__(self, memodict={}):
        """Make a deepcopy of a puzzle."""
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        result.cell_array = [[] for _ in range(9)]
        for row, col in itertools.product(range(9), repeat=2):
            result.cell_array[row].append(copy.deepcopy(self.cell_array[row][col], memodict))
        return result

    @property
    def changed(self):
        """Return True if any cell has been changed, False if none have."""
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                if cell.is_changed():
                    return True
        return False

    @changed.setter
    def changed(self, changed):
        # if changed being set to false, all cells _changed must be false
        if not changed:
            for row in range(9):
                for col in range(9):
                    cell = self.cell_array[row][col]
                    cell._changed = changed
        # if changed being set to true, only one cell _changed must be true
        elif changed:
            self.cell_array[0][0]._changed = changed

    @property
    def solved(self):
        """Return True if puzzle is solved, False if not."""
        for row in range(9):
            for col in range(9):
                if not self.cell_array[row][col].is_solved():
                    return False
        try:
            self.check()
            return True
        except SolutionError:
            return False

    def check(self):
        """Return True if there are no mistakes in the puzzle, False if there are."""
        bands = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        row_iter = [[(row, col) for col in range(9)] for row in range(9)]
        col_iter = [[(row, col) for row in range(9)] for col in range(9)]
        block_iter = [[(row, col) for row in rows for col in cols] for rows in bands for cols in bands]
        for unit_type in [row_iter, col_iter, block_iter]:
            for unit in unit_type:
                solved_vals = []
                for row, col in unit:
                    cell = self.cell_array[row][col]
                    if cell.is_solved():
                        solved_vals.append(cell.last_candidate())
                if len(solved_vals) != len(set(solved_vals)):
                    raise SolutionError()

    def print_puzzle(self):
        """Print the puzzle with unsolved cells as a '.', and solved cells as their value."""
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                if cell.is_solved():
                    print(cell.last_candidate(), end=' ')
                else:
                    print('.', end=' ')
                if col == 2 or col == 5:
                    print('|', end=' ')
            print()
            if row == 2 or row == 5:
                print('-' * 21)
        print()

    def print_all_candidates(self):
        """Print each cell's candidate set for debugging."""
        for row in range(9):
            for col in range(9):
                self.cell_array[row][col].print_cell()
