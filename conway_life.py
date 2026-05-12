#!/usr/bin/env python3

"""
Conway's Game of Life demonstration.
autor: crissmath

This script demonstrates iteration by updating a board through
multiple generations.

If no pattern file is provided, it uses a default pattern.
If a pattern file is provided, it loads the board from the file.

Pattern file format:
X = live cell
. = dead cell
"""

import sys


def load_board_from_file(filename):
    board = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()

            if clean_line == "":
                continue

            row = []

            j = 0
            while j < len(clean_line):
                char = clean_line[j]

                if char == "X":
                    row.append(1)
                elif char == ".":
                    row.append(0)
                else:
                    print(f"Invalid character in pattern file: {char}")
                    sys.exit(1)

                j = j + 1

            board.append(row)

    if len(board) == 0:
        print("Error: empty pattern file.")
        sys.exit(1)

    cols = len(board[0])

    i = 0
    while i < len(board):
        if len(board[i]) != cols:
            print("Error: all rows in the pattern file must have the same size.")
            sys.exit(1)

        i = i + 1

    return board


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


def get_next_cell_state(current_cell, live_neighbors):
    next_cell = 0

    if current_cell == 1 and live_neighbors < 2:
        next_cell = 0
    elif current_cell == 1 and (live_neighbors == 2 or live_neighbors == 3):
        next_cell = 1
    elif current_cell == 1 and live_neighbors > 3:
        next_cell = 0
    elif current_cell == 0 and live_neighbors == 3:
        next_cell = 1
    else:
        next_cell = 0

    return next_cell


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

        board = create_next_generation(board)
        current_generation = current_generation + 1


def print_board(board):
    for row in board:
        line = ""

        for cell in row:
            if cell == 1:
                line = line + "X"
            else:
                line = line + "."

        print(line)


def main():
    generations = 5

    board = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]

    if len(sys.argv) >= 2:
        board = load_board_from_file(sys.argv[1])

    if len(sys.argv) >= 3:
        generations = int(sys.argv[2])

    run_simulation(board, generations)


if __name__ == "__main__":
    main()
