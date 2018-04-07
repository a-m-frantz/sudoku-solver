import time

import sudoku_solver


def validate_file(file):
    """Validate that the file exists and is a proper puzzle file.

    Preemptively perform all the checks that are done in the input loop of sudoku_solver.py.

    :param file: name of file to validate
    :return True if the file passes all checks, False if it fails
    """
    try:
        open_file = open(file)
        file_contents = open_file.read()
        puzzle_list = [char for char in file_contents if char.isdigit() or char == '.']
        puzzle_string = ''.join(puzzle_list)
        if len(puzzle_string) == 81:
            clues = [char for char in puzzle_string if char != '.' and char != '0']
            num_clues = len(clues)
            if num_clues >= 17:
                return True
            else:
                print('{} is an unsolvable puzzle. It has {} clues.\n'
                      'There are no valid sudoku puzzles with fewer than 17 clues.'.format(file, num_clues))
                return False
        else:
            print('{} in incorrect format.\nSee README.md for accepted puzzle formats.'.format(file))
            return False
    except OSError:
        print('File {} not found.'.format(file))
        return False


def main(file, num_tests):
    """Time how long sudoku_solver takes to solve a puzzle."""
    if not validate_file(file):
        return
    print('Timing {} over {} run(s)...'.format(file, num_tests))
    start_time = time.time()
    run_times = []
    for _ in range(num_tests):
        t_start = time.time()
        sudoku_solver.main(file, quiet=True)
        t_end = time.time()
        run_times.append(t_end - t_start)
    end_time = time.time()

    total_time = end_time - start_time
    print('Total time = {0:.4f}'.format(total_time))
    if len(run_times) > 1:
        max_time = max(run_times)
        min_time = min(run_times)
        avg_time = sum(run_times) / len(run_times)
        print()
        print('Maximum runtime = {0:.4f}'.format(max_time))
        print('Minimum runtime = {0:.4f}'.format(min_time))
        print()
        print('Average runtime = {0:.4f}'.format(avg_time))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='File(s) with sudoku puzzle')
    parser.add_argument('-n', '--num-tests', type=int, default=20, help='Number of times to run solver, defaults to 20')
    arguments = parser.parse_args()
    if arguments.num_tests < 1:
        parser.error('num-tests must be greater than 0')

    for infile in arguments.input:
        print()
        main(infile, arguments.num_tests)
        print()
