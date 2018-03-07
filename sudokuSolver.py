import init
import utility as util


def main():
    puzzle = init.read_file()
    util.print_puzzle(puzzle)
    candidates_array = init.generate_candidates(puzzle)
    # util.list_buddies(1)


main()
