import time

import algorithms as alg
import puzzle as pzl


class ClueError(Exception):
    """Exception thrown when a puzzle doesn't have enough clues, less than 17, to solve it."""
    def __init__(self, file_name, num_clues):
        self.file_name = file_name
        self.num_clues = num_clues


def parse_file(file_name):
    """Check that file has a puzzle with at least 17 clues and return the puzzle in string format if validated.

    :param file_name: name of file to check
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
            raise ClueError(file_name, num_clues)
    else:
        print('{} in incorrect format.\nSee README.md for accepted puzzle formats.'.format(file_name))
        return None


def read_file(file, check):
    """Get puzzle file from user, validate it, and return a Puzzle object and the name of the file the puzzle came from.

    :param file: name of file to check
    :param check: True if the user is only checking if the puzzle is solvable.
                  This suppresses the warning that the puzzle doesn't have enough clues.
    :return: Puzzle object and file name on success, (None, None) either on quit or when less than 17 clues
             and the --check flag was passed.
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
                print('User quit program.')
                return None, None
            puzzle_string = parse_file(file_name)
            if puzzle_string:
                break

        except ClueError as err:
            if check:
                print('{} is unsolvable'.format(err.file_name))
                return None, None  # quits run
            else:
                print('{} is an unsolvable puzzle. It has {} clues.\n'
                      'There are no valid sudoku puzzles with fewer than 17 clues.'
                      .format(err.file_name, err.num_clues))

        except OSError:
            print('File {} not found.'.format(file_name))

    puzzle = pzl.Puzzle(puzzle_string)
    return puzzle, file_name


def solve(puzzle):
    """Solve puzzle.

    :param puzzle: Puzzle object
    :return: None on an unsolvable puzzle, a solved Puzzle object, or an unsolved Puzzle object when there are
             multiple solutions to the puzzle
    """
    try:
        alg.update_clue_peers(puzzle)
        alg.basic_solve(puzzle)
        if not puzzle.solved:
            puzzle = alg.guess_and_check(puzzle)

    except pzl.SolutionError:
        puzzle = None

    return puzzle


def main(infile=None, check=False, quiet=False):
    puzzle, file_name = read_file(infile, check)
    if not puzzle:
        return  # user either quit program or the puzzle had less than 17 clues and the --check flag was passed.

    if not quiet and not check:
        print('Starting puzzle:')
        puzzle.print_puzzle()
        print('Solving...', end='\n\n')

    t0 = time.time()

    puzzle = solve(puzzle)

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
