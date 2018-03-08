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
