class Cell:
    def __init__(self, row, col, val=None):
        self.POS = (row, col)
        if val:
            self.candidates = {val}
        else:
            self.candidates = {val for val in range(1, 10)}

    def remove_candidates(self, candidates):
        self.candidates.remove(candidates)


class Region:
    def __init__(self, cells):
        self.cells = cells

    def remove_digits(self, digits):
        return

    def update(self):
        return


class Puzzle:
    def __init__(self, puzzle):
        # candidates_array = [[range(1, 10) for col in range(9)] for row in range(9)]
        self.candidates_array = []
        pos = 0
        for row in range(9):
            self.candidates_array.append([])
            for col in range(9):
                self.candidates_array[row].append([])
                if puzzle[pos] != '.':
                    # candidates_array[row][col] = [int(puzzle[pos])]
                    self.candidates_array[row][col].append(Cell(row, col, int(puzzle[pos])))
                else:
                    self.candidates_array[row][col].append(Cell(row, col))
                pos += 1

        print(self.candidates_array)
