# sudoku-solver
Python program that can solve any sudoku puzzle.

## Usage
This program requires Python3 to function. Make sure you have the proper
version installed.

First you have to clone this repository and navigate to its root directory.
```
git clone https://github.com/a-m-frantz/sudoku-solver
cd sudoku-solver/
```

### sudoku_solver.py
```
python sudoku_solver.py [-h] [-c] [input [input ...]]
```
`input` is the path to any number of files with sudoku puzzles in them.
If no files are supplied, the program will interactively ask you for a
path to a file after you run it.

The default behavior is to print the original puzzle followed by its
solution or a message that it can't be solved and the time it took to solve.
You can modify this with the `-c` flag.
```
python sudoku_solver.py -c [input [input ...]]
```
This just prints a message indicating whether the puzzle(s) are solvable.
If you're just interested in the time it took, see `benchmark.py` below.

The `-h` option prints a help message for the usage of the program.

### benchmark.py
```
python benchmark.py [-h] [-n NUM_TESTS] input [input ...]
```
`benchmark.py` can be used to test the performance of `sudoku_solver.py`.
This script will print the maximum, minimum, and average run times for each
puzzle provided, over a number of runs. The number of times to test each file
can be specified with the `-n` option. It defaults to 20 tests.

The `-h` option prints a help message for the usage of the script.

The most important result to look at is the minimum time to run.
This time represents when your computer was least busy with other processes.

Note that `benchmark.py` won't detect if a puzzle is unsolvable. In case of
an unsolvable puzzle, the output will represent the time it took for the
program to discover the puzzle could not be solved.

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

## Algorithm
The puzzle board can be broken down into "units", which are a single row,
column, or block. Each unit is comprised of 9 "cells", and each cell is a
part of 3 units. Additionally, each cell has 20 "peers".
A peer is a cell which occupies the same row, column, or block.

At the start of the program, each of the 81 cells gets assigned
a list of candidates, [1-9], representing the values that the cell could be.
The clue cells start out with their value solved.
Values are removed from the candidate list as the algorithm progresses.
A cell is solved once the size of its candidate list is reduced to one.

When a cell is solved, the value it took on is removed from the candidate
list of all of its peers.

A cell can be solved if it is a "hidden single."
When you look at the unsolved cells of a unit, if there is only one cell
that could be any given value, that cell must be that value, regardless
of how many other values are in its candidate list. This cell would be a
hidden single.

For example, you look at row 1 and there are 3 unsolved cells. The values
which have not been taken in that unit are 4, 6, and 7. Two of the cells
could be 6 or 7, and the third cell could be 4, 6, or 7. The third cell
must be 4, because row 1 must have a 4 in it and the third cell
is the only cell which could be a 4.

Merely finding hidden singles may be enough to solve the easiest sudoku
puzzles, but it won't be enough for most. When that isn't enough, you can
guess a possible value for an unsolved cell, then try to find any
new hidden singles that value created. If that results in a contradiction
somewhere else in the puzzle, such as two cells in the same unit having 4
as their answer, then you know the value you guessed for the original cell
is wrong and you can remove it from the candidate list. However, if there
is no contradiction, that doesn't mean it is the correct value. It only
means that guess is still a possible value.

If this guessing and checking is done recursively, making a second guess
when the first guess doesn't result in a contradiction,
and a third guess when the second guess doesn't result in a contradiction,
etc., then all valid sudoku puzzles can
be solved using only these two techniques.

The implementation of these two algorithms can be looked at in
`algorithms.py`.

There are other techniques which are similar to finding hidden singles,
but are a bit more complicated. A few of these can be found in
`extra_algorithms.py`. These additional algorithms are not incorporated
into the main program because they reduce the efficiency of the program,
but are valuable tools when solving sudoku puzzles by yourself, as the
guessing and checking method is easy for a computer to do, but hard to do
by hand.

## References
The 20 puzzles found in `sample_puzzles/hard20/` are the puzzles that were
used to benchmark 16 other sudoku solvers in
[this article](https://attractivechaos.wordpress.com/2011/06/19/an-incomplete-review-of-sudoku-solver-implementations/).
The article provides a good overview ways to implement a sudoku solver
in a variety of languages.

The articles written by [Peter Norivg](http://norvig.com/sudoku.html) and
[Peter Cock](https://warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/sudoku/)
 are also good in-depth looks at how to use
computers to solve sudoku puzzles.
