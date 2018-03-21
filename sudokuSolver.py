import time
import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)

    print('Starting puzzle:')
    puzzle.print_puzzle()
    print('Solving...', end='\n\n')

    t0 = time.time()
    alg.update_clue_peers(puzzle)
    alg.basic_solve(puzzle)
    if not puzzle.solved:
        print('Basic solving techniques weren\'t enough.\n'
              'Have to use supposition for remaining unsolved cells\nThe puzzle so far is:')
        puzzle.print_puzzle()
        t1 = time.time()
        total_time = t1 - t0
        print('Time it took to solve up to supposition: {}'.format(total_time), end='\n\n')
        alg.supposition(puzzle)

    t1 = time.time()
    total_time = t1 - t0

    if puzzle.solved:
        print('Solved puzzle:')
    else:
        print('Something went wrong!\nThis is an incorrect solution:')
    puzzle.print_puzzle()
    print('Time to solve: {}'.format(total_time))


main()
