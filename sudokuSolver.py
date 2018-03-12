import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)

    print('Starting puzzle:')
    puzzle.print_puzzle()

    print(str(puzzle.changed()))
    print('Removing clues from candidate lists')
    alg.update_clue_regions(puzzle)
    print('Done removing clues from candidate lists', end='\n\n')
    print(str(puzzle.changed()))

    while puzzle.changed():
        puzzle.reset()

        print('Finding hidden singles', end='\n\n')
        alg.find_hidden_singles(puzzle)
        puzzle.check()
        print()
        print('Finding naked pairs', end='\n\n')
        alg.find_naked_pairs(puzzle)
        puzzle.check()
        print()
        print('Finding hidden pairs', end='\n\n')
        alg.find_hidden_pairs(puzzle)
        puzzle.check()
        print()
        print('Finding naked triples', end='\n\n')
        alg.find_naked_triples(puzzle)
        puzzle.check()
        print()
        print('Finding hidden triples', end='\n\n')
        alg.find_hidden_triples(puzzle)
        puzzle.check()
        print()
        puzzle.print_puzzle()
        puzzle.check()
        print()

    puzzle.print_all_candidates()
    # print('Finding hidden singles')
    # alg.find_hidden_singles(puzzle)
    # print()
    # print('After finding hidden singles:')
    # puzzle.print_puzzle()
    #
    # for cell in [col[3] for col in puzzle.cell_array]:
    #     cell.print_cell()
    # print()
    #
    # print('Finding naked pairs')
    # alg.find_naked_pairs(puzzle)
    # print()
    # print('After finding naked pairs:')
    # puzzle.print_puzzle()
    #
    # for cell in [col[3] for col in puzzle.cell_array]:
    #     cell.print_cell()
    # print()
    #
    # print('Finding naked pairs #2')
    # alg.find_naked_pairs(puzzle)
    # print()
    # print('After finding naked pairs: #2')
    # puzzle.print_puzzle()
    #
    # for cell in [col[3] for col in puzzle.cell_array]:
    #     cell.print_cell()
    # print()
    #
    # print('Finding hidden pairs')
    # alg.find_hidden_pairs(puzzle)
    # print()
    # print('After finding hidden pairs:')
    # puzzle.print_puzzle()
    #
    # for cell in [col[3] for col in puzzle.cell_array]:
    #     cell.print_cell()
    # print()
    #
    # print('Finding naked triples')
    # alg.find_naked_triples(puzzle)
    # print()
    # print('After finding naked triples:')
    # puzzle.print_puzzle()


main()
