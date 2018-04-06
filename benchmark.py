import statistics
import time

import sudoku_solver


def main(args):
    """Time how long sudoku_solver takes to solve the same puzzle over multiple runs."""
    num_tests = args.num_tests
    print('Timing {} over {} runs...'.format(args.input, num_tests))
    start_time = time.time()
    run_times = []
    for _ in range(num_tests):
        t_start = time.time()
        with sudoku_solver.suppress_stdout():
            sudoku_solver.main(args.input)
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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='File(s) with sudoku puzzle')
    parser.add_argument('-n', '--num-tests', type=int, default=100, help='Number of times to run solver')
    arguments = parser.parse_args()
    if arguments.num_tests < 2:
        parser.error('num-tests must be greater than 1')
    main(arguments)
