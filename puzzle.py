import copy
import itertools

DIGITS = '123456789'

BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]


class SolutionError(Exception):
    """Exception thrown when a puzzle board becomes invalid."""
    pass


class Cell:
    """A single cell of a sudoku puzzle"""
    def __init__(self, row, col, val=DIGITS):
        """Initialize a cell.

        :param row: cell's row
        :param col: cell's column
        :param val: str of a clue's value, '123456789' for a cell with an unknown value
        """
        self.POS = (row, col)
        self._changed = False
        self.dont_remove = ''
        self.candidates = val
        if val != DIGITS:
            self._solved = True
            self._last_candidate = val
        else:
            self._solved = False
            self._last_candidate = None

    def __deepcopy__(self, memodict={}):
        """Make a deepcopy of a cell."""
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        result.POS = self.POS
        result._changed = False
        result.dont_remove = ''
        result.candidates = self.candidates
        result._solved = self._solved
        result._last_candidate = self._last_candidate
        return result

    def is_changed(self):
        """Return whether this cell has had it's candidate list changed."""
        return self._changed

    def is_solved(self):
        """Return whether this cell has been solved."""
        return self._solved

    def last_candidate(self):
        """Return this cell's solved value."""
        return self._last_candidate

    def remove_candidate(self, candidate):
        """Remove value from this cell's candidate list. Raise SolutionError if trying to remove the last candidate."""
        if candidate in self.candidates and candidate not in self.dont_remove:
            if self.is_solved():
                raise SolutionError()
            self.candidates = self.candidates.replace(candidate, '')
            self._changed = True
            candidates = self.candidates
            if len(candidates) == 1:
                self._solved = True
                self._last_candidate = candidates

    def set_cell(self, vals):
        """Set this cell's candidate list to the union of it's candidate list and the set of provided values."""
        new_candidates_list = [val for val in vals if val in self.candidates]  # don't add candidates already ruled out
        new_candidates = ''.join(new_candidates_list)
        if self.candidates == new_candidates:  # candidates already equal to new values
            return
        self.candidates = new_candidates
        self._changed = True
        candidates = self.candidates
        if len(candidates) == 1:
            self._solved = True
            self._last_candidate = candidates

    def print_cell(self):
        """Print this cell's position and candidate list for debugging."""
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
                self.cell_array[row].append(Cell(row, col, raw_puzzle[pos]))
            else:
                self.cell_array[row].append(Cell(row, col))
            pos += 1

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
        for row, col in itertools.product(range(9), repeat=2):
            cell = self.cell_array[row][col]
            if cell.is_changed():
                return True
        return False

    @changed.setter
    def changed(self, changed):
        # if changed being set to false, all cells _changed must be false
        if not changed:
            for row, col in itertools.product(range(9), repeat=2):
                cell = self.cell_array[row][col]
                cell._changed = changed
        # if changed being set to true, only one cell _changed must be true
        elif changed:
            self.cell_array[0][0]._changed = changed

    @property
    def solved(self):
        """Return True if puzzle is solved, False if not."""
        for row, col in itertools.product(range(9), repeat=2):
            if not self.cell_array[row][col].is_solved():
                return False
        try:
            self.check()
            return True
        except SolutionError:
            return False

    def check(self):
        """Return True if there are no mistakes in the puzzle, False if there are."""
        for unit_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
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
        for row, col in itertools.product(range(9), repeat=2):
            self.cell_array[row][col].print_cell()
