class Cell:
    def __init__(self, row, col, val=None):
        self.POS = (row, col)
        if val:
            self.candidates = {val}
        else:
            self.candidates = {val for val in range(1, 10)}

    @property
    def solved(self):
        if len(self.candidates) == 1:
            return True
        else:
            return False

    def remove_candidate(self, candidate):
        if candidate in self.candidates:
            self.candidates.remove(candidate)
            self.print_cell()
            if self.solved:
                print('Cell ({}, {}) is {}!'.format(self.POS[0], self.POS[1], self.last_candidate))
                return True
        return False

    @property
    def last_candidate(self):
        if self.solved:
            return next(iter(self.candidates))
        # TODO throw some sort of error

    def print_cell(self):
        print('Cell: ({}, {})'.format(self.POS[0], self.POS[1]))
        print(self.candidates)


class Puzzle:
    def __init__(self, raw_puzzle):
        self.cell_array = []
        pos = 0
        for row in range(9):
            self.cell_array.append([])
            for col in range(9):
                if raw_puzzle[pos] != '.':
                    self.cell_array[row].append(Cell(row, col, int(raw_puzzle[pos])))
                else:
                    self.cell_array[row].append(Cell(row, col))
                pos += 1

    def print_puzzle(self):
        for row in range(9):
            for col in range(9):
                cell = self.cell_array[row][col]
                if cell.solved:
                    print(cell.last_candidate, end=' ')
                else:
                    print('.', end=' ')
                if col == 2 or col == 5:
                    print('|', end=' ')
            print()
            if row == 2 or row == 5:
                print('-' * 21)
        print('\n\n', end='')

    def print_all_candidates(self):
        for row in range(9):
            for col in range(9):
                self.cell_array[row][col].print_cell()
