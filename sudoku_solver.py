import sys
import time

import algorithms as alg
import puzzle as pzl


def parse_file(file_contents):
    """Validate that file has a puzzle with at least 17 clues and return the puzzle in string format if validated."""
    puzzle_list = [char for char in file_contents if char.isdigit() or char == '.']
    puzzle_string = ''.join(puzzle_list)
    if len(puzzle_string) == 81:
        clues = [char for char in puzzle_string if char != '.' and char != '0']
        num_clues = len(clues)
        if num_clues >= 17:
            return puzzle_string
        else:
            print('This is an unsolvable puzzle. It has {} clues.\n'
                  'There are no valid sudoku puzzles with fewer than 17 clues.'.format(num_clues))
            return None
    else:
        print('File in incorrect format.\nSee README.md for accepted puzzle formats.')
        return None


def read_file(file=None):
    """Get puzzle file from user, validate it, and return a Puzzle object."""
    while True:
        try:
            if not file:
                print('Type "exit" at the prompt to quit.')
                file_name = input('Puzzle file name: ')
            else:
                file_name = file
                file = None
            if file_name == 'exit':
                sys.exit('User quit program.')
            infile = open(file_name)
            file_contents = infile.read()
            puzzle_string = parse_file(file_contents)
            if puzzle_string:
                break
        except OSError:
            print('File {} not found. Please try again.'.format(file_name))
    puzzle = pzl.Puzzle(puzzle_string)
    return puzzle, file_name


def main(infile=None, validate=False, quiet=False):
    puzzle, file_name = read_file(infile)

    if not validate and not quiet:
        print('Starting puzzle:')
        puzzle.print_puzzle()
        print('Solving...', end='\n\n')

    t0 = time.time()
    try:
        alg.update_clue_peers(puzzle)
        alg.basic_solve(puzzle)
        if not puzzle.solved:
            puzzle = alg.guess_and_check(puzzle)
    except pzl.SolutionError:
        pass

    if quiet:
        return

    t1 = time.time()
    total_time = t1 - t0

    if puzzle.solved:
        if not validate:
            print('Solved puzzle:')
            puzzle.print_puzzle()
            print('Time to solve: {0:.4f}'.format(total_time))
        else:
            print('{} is solvable'.format(file_name))
    else:
        if not validate:
            print('This puzzle doesn\'t have a solution!')
            print('Time it took to realize this: {0:.4f}'.format(total_time))
        else:
            print('{} is unsolvable'.format(file_name))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', help='File with sudoku puzzle')
    parser.add_argument('-v', '--validate', action='store_true', help='Only check if the puzzle(s) are solvable')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run without printing to stdout')
    arguments = parser.parse_args()
    if arguments.input:
        for input_file in arguments.input:
            main(input_file, arguments.validate, arguments.quiet)
    else:
        main(validate=arguments.validate, quiet=arguments.quiet)
