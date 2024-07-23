import time
import pygame
import sys

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (52, 136, 60)

# 定义棋盘大小和每个格子的大小
BOARD_SIZE = 8
CELL_SIZE = 60
WIDTH, HEIGHT = BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE
SEARCH_DEPTH = 8

# 初始化窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("黑白棋")

# 初始化棋盘
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[3][3] = board[4][4] = 'O'
board[3][4] = board[4][3] = 'X'

# 当前玩家
current_player = 'X'


def evaluate(the_board, player):
    score = 0

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if the_board[i][j] == player:
                score += 1

                if i == 0 or i == BOARD_SIZE - 1:
                    if j == 0 or j == BOARD_SIZE - 1:
                        score += 40

                if i == 0:
                    if j == 1 or j == BOARD_SIZE - 2:
                        score -= 10
                if i == 1:
                    if j == 0 or j == 1 or j == BOARD_SIZE - 2 or j == BOARD_SIZE - 1:
                        score -= 10
                if i == BOARD_SIZE-2:
                    if j == 0 or j == 1 or j == BOARD_SIZE - 2 or j == BOARD_SIZE - 1:
                        score -= 20
                if i == BOARD_SIZE-1:
                    if j == 1 or j == BOARD_SIZE - 2:
                        score -= 20

            elif the_board[i][j] == opponent(player):
                score -= 1
                if i == 0 or i == BOARD_SIZE - 1:
                    if j == 0 or j == BOARD_SIZE - 1:
                        score -= 20
    return score


def return_able_move(the_board, the_current_player):
    move_list = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(row, col, the_current_player, the_board):
                move_list.append([row, col])
    return move_list


def make_temporary_move(board, row, col, player):
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dir in directions:
        dr, dc = dir
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and new_board[r][c] == opponent(player):
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and new_board[r][c] == opponent(player):
                r += dr
                c += dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and new_board[r][c] == player:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and new_board[r][c] == opponent(player):
                    new_board[r][c] = player
                    r += dr
                    c += dc
    return new_board


def alpha_beta_search(the_board, depth, alpha, beta, maximizing_player):
    if depth == 0 or len(return_able_move(the_board, current_player)) == 0:
        return evaluate(the_board, current_player)

    legal_moves = return_able_move(the_board, current_player)
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in legal_moves:
            new_board = make_temporary_move(the_board, move[0], move[1], current_player)
            the_eval = alpha_beta_search(new_board, depth - 1, alpha, beta, False)
            if the_eval > max_eval:
                max_eval = the_eval
                best_move = move
            alpha = max(alpha, the_eval)
            if beta <= alpha:
                break
        if depth == SEARCH_DEPTH:
            return best_move
        return max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in legal_moves:
            new_board = make_temporary_move(the_board, move[0], move[1], opponent(current_player))
            the_eval = alpha_beta_search(new_board, depth - 1, alpha, beta, True)
            if the_eval < min_eval:
                min_eval = the_eval
                best_move = move
            beta = min(beta, the_eval)
            if beta <= alpha:
                break
        if depth == SEARCH_DEPTH:
            return best_move
        return min_eval


def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

            if board[row][col] == 'X':
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)


def is_valid_move(row, col, player, the_board):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and the_board[row][col] == ' ':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir in directions:
            dr, dc = dir
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == opponent(player):
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == opponent(player):
                    r += dr
                    c += dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == player:
                    return True
        return False
    else:
        return False


def make_move(row, col, player, the_board):
    the_board[row][col] = player

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dir in directions:
        dr, dc = dir
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == opponent(player):
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == opponent(player):
                r += dr
                c += dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == player:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and the_board[r][c] == opponent(player):
                    the_board[r][c] = player
                    r += dr
                    c += dc


def switch_player(the_current_player):
    return 'O' if the_current_player == 'X' else 'X'


def opponent(player):
    return 'O' if player == 'X' else 'X'


def main():
    global current_player
    start_time = time.time()
    while True:
        the_time = time.time() - start_time

        if current_player == "X":
            pygame.display.set_caption("bot thinking")
            if len(return_able_move(board, current_player)) == 0:
                current_player = switch_player(current_player)
            else:
                the_move = alpha_beta_search(board, SEARCH_DEPTH, float('-inf'), float('inf'), True)
                if is_valid_move(the_move[0], the_move[1], current_player, board):
                    make_move(the_move[0], the_move[1], current_player, board)
                    current_player = switch_player(current_player)

            if len(return_able_move(board, current_player)) == 0:
                current_player = switch_player(current_player)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE

                        if is_valid_move(row, col, current_player, board):
                            make_move(row, col, current_player, board)
                            current_player = switch_player(current_player)
        else:
            pygame.display.set_caption("your turn!")
            if len(return_able_move(board, current_player)) == 0:
                current_player = switch_player(current_player)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE

                        if is_valid_move(row, col, current_player, board):
                            make_move(row, col, current_player, board)
                            current_player = switch_player(current_player)
        screen.fill(WHITE)
        draw_board()
        pygame.display.flip()

        if len(return_able_move(board, current_player)) == 0 and len(
                return_able_move(board, opponent(current_player))) == 0:
            print("white: ", evaluate(board, 'O'))
            break


if __name__ == "__main__":
    main()
