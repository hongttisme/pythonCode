import chess


class ChessBot:
    def __init__(self, depth, color):
        self.depth = depth
        self.board = chess.Board()
        self.color = color

    def square_to_coord(self, square):
        return (square // 8, square % 8)

    def evaluate(self, board):
        material = 0
        for square, piece in board.piece_map().items():
            piece_val = self.get_piece_value(piece)
            material += piece_val * (1 if piece.color else -1)

            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    material += self.pawn_placement(square)
                if piece.color == chess.BLACK:
                    material -= self.pawn_placement(chess.square_mirror(square))
            elif piece.piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    material += self.knight_placement(square)
                if piece.color == chess.BLACK:
                    material -= self.knight_placement(chess.square_mirror(square))
            elif piece.piece_type == chess.KING:
                if piece.color == chess.WHITE:
                    material += self.king_placement(square)
                if piece.color == chess.BLACK:
                    material -= self.king_placement(chess.square_mirror(square))
            elif piece.piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    material += self.rook_placement(square)
                if piece.color == chess.BLACK:
                    material -= self.rook_placement(chess.square_mirror(square))

        color = 1 if self.color else -1

        material += self.king_towards_corner(board) * color

        self.evaluate_castling(board)
        # self.check_doubled_pawns(board)
        return material

    def evaluate_castling(self, board):
        score = 0
        if board.has_kingside_castling_rights(chess.WHITE):
            score += 100
        if board.has_queenside_castling_rights(chess.WHITE):
            score += 70
        if board.has_kingside_castling_rights(chess.BLACK):
            score -= 100
        if board.has_queenside_castling_rights(chess.BLACK):
            score -= 70
        return score

    def check_doubled_pawns(self, board):
        score = 0
        for file in chess.FILE_NAMES:
            white_pawns_in_file = sum(1 for square in chess.SQUARES if
                                      chess.square_file(square) == chess.FILE_NAMES.index(file) and board.piece_at(
                                          square) == chess.Piece(chess.PAWN, chess.WHITE))
            black_pawns_in_file = sum(1 for square in chess.SQUARES if
                                      chess.square_file(square) == chess.FILE_NAMES.index(file) and board.piece_at(
                                          square) == chess.Piece(chess.PAWN, chess.BLACK))

            if white_pawns_in_file == 2:
                score -= 30
            elif white_pawns_in_file > 2:
                score -= 40 * (white_pawns_in_file - 1)

            if black_pawns_in_file == 2:
                score += 30
            elif black_pawns_in_file > 2:
                score += 40 * (black_pawns_in_file - 1)
        return score

    def opening_score(self, board):
        piece_no = len(board.piece_map())
        piece_captured = 32 - piece_no
        if board.fullmove_number > 13 or piece_captured > 8:
            return 0
        return (1 - (8 - piece_captured) / 8 + (13 - board.fullmove_number) / 13)

    def king_towards_corner(self, board):
        score = 0
        self_king_coord = self.square_to_coord(board.king(self.color))
        enemy_king_coord = self.square_to_coord(board.king(not self.color))
        enemy_center_dist = max(3 - enemy_king_coord[0], enemy_king_coord[0] - 4) + max(3 - enemy_king_coord[1],
                                                                                        enemy_king_coord[1] - 4)
        score += enemy_center_dist

        king_dist = abs(self_king_coord[0] - enemy_king_coord[0]) + abs(self_king_coord[1] - enemy_king_coord[1])
        score += 14 - king_dist
        return score * 10 * self.endgame_score(board)

    def midgame_score(self, board):
        return

    def endgame_score(self, board):
        multiplier = 1 / 1600
        score_without_pawn = 0
        for square, piece in board.piece_map().items():
            if piece != chess.PAWN and piece.color != self.color:
                col = 1 if not self.color else -1
                score_without_pawn += self.get_piece_value(piece) * col
        return 1 - min(1, score_without_pawn * multiplier)

    def pawn_placement(self, square):
        pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 10, 10, -20, -20, 10, 10, 0,
            10, -5, 0, 0, 0, 0, -5, 10,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        return pawn_table[square]

    def pawn_end_placement(self, square):
        pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            10, 10, 10, 10, 10, 10, 10, 10,
            20, 20, 20, 20, 20, 20, 20, 20,
            30, 30, 30, 30, 30, 30, 30, 30,
            50, 50, 50, 50, 50, 50, 50, 50,
            70, 70, 70, 70, 70, 70, 70, 70,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        return pawn_table[square]

    def king_end_placement(self, square):
        king_table = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -10, 40, 40, 40, 40, 40, 40, -10,
            -10, -10, -10, -10, -10, -10, -10, -10
        ]

    def knight_placement(self, square):
        knight_table = [
            -30, -30, -10, -5, -5, -10, -30, -30,
            -20, -10, -5, 0, 0, -5, -10, -20,
            -10, 10, 30, 5, 5, 30, 10, -10,
            -5, 0, 20, 20, 20, 20, 0, -5,
            -5, 0, 30, 10, 10, 30, 0, -5,
            -10, -5, 0, 5, 5, 0, -5, -10,
            -20, -10, -5, 0, 0, -5, -10, -20,
            -30, -20, -10, -5, -5, -10, -20, -30
        ]
        return knight_table[square]

    def king_placement(self, square):
        king_table = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30
        ]
        return king_table[square]

    def rook_placement(self, square):
        rook_table = [
            0, 0, 10, 20, 20, 10, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 5, 5, 0, 0, 0
        ]
        return rook_table[square]

    def bishop_placement(self, square):
        bishop_table = [
            -20, -10, -30, -10, -10, -30, -10, -20,
            -10, 10, 0, 0, 0, 0, 10, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 5, 15, 10, 10, 15, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            5, 10, 10, 10, 10, 10, 10, 5,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]
        return bishop_table[square]

    def get_piece_value(self, piece):
        if piece.piece_type == chess.PAWN:
            return 100
        elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
            return 300
        elif piece.piece_type == chess.ROOK:
            return 500
        elif piece.piece_type == chess.QUEEN:
            return 900
        elif piece.piece_type == chess.KING:
            return 20000
        return 0

    def move_priority(self, board):
        move_prio = []
        for move in board.legal_moves:
            prio = 0

            if move.promotion:
                prio += self.get_piece_value(chess.Piece(move.promotion, chess.WHITE if board.turn else chess.BLACK))

            move_piece = board.piece_at(move.from_square)
            captured_piece = board.piece_at(move.to_square)
            if captured_piece != None:
                prio += 10 * self.get_piece_value(captured_piece) - self.get_piece_value(move_piece)

            move_prio.append((prio, move))

        move_prio.sort(reverse=True, key=lambda x: x[0])

        # Extract and return the list of moves
        return [move for _, move in move_prio]

    def minimax(self, board, depth, alpha, beta, player):
        if board.is_checkmate():
            return float('inf') if board.turn == chess.BLACK else -float('inf')

        if board.is_stalemate():
            return 0

        if depth == 0 or board.is_game_over():
            return self.search_captures(board, alpha, beta, player)

        if player:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def search_captures(self, board, alpha, beta, player):
        score = self.evaluate(board)
        alpha = max(score, alpha)
        if player:
            for move in board.legal_moves:
                if board.is_capture(move):
                    board.push(move)
                    score = self.evaluate(board)
                    board.pop()
                    alpha = max(score, alpha)
                    if beta <= alpha:
                        break
            return score
        else:
            for move in board.legal_moves:
                if board.is_capture(move):
                    board.push(move)
                    score = self.evaluate(board)
                    board.pop()
                    beta = min(score, beta)
                    if beta <= alpha:
                        break
            return score

    def play(self, board):
        best_move = None
        if self.color:
            best_score = -float('inf')
        else:
            best_score = float('inf')
        alpha = -float('inf')
        beta = float('inf')
        search_moves = self.move_priority(board)
        for move in search_moves:
            board.push(move)
            score = self.minimax(board, self.depth - 1, alpha, beta, not self.color)
            if board.is_checkmate():
                board.pop()
                return move
            board.pop()
            if self.color:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        print(best_score)
        return best_move

    def move(self, move):
        self.board.push(move)


