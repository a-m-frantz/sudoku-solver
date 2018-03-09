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

    print('Finding hidden singles')
    alg.find_hidden_singles(puzzle)
    print()
    print('After finding hidden singles:')
    puzzle.print_puzzle()

    for cell in puzzle.cell_array[1]:
        cell.print_cell()
    print()

    print('Finding naked pairs')
    alg.find_naked_pairs(puzzle)
    print()
    print('After finding naked pairs:')
    puzzle.print_puzzle()

    for cell in puzzle.cell_array[6]:
        cell.print_cell()

    # print('Finding trips')
    # alg.find_triples(puzzle)
    # print()
    # print('After finding triples:')
    # puzzle.print_puzzle()
    #
    # for cell in puzzle.cell_array[0]:
    #     cell.print_cell()


    #
    # alg.find_triples(puzzle)
    # print('After finding triples:')
    # puzzle.print_puzzle()
    #
    # puzzle.cell_array[2][0].print_cell()
    #
    # alg.find_hidden_singles(puzzle)
    # print('And singles again:')
    # puzzle.print_puzzle()
    #
    # puzzle.cell_array[2][0].print_cell()
    #
    # alg.find_pairs(puzzle)
    # print('After finding pairs:')
    # puzzle.print_puzzle()
    #
    # puzzle.cell_array[2][0].print_cell()
    #
    # alg.find_hidden_singles(puzzle)
    # print('And singles again:')
    # puzzle.print_puzzle()
    #
    # puzzle.cell_array[2][0].print_cell()


main()
