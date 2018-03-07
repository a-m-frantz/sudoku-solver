def read_file():
    # infile_name = input('Puzzle file name: ')
    infile_name = 'test1.txt'
    print('Input file: ' + infile_name, end='\n\n')
    infile = open(infile_name)
    puzzle = infile.read()
    return puzzle


def generate_candidates(puzzle):
    candidates_array = [[range(1, 10) for col in range(9)] for row in range(9)]
    pos = 0
    for row in range(9):
        for col in range(9):
            if puzzle[pos] != '.':
                candidates_array[row][col] = [int(puzzle[pos])]
            pos += 1

    return candidates_array
