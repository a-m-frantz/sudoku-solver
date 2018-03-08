import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)

    print('Starting puzzle:')
    puzzle.print_puzzle()
    alg.update_clue_regions(puzzle)

    alg.find_hidden_singles(puzzle)
    print('After finding hidden singles:')
    puzzle.print_puzzle()

    puzzle.cell_array[2][0].print_cell()

    alg.find_triples(puzzle)
    print('After finding triples:')
    puzzle.print_puzzle()

    puzzle.cell_array[2][0].print_cell()

    alg.find_hidden_singles(puzzle)
    print('And singles again:')
    puzzle.print_puzzle()

    puzzle.cell_array[2][0].print_cell()

    alg.find_pairs(puzzle)
    print('After finding pairs:')
    puzzle.print_puzzle()

    puzzle.cell_array[2][0].print_cell()

    alg.find_hidden_singles(puzzle)
    print('And singles again:')
    puzzle.print_puzzle()

    puzzle.cell_array[2][0].print_cell()


main()
