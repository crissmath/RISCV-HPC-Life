"""
Conway's Game of life:
https://en.wikipedia.org/wiki/Conway's_Game_of_Life
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
    rows = len(board)
    cols = len(board[0])
    print(f"row: {rows}, cols:{cols}")

    live_neighbors = 0

    # init position of cell i check neighbors
    start_row = row - 1
    end_row = row + 1

    start_col = col - 1
    end_col = col + 1

    print(f"cell pos cell:{row, col}")
    print(f"init pos neighbors :{start_row, start_col}")
    print(f"end  pos neighbors:{end_row, end_col}")

    i = start_row
    while i <= end_row:
        j = start_col

        while j <= end_col:
            if not (i == row and j == col):  # dont evaluate the position of actual cell

                # check the limits in the board
                if i >= 0 and i < rows and j >= 0 and j < cols:
                    live_neighbors = live_neighbors + board[i][j]
            j = j + 1
        i = i + 1

    return live_neighbors


# basic print board in terminal
def print_board(board):
    print("Conway's Game of life ")
    print(10 * "--")

    for row in board:
        line = ""

        for cell in row:
            if cell == 1:
                line += "X"
            else:
                line += "."
        print(line)


def main():
    board_1 = [
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ]

    board = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]

    print_board(board)
    n_neighbors = count_live_neighbors(board, 2, 2)
    print(f"vecinos: {n_neighbors}")


if __name__ == "__main__":
    main()
