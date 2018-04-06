import os
import sys
import time
from contextlib import contextmanager

import algorithms as alg
import puzzle as pzl


@contextmanager
def suppress_stdout():
    """Suppress stdout."""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


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
        print('File in incorrect format.\nSee README for accepted puzzle formats.')
        return None


def read_file(file=None):
    """Get puzzle file from user, validate it, and return a Puzzle object."""
    while True:
        try:
            if not file:
                print('Type "exit" at the prompt to quit.')
                infile_name = input('Puzzle file name: ')
            else:
                infile_name = file
                file = None
            # infile_name = 'sample_puzzles/hard3.txt'
            if infile_name == 'exit':
                sys.exit('User quit program.')
            infile = open(infile_name)
            file_contents = infile.read()
            puzzle_string = parse_file(file_contents)
            if puzzle_string:
                break
        except OSError:
            print('File not found. Please try again.')
    print('Input file: ' + infile_name, end='\n\n')
    puzzle = pzl.Puzzle(puzzle_string)
    return puzzle


def main(infile=None):
    puzzle = read_file(infile)

    print('Starting puzzle:')
    puzzle.print_puzzle()
    print('Solving...', end='\n\n')

    t0 = time.time()
    alg.update_clue_peers(puzzle)
    alg.basic_solve(puzzle)
    if not puzzle.solved:
        puzzle = alg.guess_and_check(puzzle)

    t1 = time.time()
    total_time = t1 - t0

    if puzzle.solved:
        print('Solved puzzle:')
        puzzle.print_puzzle()
        print('Time to solve: {0:.4f}'.format(total_time))
    else:
        print('This puzzle doesn\'t have a solution!')
        print('Time it took to realize this: {0:.4f}'.format(total_time))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', help='File with sudoku puzzle')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run without printing to stdout')
    arguments = parser.parse_args()
    if arguments.quiet:
        with suppress_stdout():
            for input_file in arguments.input:
                main(input_file)
    else:
        for input_file in arguments.input:
            main(input_file)
