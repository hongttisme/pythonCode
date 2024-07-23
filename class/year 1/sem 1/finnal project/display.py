

unicode_pieces = {
    6: "\u265A",
    5: "\u265B",
    4: "\u265C",
    3: "\u265D",
    2: "\u265E",
    1: "\u265F",
    0: "\u30FB",
    -1: "\u2659",
    -2: "\u2658",
    -3: "\u2657",
    -4: "\u2656",
    -5: "\u2655",
    -6: "\u2654"
}
normal_pieces = {
    6: "\u265A",
    5: "\u265B",
    4: "\u265C",
    3: "\u265D",
    2: "\u265E",
    1: "\u265F",
    0: ".",
    -1: "\u2659",
    -2: "\u2658",
    -3: "\u2657",
    -4: "\u2656",
    -5: "\u2655",
    -6: "\u2654"
}

unicode_numbers = {
    1: "\uFF11",
    2: "\uFF12",
    3: "\uFF13",
    4: "\uFF14",
    5: "\uFF15",
    6: "\uFF16",
    7: "\uFF17",
    8: "\uFF18",
}
unicode_alphabet = {
    0: "\u3000",
    1: "\uFF21",
    2: "\uFF22",
    3: "\uFF23",
    4: "\uFF24",
    5: "\uFF25",
    6: "\uFF26",
    7: "\uFF27",
    8: "\uFF28",
}
normal_numbers = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
}
normal_alphabet = {
    0: " ",
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
}

promotion_menu = """you are able to promotion now
1 for pawn
2 for knight
3 for bishop
4 for rook
5 for queen
"""

menu = """MAIN MENU
type 1 for chess rule
type 2 for game help
type 3 for new game
type 4 for set up chess board
type 5 for esc the program
"""

menu1 = """GAME MENU
type 1 for chess rule
type 2 for game help
type 3 for new game
type 4 for resume game
type 5 for quit game
"""

def display_board(map_array,method=0,bw = 0):
    if method == 0:
        print(" " * 3, end='')
        print("{:<2}".format(unicode_alphabet[0]), end="")
        for x in range(0,9):
            print("{:<2}".format(unicode_alphabet[x]), end="")
        print('\n')
        num = 9
        for row in map_array:
            num -= 1
            print(" " * 3,end='')
            print("{:<2}".format(unicode_numbers[num]), end="")
            print("{:<2}".format(unicode_alphabet[0]), end="")
            for piece in row:
                if bw == 0:
                    a = -piece
                else:
                    a = piece
                print("{:<2}".format(unicode_pieces[a]), end="")
            print()
    elif method == 1:
        print(" " * 3, end='')
        print("{:<2}".format(normal_alphabet[0]), end="")
        for x in range(0, 9):
            print("{:<2}".format(normal_alphabet[x]), end="")
        print('\n')
        num = 9
        for row in map_array:
            num -= 1
            print(" " * 3, end='')
            print("{:<2}".format(normal_numbers[num]), end="")
            print("{:<2}".format(normal_alphabet[0]), end="")
            for piece in row:
                if bw == 0:
                    a = -piece
                else:
                    a = piece
                print("{:<2}".format(normal_pieces[a]), end="")
            print()

text_chess_rule = """1. Board Setup: Chess is played on a square board divided into 64 squares of alternating colors, usually black and white. Each player starts with 16 pieces placed on the board as follows:

    The back rank (the row closest to the player) is filled with the following pieces from left to right: rook, knight, bishop, queen, king, bishop, knight, and rook.
    The second rank is filled with eight pawns.
2. Piece Movements:

    King: The king can move one square in any direction (horizontally, vertically, or diagonally).
    Queen: The queen can move any number of squares in any direction (horizontally, vertically, or diagonally).
    Rook: The rook can move any number of squares horizontally or vertically.
    Bishop: The bishop can move any number of squares diagonally.
    Knight: The knight moves in an L-shape: two squares in one direction (horizontally or vertically) and then one square perpendicular to that.
    Pawn: Pawns move forward one square, but they capture diagonally. On their first move, pawns have the option to move forward two squares.
3. Capturing: A piece captures an opponent's piece by moving to the square occupied by that piece. The captured piece is then removed from the board.

4. Check: When a king is under direct attack by an opponent's piece, it is said to be in "check." A player must remove the check on their king in their next move; otherwise, the game ends in checkmate.

5. Checkmate: Checkmate occurs when a player's king is in check, and there is no legal move to remove the check. The game ends, and the player in checkmate loses.

6. Stalemate: Stalemate occurs when a player's king is not in check, but they have no legal moves to make. The game ends in a draw, and neither player wins.

7. Castling: Castling is a special move involving the king and either of the player's rooks. It is used to improve the king's safety. There are specific requirements for castling, including no pieces between the king and the rook, the king not being in check, and the king not passing through or ending up in a square under attack.

8. Promotion: When a pawn reaches the opposite end of the board, it can be promoted to any other piece (except a king). The player usually chooses to promote the pawn to a queen, as it is the most powerful piece.
"""

readme = """== first, you have to start a new game ==
1. To move, enter the starting square of the piece then the the target square. 
    Example: if starting square is e2, target square is e4, input is "e2e4"
2. To take back, enter "b"
3. To enter settings during the game, enter "s" 
4. To quit the game, enter "q"
5. Move your King into the corresponding for castling.
"""
