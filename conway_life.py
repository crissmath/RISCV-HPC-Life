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
    # print(f"row: {rows}, cols:{cols}")

    live_neighbors = 0

    # init position of cell i check neighbors
    # 3x3 squere posible neighbors
    start_row = row - 1
    end_row = row + 1

    start_col = col - 1
    end_col = col + 1

    # print(f"cell pos cell:{row, col}")
    # print(f"init pos neighbors :{start_row, start_col}")
    # print(f"end  pos neighbors:{end_row, end_col}")

    i = start_row
    while i <= end_row:
        j = start_col

        while j <= end_col:

            if i == row and j == col:
                # dont evaluate the position of actual cell
                pass

            # check the limits in the board
            else:
                if i >= 0 and i < rows and j >= 0 and j < cols:
                    live_neighbors = live_neighbors + board[i][j]

            j = j + 1
        i = i + 1

    return live_neighbors


# Conways rules fuction
def get_next_cell_state(curent_cell, live_neighbors):
    next_cell = 0
    """
    cell = 1, neighbors < 2  -> 0   (Underpoblacion)
    cell = 1, neighbors == 2 -> 1   (stable population)
    cell = 1, neighbors == 3 -> 1   (stable population)
    cell = 1, neighbors  > 3 -> 0   (over population)
    cell = 0, neighbors == 3 -> 1   (reproductions)
    cell = 0, otherwise      -> 0   (othercases)
    """
    if curent_cell == 1 and live_neighbors < 2:
        next_cell = 0
    elif curent_cell == 1 and (live_neighbors == 2 or live_neighbors == 3):
        next_cell = 1
    elif curent_cell == 1 and live_neighbors > 3:
        next_cell = 0
    elif curent_cell == 0 and live_neighbors == 3:
        next_cell = 1
    else:
        next_cell = 0

    return next_cell


def create_next_generation(board):
    rows = len(board)
    cols = len(board[0])

    new_board = (
        []
    )  # use a new board because all cell calculate this next step based in the las board

    i = 0
    while i < rows:
        new_row = []
        j = 0
        while j < cols:
            current_cell = board[i][j]
            live_neighbors = count_live_neighbors(board, i, j)

            next_cell = get_next_cell_state(current_cell, live_neighbors)
            new_row.append(next_cell)
            j = j + 1
        new_board.append(new_row)
        i = i + 1
    return new_board


def run_simulation(board, generations):
    current_generation = 0

    while current_generation <= generations:
        print(f"Generation {current_generation}")
        print_board(board)

        board = create_next_generation(board)  # the new board replaza the last board
        current_generation = current_generation + 1


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
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]

    row = 2
    col = 2

    # n_neighbors = count_live_neighbors(board, row, col)
    # current_cell = board[row][col]
    # next_cell = get_next_cell_state(current_cell, n_neighbors)

    # print(f"cell position : {row, col}")
    # print(f"current cell  : {current_cell}")
    # print(f"live neighbors: {n_neighbors}")
    # print(f"next_cell     : {next_cell}")

    # print("Initial board")
    # print_board(board)

    # new_board = create_next_generation(board)

    # print("\nNext generation:")
    # print_board(new_board)

    run_simulation(board, 4)


if __name__ == "__main__":
    main()