def main():
    depth = int(input("Enter the depth of the bot (recommended: 3 or 4): "))
    color = input("Choose your color (white/black): ").strip().lower()
    player_color = chess.WHITE if color == 'white' else chess.BLACK
    bot_color = chess.BLACK if player_color == chess.WHITE else chess.WHITE

    bot = ChessBot(depth=depth, color=bot_color)

    print("Let's start the game!")
    print(bot.board)

    while not bot.board.is_game_over():
        if bot.board.turn == player_color:
            move = input("Enter your move in SAN format (e.g., Nf3): ").strip()
            try:
                san_move = bot.board.parse_san(move)
                bot.move(san_move)
            except:
                print("Invalid move. Please try again.")
                continue
        else:
            print("Bot is thinking...")
            best_move = bot.play(bot.color)
            bot.move(best_move)
            print(f"Bot plays: {best_move.uci()}")

        print(bot.board)
        print()

    print("Game over!")
    if bot.board.is_checkmate():
        print("Checkmate!")
    elif bot.board.is_stalemate():
        print("Stalemate!")
    elif bot.board.is_insufficient_material():
        print("Draw due to insufficient material!")
    elif bot.board.is_seventyfive_moves():
        print("Draw due to seventy-five moves rule!")
    elif bot.board.is_fivefold_repetition():
        print("Draw due to fivefold repetition!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()