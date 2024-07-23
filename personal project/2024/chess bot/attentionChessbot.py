import numpy as np
import chess
import torch
from attention import GPTLanguageModel as Chessbot


def board_to_matrix(board):
    # Initialize a 8x8x12 matrix with zeros
    matrix = np.zeros((8, 8), dtype=int)

    # Piece types and their corresponding channels
    piece_to_channel = {
        'P': 1,  # White pawn
        'N': 2,  # White knight
        'B': 3,  # White bishop
        'R': 4,  # White rook
        'Q': 5,  # White queen
        'K': 6,  # White king
        'p': 7,  # Black pawn
        'n': 8,  # Black knight
        'b': 9,  # Black bishop
        'r': 10,  # Black rook
        'q': 11,  # Black queen
        'k': 12  # Black king
    }

    # Map the pieces to the matrix
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            channel = piece_to_channel[piece.symbol()]
            matrix[row, col] = channel

    return matrix


class AttentionBot:
    def __init__(self, player):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.player = player
        self.model = Chessbot().to(self.device)
        checkpoint = torch.load('model.pth')
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

    def play(self, board):
        chess_board = board

        board_array = board_to_matrix(chess_board)
        board_array = board_array.reshape(64)
        if self.player == chess.WHITE:
            a = np.array([14])
        else:
            a = np.array([13])

        x = torch.tensor(np.concatenate((a, board_array))).to(self.device)
        x = x.reshape(1, 65)
        print(x.shape)

        my_list = self.model(x)[0][0].tolist()
        print(len(my_list))

        index_with_list = [(x, i) for i, x in enumerate(my_list)]
        index_with_list = sorted(index_with_list, reverse=True)

        move_found_count = 0
        moves = []
        for output_move in index_with_list:
            for move in chess_board.legal_moves:
                chess_board.push(move)
                the_move = chess_board.pop()
                move_num = output_move[1]
                if the_move.from_square == move_num // 64 and the_move.to_square == move_num % 64:
                    print(the_move, output_move[0])
                    move_found_count += 1
                    moves.append(the_move)
                    break

            if move_found_count > 5:
                break

        return moves[0]
