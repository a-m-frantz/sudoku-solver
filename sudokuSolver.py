import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)

    print('Starting puzzle:')
    puzzle.print_puzzle()

    print('Removing clues from candidate lists')
    alg.update_clue_regions(puzzle)
    print('Done removing clues from candidate lists', end='\n\n')

    while puzzle.changed():
        puzzle.reset()

        print('Finding hidden singles', end='\n\n')
        alg.find_hidden_singles(puzzle)
        puzzle.check()

        print('Finding naked pairs', end='\n\n')
        alg.find_preemptive_set(puzzle, 2)
        puzzle.check()

        print('Finding hidden pairs', end='\n\n')
        alg.find_hidden_pairs(puzzle)
        puzzle.check()

        print('Finding naked triples', end='\n\n')
        alg.find_preemptive_set(puzzle, 3)
        puzzle.check()

        print('Finding hidden triples', end='\n\n')
        alg.find_hidden_triples(puzzle)
        puzzle.check()

        print('Finding naked quads', end='\n\n')
        alg.find_preemptive_set(puzzle, 4)
        puzzle.check()

        puzzle.print_puzzle()
        puzzle.check()

    puzzle.print_all_candidates()


main()
