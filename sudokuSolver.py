import init
import utility as util
import puzzle as pzl


def main():
    raw_puzzle = init.read_file()
    util.print_puzzle(raw_puzzle)
    # candidates_array = init.generate_candidates(puzzle)
    puzzle = pzl.Puzzle(raw_puzzle)

main()
