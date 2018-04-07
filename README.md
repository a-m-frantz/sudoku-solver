# sudoku-solver
Python program that can solve any sudoku puzzle.

## Usage
### sudoku_solver.py
Clone this repository, navigate to its root directory and call the program
from the commandline.
```
git clone https://github.com/a-m-frantz/sudoku-solver
cd sudoku-solver/
python sudoku_solver.py [-h] [-v] [input [input ...]]
```
`input` is the path to any number of files with sudoku puzzles in them.
If no files are supplied, the program will interactively ask you for a
path to a file after you run it.

The default behavior is to print the original puzzle followed by its
solution or a message that it can't be solved and the time it took to solve.
You can modify this behavior by typing
`python sudoku_solver.py -v [input [input ...]]`.
This just prints a message indicating whether the puzzle(s) are solvable.

The `-h` option prints a help message for the usage of the program.

### benchmark.py
`benchmark.py` can be used to test the performance of the `sudoku_solver.py`.
Call it with `python benchmark.py [-h] [-n NUM_TESTS] input [input ...]`.
The script will print the maximum, minimum, and average run times for each
puzzle provided over a number of runs. The number of times to test each file
can be specified with the `-n` option. It defaults to 20 tests.

The most important result to look at is the minimum time to run.
This time represents when your computer was least busy with other processes.

## Input files
For input files, sudoku puzzles are represented as 81 characters,
with `.`'s or `0`'s standing for unknown squares and digits `1-9` standing
for given clues. All whitespace and other characters are ignored, making
each of the following equivalent input:
```
.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8
```
```
094000130
000000000
000076002
080010000
032000000
000200060
000050400
000008007
006304008
```
```
. 9 4 | . . . | 1 3 .
. . . | . . . | . . .
. . . | . 7 6 | . . 2
---------------------
. 8 . | . 1 . | . . .
. 3 2 | . . . | . . .
. . . | 2 . . | . 6 .
---------------------
. . . | . 5 . | 4 . .
. . . | . . 8 | . . 7
. . 6 | 3 . 4 | . . 8
```

Sample puzzle files are included in the `sample_puzzles/` directory.
