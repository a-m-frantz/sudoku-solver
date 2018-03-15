BANDS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in BANDS for cols in BANDS]
# TODO find a way to avoid these global variables


class SolutionError(Exception):
    pass


class Cell:
    def __init__(self, row, col, val=None):
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

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, changed):
        self._changed = changed

    @property
    def solved(self):
        return self._solved

    def last_candidate(self):
        return self._last_candidate

    def remove_candidate(self, candidate):
        if candidate in self.candidates and candidate not in self.dont_remove:
            if self.solved:
                raise SolutionError()
            self.candidates.remove(candidate)
            self.changed = True
            if len(self.candidates) == 1:
                self._solved = True
                self._last_candidate = next(iter(self.candidates))

    def set_cell(self, val_set):
        if val_set == self.candidates:  # candidates already equal to new values
            return
        self.candidates = self.candidates & val_set
        self.changed = True
        if len(self.candidates) == 1:
            self._solved = True
            self._last_candidate = next(iter(self.candidates))

    def print_cell(self):
        print('Cell: ({}, {})'.format(self.POS[0], self.POS[1]))
        print(self.candidates)


class Puzzle:
    def __init__(self, raw_puzzle):
        self.cell_array = []
        pos = 0
        num_clues = 0
        for row in range(9):
            self.cell_array.append([])
            for col in range(9):
                if raw_puzzle[pos] != '.':
                    num_clues += 1
                    self.cell_array[row].append(Cell(row, col, int(raw_puzzle[pos])))
                else:
                    self.cell_array[row].append(Cell(row, col))
                pos += 1
        print('Number of clues: {}'.format(num_clues), end='\n\n')

    @property
    def changed(self):
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                if cell.changed:
                    return True
        return False

    @changed.setter
    def changed(self, changed):
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                cell.changed = changed

    @property
    def solved(self):
        for row in range(9):
            for col in range(9):
                if not self.cell_array[row][col].solved:
                    return False
        try:
            self.check()
            return True
        except SolutionError:
            return False

    def check(self):
        for region_type in [ROW_ITER, COL_ITER, BLOCK_ITER]:
            for region in region_type:
                solved_vals = []
                for row, col in region:
                    cell = self.cell_array[row][col]
                    if cell.solved:
                        solved_vals.append(cell.last_candidate())
                if len(solved_vals) != len(set(solved_vals)):
                    raise SolutionError()

    def print_puzzle(self):
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                if cell.solved:
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
        for row in range(9):
            for col in range(9):
                self.cell_array[row][col].print_cell()
