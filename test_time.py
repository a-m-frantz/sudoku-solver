import os
import statistics
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


def test_time():
    """Time how long sudoku_solver takes to solve the same puzzle over multiple runs."""
    num_tests = 100
    print('#####################################')
    print('# Timing sudoku_solver over {} runs #'.format(num_tests))
    print('#####################################', end='\n\n')
    start_time = time.time()
    run_times = []
    with suppress_stdout():
        for _ in range(num_tests):
            t_start = time.time()
            sudoku_solver.main()
            t_end = time.time()
            run_times.append(t_end - t_start)
    end_time = time.time()

    total_time = end_time - start_time
    max_time = max(run_times)
    min_time = min(run_times)
    avg_time = sum(run_times) / len(run_times)
    std_dev = statistics.stdev(run_times)
    print('Total time = {0:.4f}'.format(total_time))
    print()
    print('Maximum runtime = {0:.4f}'.format(max_time))
    print('Minimum runtime = {0:.4f}'.format(min_time))
    print()
    print('Average runtime = {0:.4f}'.format(avg_time))
    print('Standard Deviation = {0:.4f}'.format(std_dev))


if __name__ == '__main__':
    test_time()
