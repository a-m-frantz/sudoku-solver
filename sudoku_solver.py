import sys
import time

import algorithms as alg
import puzzle as pzl


class ClueError(Exception):
    """Exception thrown when a puzzle doesn't have enough clues, less than 17, to solve it."""
    def __init__(self, file_name):
        self.file_name = file_name


def parse_file(file_name, check):
    """Check that file has a puzzle with at least 17 clues and return the puzzle in string format if validated.

    :param file_name: name of file to check
    :param check: True if the user is only checking if the puzzle is solvable.
                  This suppresses the warning that the puzzle doesn't have enough clues.
    """
    infile = open(file_name)
    file_contents = infile.read()
    puzzle_list = [char for char in file_contents if char.isdigit() or char == '.']
    puzzle_string = ''.join(puzzle_list)
    if len(puzzle_string) == 81:
        clues = [char for char in puzzle_string if char != '.' and char != '0']
        num_clues = len(clues)
        if num_clues >= 17:
            return puzzle_string
        else:
            if not check:
                print('{} is an unsolvable puzzle. It has {} clues.\n'
                      'There are no valid sudoku puzzles with fewer than 17 clues.'.format(file_name, num_clues))
            raise ClueError(file_name)
    else:
        print('{} in incorrect format.\nSee README.md for accepted puzzle formats.'.format(file_name))
        return None


def read_file(file, check):
    """Get puzzle file from user, validate it, and return a Puzzle object and the name of the file the puzzle came from.

    :param file: name of file to check
    :param check: True if the user is only checking if the puzzle is solvable.
                  This suppresses the warning that the puzzle doesn't have enough clues.
    """
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
            puzzle_string = parse_file(file_name, check)
            if puzzle_string:
                break
        except OSError:
            print('File {} not found.'.format(file_name))
    puzzle = pzl.Puzzle(puzzle_string)
    return puzzle, file_name


def main(infile=None, check=False, quiet=False):
    while True:
        try:
            puzzle, file_name = read_file(infile, check)
            break
        except ClueError as err:
            if check:
                if not quiet:
                    print('{} is unsolvable'.format(err.file_name))
                return
            else:
                pass

    if not check and not quiet:
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

    if puzzle and puzzle.solved:
        if not check:
            print('Solved puzzle:')
            puzzle.print_puzzle()
            print('Time to solve: {0:.4f}'.format(total_time))
        else:
            print('{} is solvable'.format(file_name))
    else:
        if not check:
            print('This puzzle doesn\'t have a solution!')
            print('Time it took to realize this: {0:.4f}'.format(total_time))
        else:
            print('{} is unsolvable'.format(file_name))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='*', help='File(s) with sudoku puzzle')
    parser.add_argument('-c', '--check', action='store_true', help='Only check if the puzzle(s) are solvable')
    arguments = parser.parse_args()
    if arguments.input:
        for input_file in arguments.input:
            main(input_file, arguments.check)
    else:
        main(check=arguments.check)
