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
    alg.update_clue_regions(puzzle)
    alg.solve(puzzle)
    while not puzzle.solved:
        alg.solve(puzzle, exhaustive=True)
        if not puzzle.solved:
            alg.supposition(puzzle)

    if puzzle.solved:
        print('Solved puzzle:')
    else:
        print('Something went wrong!\nThese are the incorrect candidate lists and puzzle')
        puzzle.print_all_candidates()
    puzzle.print_puzzle()

    t1 = time.time()
    total_time = t1 - t0
    print('Time to solve: {}'.format(total_time))


main()
