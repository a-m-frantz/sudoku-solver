import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)
    tier_one_checks = 0
    tier_two_checks = 0

    print('Starting puzzle:')
    puzzle.print_puzzle()

    print('Removing clues from candidate lists')
    alg.update_clue_regions(puzzle)
    print('Done removing clues from candidate lists', end='\n\n')

    while puzzle.changed:
        while puzzle.changed:
            # Tier one checks
            tier_one_checks += 1
            puzzle.changed = False

            print('Finding hidden singles', end='\n\n')
            alg.find_hidden_sets(puzzle, 1)
            puzzle.check()

            print('Finding naked pairs', end='\n\n')
            alg.find_preemptive_set(puzzle, 2)
            puzzle.check()

            print('Finding hidden pairs', end='\n\n')
            alg.find_hidden_sets(puzzle, 2)
            puzzle.check()

            print('Finding naked triples', end='\n\n')
            alg.find_preemptive_set(puzzle, 3)
            puzzle.check()

            puzzle.print_puzzle()

        # Tier two checks
        tier_two_checks += 1
        print('Finding hidden triples', end='\n\n')
        alg.find_hidden_sets(puzzle, 3)
        puzzle.check()

        print('Finding naked quads', end='\n\n')
        alg.find_preemptive_set(puzzle, 4)
        puzzle.check()

        print('Finding hidden quads', end='\n\n')
        alg.find_hidden_sets(puzzle, 4)
        puzzle.check()

        puzzle.print_puzzle()
        puzzle.check()

    # puzzle.print_all_candidates()
    print('Number of tier one checks: {}'.format(tier_one_checks))
    print('Number of tier two checks: {}'.format(tier_two_checks))

main()
