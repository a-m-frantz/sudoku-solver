def read_file():
    # infile_name = input('Puzzle file name: ')
    infile_name = 'test5.txt'
    print('Input file: ' + infile_name, end='\n\n')
    infile = open(infile_name)
    puzzle = infile.read()
    return puzzle
