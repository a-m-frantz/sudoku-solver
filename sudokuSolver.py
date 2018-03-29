import time
import puzzle as pzl
import algorithm as alg


def read_file():
    while True:
        try:
            # infile_name = input('Puzzle file name: ')
            infile_name = 'hard3.txt'
            infile = open(infile_name)
            file_contents = infile.read()
            puzzle_list = [char for char in file_contents if char.isdigit or char == '.']
            puzzle_string = ''.join(puzzle_list)
            if len(puzzle_string) == 81:
                break
        except OSError:
            print('File not found. Please try again.')
        else:
            print('File in incorrect format.\nSee README for accepted puzzle formats.')
    print('Input file: ' + infile_name, end='\n\n')
    puzzle = pzl.Puzzle(puzzle_string)
    return puzzle


def main():
    puzzle = read_file()

    print('Starting puzzle:')
    puzzle.print_puzzle()
    print('Solving...', end='\n\n')

    t0 = time.time()
    alg.update_clue_peers(puzzle)
    alg.basic_solve(puzzle)
    if not puzzle.solved:
        print('Basic solving techniques weren\'t enough.\n'
              'Have to guess and check for remaining unsolved cells.\nThe puzzle so far is:')
        puzzle.print_puzzle()
        t1 = time.time()
        total_time = t1 - t0
        print('Time it took to solve up to guessing and checking: {0:.4f}'.format(total_time), end='\n\n')
        puzzle = alg.guess_and_check(puzzle)

    t1 = time.time()
    total_time = t1 - t0

    if puzzle.solved:
        print('Solved puzzle:')
    else:
        print('Something went wrong!\nThis is an incorrect solution:')
    puzzle.print_puzzle()
    print('Time to solve: {0:.4f}'.format(total_time))


if __name__ == '__main__':
    main()
