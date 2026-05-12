"""
Conway's Game of life:

rules:

1. Any live cell with fewer than 2 live neighbors dies.
    Reason: Underpopulation

2. Any live cell with 2 or 3 live neighbors survives.
    Reason: Stable population

3. Any live cell with more than 3 live neighbors dies.
    Reason: overpopulation.

4. Any dead cell with exactly 3 live neighbors becomes alive.
    Reason: reproductions
"""


# fuction for count neighbors
def count_live_neighbors(board, row, col):
    pass


# basic print board in terminal
def print_board(board):
    print("Conway's Game of life ")
    print(5 * "--")

    for row in board:
        line = ""

        for cell in row:
            if cell == 1:
                line += "X"
            else:
                line += "."
        print(line)


def main():
    board = [
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
    ]

    print_board(board)


if __name__ == "__main__":
    main()
