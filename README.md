# sudoku-solver
Python program that can solve any sudoku puzzle.

## Usage
First clone this repository and navigate to its root directory.
```
git clone https://github.com/a-m-frantz/sudoku-solver
cd sudoku-solver/
```
Launch the program with `py sudoku_solver.py` and supply the path to
a text file containing a sudoku puzzle at the prompt. Sample puzzle files
are included in the `sample_puzzles/` directory.

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
