import os
import sys
import time
from contextlib import contextmanager

import sudoku_solver


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


def main(file, num_tests):
    """Time how long sudoku_solver takes to solve a puzzle."""
    print('Timing {} over {} run(s)...'.format(file, num_tests))
    start_time = time.time()
    run_times = []
    for _ in range(num_tests):
        t_start = time.time()
        with suppress_stdout():
            sudoku_solver.main(file)
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
    parser.add_argument('-n', '--num-tests', type=int, default=20, help='Number of times to run solver. '
                                                                        'Must be greater than 0')
    arguments = parser.parse_args()
    if arguments.num_tests < 1:
        parser.error('num-tests must be greater than 0')

    for infile in arguments.input:
        print()
        main(infile, arguments.num_tests)
        print()
