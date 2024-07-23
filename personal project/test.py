import chess

class ChessBot:
    def __init__(self, depth):
        self.depth = depth
        self.board = chess.Board()

    def evaluate(self, board):
        material = 0
        for piece in board.piece_map().values():
            piece_val = self.get_piece_value(piece)
            material += piece_val * (1 if piece.color else -1)
        return material

    def get_piece_value(self, piece):
        if piece.piece_type == chess.PAWN:
            return 1
        elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
            return 3
        elif piece.piece_type == chess.ROOK:
            return 5
        elif piece.piece_type == chess.QUEEN:
            return 9
        elif piece.piece_type == chess.KING:
            return 20000
        return 0

    def minimax(self, board, depth, alpha, beta, player):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None

        if player:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

bot = ChessBot(7)

board = chess.Board()

while not board.is_game_over():
    player_move = input("Your move: ")
    board.push_san(player_move)
    print(board)
    eval, move = bot.minimax(board, bot.depth, -float('inf'), float('inf'), False)
    print(f"Evaluation: {eval}, Best Move: {move}")
    board.push(move)
    print(board)
    print()
