import pygame
import sys
import chess
import chess.pgn
from alpha_beta import ChessBot as ABbot
from attentionChessbot import AttentionBot
from alpha_beta2 import ChessBot as NewABbot

# 初始化Pygame
pygame.init()

# 参数
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
BORDER = 2
CIRCLE_WIDTH = 8
CIRCLE_RADIUS = 15

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_COLOR1 = (235, 236, 208)
DARK_COLOR1 = (115, 149, 82)
GREY = (192, 192, 192)

# 设置
SQ_SIZE = WIDTH // 8
MOVE_RECORD = []

# 加载棋子图像
PIECES = {}
for piece in ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']:
    PIECES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))

# 初始化棋盘
board = chess.Board()

black_bot = NewABbot(4, False)
# black_bot = AttentionBot(False)
# black_bot = None
# white_bot = NewABbot(4, True)
white_bot = AttentionBot(True)

# white_bot = None


def get_pgn(board):
    game = chess.pgn.Game()
    node = game

    for move in board.move_stack:
        node = node.add_variation(move)

    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    pgn_string = game.accept(exporter)
    return pgn_string

def draw_board(screen):
    colors = [LIGHT_COLOR1, DARK_COLOR1]
    for r in range(8):
        for c in range(8):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    piece_to_image = {
        'P': 'wp', 'R': 'wr', 'N': 'wn', 'B': 'wb', 'Q': 'wq', 'K': 'wk',
        'p': 'bp', 'r': 'br', 'n': 'bn', 'b': 'bb', 'q': 'bq', 'k': 'bk'
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = PIECES[piece_to_image[piece.symbol()]]
            row, col = divmod(square, 8)
            screen.blit(piece_image, pygame.Rect(col * SQ_SIZE, (7 - row) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_legal_moves(screen, board, square):
    moves = board.legal_moves
    for move in moves:

        if move.from_square == square:
            to_square = move.to_square
            row, col = divmod(to_square, 8)
            if board.piece_at(move.to_square):
                pygame.draw.circle(screen, GREY, (col * SQ_SIZE + SQ_SIZE // 2, (7 - row) * SQ_SIZE + SQ_SIZE // 2),
                                   CIRCLE_RADIUS * 2, CIRCLE_WIDTH)
            else:
                pygame.draw.circle(screen, GREY, (col * SQ_SIZE + SQ_SIZE // 2, (7 - row) * SQ_SIZE + SQ_SIZE // 2),
                                   CIRCLE_RADIUS)


def draw_selected_square(screen, mouse_pos, is_promoting):
    if is_promoting:
        choice = get_promotion_choice(mouse_pos)
        options = ['q', 'r', 'b', 'n']
        y_offset = HEIGHT // 2 - 2 * SQ_SIZE
        for i, option in enumerate(options):
            if choice == option:
                pygame.draw.rect(screen, GREY,
                                 pygame.Rect(WIDTH // 2 - SQ_SIZE // 2, y_offset + i * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                                 2)

    elif 0 < mouse_pos[0] < WIDTH - 1 and 0 < mouse_pos[1] < HEIGHT - 1:
        mouse_row = mouse_pos[1] // SQ_SIZE
        mouse_col = mouse_pos[0] // SQ_SIZE

        square = chess.square(mouse_col, 7 - mouse_row)
        piece = board.piece_at(square)
        if piece and piece.color == board.turn:
            pygame.draw.rect(SCREEN, GREEN, (mouse_col * SQ_SIZE, mouse_row * SQ_SIZE, SQ_SIZE, SQ_SIZE), BORDER)
        else:
            pygame.draw.rect(SCREEN, RED, (mouse_col * SQ_SIZE, mouse_row * SQ_SIZE, SQ_SIZE, SQ_SIZE), BORDER)


def draw_promotion_options(screen, turn):
    options = ['q', 'r', 'b', 'n']
    y_offset = HEIGHT // 2 - 2 * SQ_SIZE
    for i, option in enumerate(options):
        piece = PIECES[f'w{option}' if turn else f'b{option}']
        pygame.draw.rect(screen, LIGHT_COLOR1, pygame.Rect(WIDTH // 2 - SQ_SIZE // 2, y_offset + i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(piece, pygame.Rect(WIDTH // 2 - SQ_SIZE // 2, y_offset + i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH // 2 - SQ_SIZE // 2, y_offset + i * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                         2)


def get_promotion_choice(pos):
    x, y = pos
    if WIDTH // 2 - SQ_SIZE // 2 <= x <= WIDTH // 2 + SQ_SIZE // 2:
        options = ['q', 'r', 'b', 'n']
        y_offset = HEIGHT // 2 - 2 * SQ_SIZE
        for i, option in enumerate(options):
            if y_offset + i * SQ_SIZE <= y <= y_offset + (i + 1) * SQ_SIZE:
                return option
    return None



def main():
    selected_square = None
    running = True
    promoting = False
    promotion_move = None
    end_flat = False

    while running:
        if board.turn and white_bot:
            move = white_bot.play(board)
            board.push(move)
        elif not board.turn and black_bot:
            move = black_bot.play(board)
            board.push(move)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(get_pgn(board))
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if promoting:
                        choice = get_promotion_choice(event.pos)
                        if choice:
                            promotion_move.promotion = chess.Piece.from_symbol(choice.upper()).piece_type
                            board.push(promotion_move)
                            promoting = False
                    else:
                        location = pygame.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        square = chess.square(col, 7 - row)

                        if selected_square is not None:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                board.push(move)
                                MOVE_RECORD = []
                            elif move.from_square != move.to_square:
                                if chess.Move.from_uci(str(move) + 'q') in list(board.legal_moves):
                                    promoting = True
                                    promotion_move = move
                            selected_square = None
                        else:
                            piece = board.piece_at(square)
                            if piece and piece.color == board.turn:
                                selected_square = square
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        if board.move_stack:
                            MOVE_RECORD.append(board.pop())
                    elif len(MOVE_RECORD) > 0 and event.key == pygame.K_x:
                        board.push(MOVE_RECORD.pop())

        draw_board(SCREEN)
        if selected_square is not None:
            row, col = divmod(selected_square, 8)
            pygame.draw.rect(SCREEN, BLUE, pygame.Rect(col * SQ_SIZE, (7 - row) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            draw_legal_moves(SCREEN, board, selected_square)
        draw_pieces(SCREEN, board)
        if promoting:
            draw_promotion_options(SCREEN, board.turn)

        # draw selected square
        pos = pygame.mouse.get_pos()
        draw_selected_square(SCREEN, pos, promoting)
        pygame.display.set_caption(f'White turn' if board.turn else f'Black turn')
        pygame.display.flip()
        if not end_flat:

            if board.is_checkmate():
                print("check mate!")
                print(get_pgn(board))
                end_flat = True
            if board.is_stalemate():
                print("stalemate!")
                print(get_pgn(board))

                end_flat = True
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
