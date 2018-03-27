import sudokuSolver
import time
import statistics
from contextlib import contextmanager
import sys
import os


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def test():
    num_tests = 10
    print('####################################')
    print('# Timing sudokuSolver over {} runs #'.format(num_tests))
    print('####################################', end='\n\n')
    start_time = time.time()
    run_times = []
    with suppress_stdout():
        for _ in range(num_tests):
            t_start = time.time()
            sudokuSolver.main()
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
    test()
