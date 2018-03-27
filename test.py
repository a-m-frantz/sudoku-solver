import sudokuSolver
import time
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
    print('#############################################################')
    print('Timing sudokuSolver over {} runs.'.format(num_tests))
    print('#############################################################', end='\n\n')
    run_times = []
    with suppress_stdout():
        for _ in range(num_tests):
            t_start = time.time()
            sudokuSolver.main()
            t_end = time.time()
            run_times.append(t_end - t_start)
    avg_time = sum(run_times) / len(run_times)
    print('Average runtime = {}'.format(avg_time))


if __name__ == '__main__':
    test()
