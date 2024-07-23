def is_safe(board, row, col):
    for i in range(row):
        if board[i][col] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, len(board))):
        if board[i][j] == 1:
            return False

    return True


def print_board(board):
    for row in board:
        print(" ".join(["Q" if cell == 1 else "." for cell in row]))
    print()


def solve_queens(board, row, solutions_count):
    if row == len(board):
        solutions_count[0] += 1
        print(f"Solution {solutions_count[0]}:")
        print_board(board)
        print()
        return

    for col in range(len(board)):
        if is_safe(board, row, col):
            board[row][col] = 1

            solve_queens(board, row+1,solutions_count)
            board[row][col] = 0


def solve_8_queens():
    n = 8
    board = [[0] * n for _ in range(n)]
    solutions_count = [0]

    solve_queens(board, 0, solutions_count)
    if solutions_count[0] == 0:
        print("No solutions found.")


if __name__ == "__main__":
    solve_8_queens()
