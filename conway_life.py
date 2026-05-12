"""
Conway's Game of Life demostration

this script demostrate iteration by updating a board through
multiple iterations.

More info review README
"""


def count_live_neighbors(board, row, col):
    rows = len(board)
    cols = len(board[0])

    live_neighbors = 0

    start_row = row - 1
    end_row = row + 1

    start_col = col - 1
    end_col = col + 1

    i = start_row
    while i <= end_row:
        j = start_col

        while j <= end_col:

            if i == row and j == col:
                pass
            else:
                if i >= 0 and i < rows and j >= 0 and j < cols:
                    live_neighbors = live_neighbors + board[i][j]

            j = j + 1
        i = i + 1

    return live_neighbors


# iterations over every cell in the board
def get_next_cell_state(curent_cell, live_neighbors):
    next_cell = 0

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


# iterate over generations
def create_next_generation(board):
    rows = len(board)
    cols = len(board[0])

    new_board = []

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
        print()

        board = create_next_generation(board)  # new board replase init_board
        current_generation = current_generation + 1


# basic print board in terminal
def print_board(board):
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

    run_simulation(board, 10)


if __name__ == "__main__":
    main()
