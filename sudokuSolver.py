import init
import utility as util
import puzzle as pzl
import algorithm as alg


def main():
    raw_puzzle = init.read_file()
    util.print_puzzle(raw_puzzle)
    puzzle = pzl.Puzzle(raw_puzzle)
    alg.update_clue_regions(puzzle)


main()
