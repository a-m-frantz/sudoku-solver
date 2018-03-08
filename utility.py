TRIPLETS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

ROW_ITER = [[(row, col) for col in range(9)] for row in range(9)]
COL_ITER = [[(row, col) for row in range(9)] for col in range(9)]
BLOCK_ITER = [[(row, col) for row in rows for col in cols] for rows in TRIPLETS for cols in TRIPLETS]


def print_puzzle(puzzle):
    print('Starting puzzle:')
    for i, val in enumerate(puzzle):
        print(val, end=' ')
        if i == 80:
            print(end='\n\n')
        elif i % 27 == 26:
            print('\n' + '-' * 21)
        elif i % 9 == 8:
            print()
        elif i % 3 == 2:
            print('|', end=' ')
    return
