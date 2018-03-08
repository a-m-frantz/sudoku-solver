class Cell:
    def __init__(self, row, col, val=None):
        self.POS = (row, col)
        if val:
            self.candidates = {val}
        else:
            self.candidates = {val for val in range(1, 10)}

    def remove_candidates(self, candidates):
        self.candidates.remove(candidates)

    def print_cell(self):
        print('Cell: ({}, {})'.format(self.POS[0], self.POS[1]))
        print(self.candidates)


class Region:
    def __init__(self, cells):
        self.cells = cells

    def remove_digits(self, digits):
        return

    def update(self):
        return


class Puzzle:
    def __init__(self, raw_puzzle):
        self.candidates_array = []
        pos = 0
        for row in range(9):
            self.candidates_array.append([])
            for col in range(9):
                if raw_puzzle[pos] != '.':
                    self.candidates_array[row].append(Cell(row, col, int(raw_puzzle[pos])))
                else:
                    self.candidates_array[row].append(Cell(row, col))
                pos += 1

    def print_all_candidates(self):
        for row in range(9):
            for col in range(9):
                self.candidates_array[row][col].print_cell()
