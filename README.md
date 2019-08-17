# gomoku-ai

## Usage

Each AI is an Player object. An AI must implement `Player.move()` function, which takes an `Board` object as an argument and returns a valid coordinate tuple `(row, col)` of the player's move.

The cooridate must allow a valid move such as:

1. It's whithn the boundary of the board
2. It has not been occupied by a stone
3. `row` and `col` are integers
