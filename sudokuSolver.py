import init
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    puzzle = pzl.Puzzle(raw_puzzle)
    print('Starting puzzle:')
    puzzle.print_puzzle()
    alg.update_clue_regions(puzzle)


main()
