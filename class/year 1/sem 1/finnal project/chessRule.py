import numpy as np
from display import *

NO_PIECE = 0
WHITE_PAWN = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 3
WHITE_ROOK = 4
WHITE_QUEEN = 5
WHITE_KING = 6
BLACK_PAWN = -1
BLACK_KNIGHT = -2
BLACK_BISHOP = -3
BLACK_ROOK = -4
BLACK_QUEEN = -5
BLACK_KING = -6

PAWN = 1  # added constants
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
WHITE = 1
BLACK = 2

DISPLAY_METHOD = 0
BW = 0

startingPosition = np.array([[-4, -2, -3, -5, -6, -3, -2, -4],
                             [-1, -1, -1, -1, -1, -1, -1, -1],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [4, 2, 3, 5, 6, 3, 2, 4]])



def convert_coordinate(row, col):
    coordinate_letter = "ABCDEFGH"
    coordinate_row = coordinate_letter[col]
    coordinate_column = str(row + 1)
    return coordinate_row + coordinate_column


def get_coordinate(s, array):
    for k in range(array.shape[0]):
        for l in range(array.shape[1]):
            if array[k, l] == s:
                return [7 - k, l]


converted_array = np.empty(startingPosition.shape, dtype=object)
for i1 in range(startingPosition.shape[0]):
    for j1 in range(startingPosition.shape[1]):
        converted_array[i1, j1] = convert_coordinate(i1, j1)

def move2coordinate(map_array, move):
    r0 = move[0][0]
    c0 = move[0][1]
    r1 = move[1][0]
    c1 = move[1][1]
    piece = map_array[r0][c0]
    target = map_array[r1][c1]
    return r0, c0, r1, c1, piece, target

def move_pure(map_array, move):  # move without considering legal or not
    r0, c0, r1, c1, piece, target = move2coordinate(map_array, move)
    map_array[r1][c1] = piece
    map_array[r0][c0] = NO_PIECE


def basic_move_check(map_array, move, the_player):  # this function return True if basic move is valid
    # map_array example: startingPosition
    # command example: np.array([[startingXPosition, startingYPosition], [endingXPosition, endingYPosition]])
    # player example: 1 or 2
    r0, c0, r1, c1, piece, target = move2coordinate(map_array, move)

    # check the place is empty or not
    if piece == NO_PIECE:
        return False

    # check if player have the right to move the chosen piece
    if piece > 0 and the_player == BLACK:
        return False
    elif piece < 0 and the_player == WHITE:
        return False

    # check if player have the right to eat the corresponding piece
    if target > 0 and the_player == WHITE:
        return False
    elif target < 0 and the_player == BLACK:
        return False

    # move rule check
    # 1.Pawn
    if abs(piece) == PAWN:
        if (r0 - r1 == piece // 1) and ((target == 0 and c0 == c1) or (target != 0 and abs(c1 - c0) == 1)):
            return True
        else:
            return False

    # 2.Knight
    if abs(piece) == KNIGHT:
        if (abs(r1 - r0) > 0 and abs(c1 - c0) > 0) and (abs(r1 - r0) + abs(c1 - c0) == 3):
            return True
        else:
            return False

    # 3.Bishop
    if abs(piece) == BISHOP:
        is_pass = True
        if abs(c1 - c0) != abs(r1 - r0):
            is_pass = False
        else:
            for x in range(1, abs(c1 - c0)):
                if map_array[r0 + x * abs(r1 - r0) // (r1 - r0), c0 + x * abs(c1 - c0) // (c1 - c0)] != 0:
                    is_pass = False
                    break

        if is_pass:
            return True
        else:
            return False

    # 4.Rook
    if abs(piece) == ROOK:
        is_pass = True
        if (c1 - c0 != 0) and (r1 - r0 != 0):
            is_pass = False
        else:
            if r1 - r0 == 0:
                for x in range(1, abs(c1 - c0)):
                    if map_array[r0, c0 + x * abs(c1 - c0) // (c1 - c0)] != 0:
                        is_pass = False
                        break
            else:
                for x in range(1, abs(r1 - r0)):
                    if map_array[r0 + x * abs(r1 - r0) // (r1 - r0), c0] != 0:
                        is_pass = False
                        break
        if is_pass:
            return True
        else:
            return False

    # 5.Queen
    if abs(piece) == QUEEN:
        is_pass = True
        if abs(c1 - c0) != abs(r1 - r0):
            if (c1 - c0 != 0) and (r1 - r0 != 0):
                is_pass = False
            else:
                if r1 - r0 == 0:
                    for x in range(1, abs(c1 - c0)):
                        if map_array[r0, c0 + x * abs(c1 - c0) // (c1 - c0)] != 0:
                            is_pass = False
                            break
                else:
                    for x in range(1, abs(r1 - r0)):
                        if map_array[r0 + x * abs(r1 - r0) // (r1 - r0), c0] != 0:
                            is_pass = False
                            break
        else:
            for x in range(1, abs(c1 - c0)):
                if map_array[r0 + x * abs(r1 - r0) // (r1 - r0), c0 + x * abs(c1 - c0) // (c1 - c0)] != 0:
                    is_pass = False
                    break

        if is_pass:
            return True
        else:
            return False

    # 6.King
    if abs(piece) == KING:
        if (abs(c1 - c0) > 0 or abs(r1 - r0) > 0) and (abs(c1 - c0) < 2 and abs(r1 - r0) < 2):
            return True
        else:
            return False

    return False


def check_check(map_array, player):  # check if player's king is in check
    king = None
    king_position = None
    opponent = None
    if player == WHITE:  # returns False if king is not in check
        king = WHITE_KING
        opponent = BLACK
    elif player == BLACK:
        king = BLACK_KING
        opponent = WHITE

    for i in range(8):  # finds the coordinate of the player's king
        for j in range(8):
            if map_array[i, j] == king:
                king_position = np.array([i, j])

    for i in range(8):  # check every move of opponent where target is the king
        for j in range(8):
            if basic_move_check(map_array, np.array([[i, j], king_position]), opponent):
                return True

    return False


def check_pawn_2_step(map_array, move, the_player):  # returns True if player performs this special move, else False
    r0, c0, r1, c1, piece, target = move2coordinate(map_array, move)
    starting_row = None

    # check if player have the right to move the chosen piece
    if piece > 0 and the_player == BLACK:
        return False
    elif piece < 0 and the_player == WHITE:
        return False

    if piece == WHITE_PAWN:  # determine the starting row of pawn
        starting_row = 6
    elif piece == BLACK_PAWN:
        starting_row = 1

    if abs(piece) != PAWN:  # check if the piece is a pawn
        return False

    if r1 - r0 != -2 * piece or c0 != c1:  # check if it moved 2 steps forward
        return False

    if r0 != starting_row:  # check if the pawn is on its starting row
        return False

    if target != NO_PIECE or map_array[int((r1 + r0) / 2)][c0] != NO_PIECE:  # check if any piece is in the way
        return False

    return True


def check_promotion(map_array, move, the_player):  # returns True if player performs this special move, else False
    r0, c0, r1, c1, piece, target = move2coordinate(map_array, move)

    if abs(piece) != PAWN:  # check if the piece is a pawn
        return False

    if r1 != 0 and r1 != 7:  # check if pawn is moving towards the last row
        return False

    if not basic_move_check(map_array, move, the_player):  # check if it is a basic legal move
        return False

    return True


def check_castling(map_array, move, the_player, # returns True if player performs this special move, else False
                   white_a_rook_moved, white_h_rook_moved, white_king_moved,
                   black_a_rook_moved, black_h_rook_moved, black_king_moved):
    r0, c0, r1, c1, piece, target = move2coordinate(map_array, move)
    c2 = int((c1 + c0) / 2)
    map_array_2 = map_array.copy()

    if piece > 0 and the_player == BLACK:
        return False
    elif piece < 0 and the_player == WHITE:
        return False

    if abs(piece) != KING: # check if piece is king
        return False

    if r0 != r1 or abs(c0 - c1) != 2: # check if king moves 2 steps to left or right
        return False

    if r1 == 0 and c1 == 2: # check if rook or king moved, and if anything is in the way
        if black_a_rook_moved or black_king_moved:
            return False
        if not np.array_equal(map_array[0, 1:4], np.array([0, 0, 0])):
            return False
    elif r1 == 0 and c1 == 6:
        if black_h_rook_moved or black_king_moved:
            return False
        if not np.array_equal(map_array[0,5:7], np.array([0,0])):
            return False
    elif r1 == 7 and c1 == 2:
        if white_a_rook_moved or white_king_moved:
            return False
        if not np.array_equal(map_array[7,1:4], np.array([0,0,0])):
            return False
    elif r1 == 7 and c1 == 6:
        if white_h_rook_moved or white_king_moved:
            return False
        if not np.array_equal(map_array[7, 5:7], np.array([0, 0])):
            return False
    else:
        return False

    if check_check(map_array_2, the_player): # check if king in check
        return False
    move_pure(map_array_2, np.array([[r0, c0], [r1, c1]]))
    if check_check(map_array_2, the_player):
        return False
    move_pure(map_array_2, np.array([[r1, c1], [r1, c2]]))
    if check_check(map_array_2, the_player):
        return False

    return True

def check_rule(the_map, move, player, record_castling_able, method = 0, moved_record = None):
    choice = 5
    if (
            basic_move_check(the_map, move, player) or
            check_pawn_2_step(the_map, move, player)
    ):
        testing_map = the_map.copy()
        move_pure(testing_map, move)
        if check_check(testing_map, player):
            return 1
        else:
            if check_promotion(the_map, move, player):
                if method == 0:
                    print(promotion_menu)
                    while True:
                        choice = input("please input your choice: ")
                        if choice.isdigit():
                            if 0 < int(choice) < 6:
                                break
                        print("Wrong input, please try again!")
                else:
                    choice = moved_record[-1][1]
                move_pure(the_map, move)
                if player == 1:
                    the_map[move[1][0], move[1][1]] = int(choice)
                else:
                    the_map[move[1][0], move[1][1]] = int(choice) * -1
            else:
                move_pure(the_map, move)

        return 2 + int(choice)


    else:

        if check_castling(the_map, move, player,
                          record_castling_able[0][0],
                          record_castling_able[0][1],
                          record_castling_able[0][2],
                          record_castling_able[1][0],
                          record_castling_able[1][1],
                          record_castling_able[1][2],
                          ):
            move_pure(the_map, move)
            if move[0][1] < move[1][1]:
                move_pure(the_map, np.array([[move[0][0], 7], [move[0][0], 5]]))
            else:
                move_pure(the_map, np.array([[move[0][0], 0], [move[0][0], 3]]))
            return
        elif len(moved_record) > 0:
            last_move = np.array(
                [get_coordinate(moved_record[-1][0][0:2], converted_array),
                 get_coordinate(moved_record[-1][0][2:], converted_array)])

            piece = the_map[move[0,0],move[0,1]]
            if piece == WHITE_PAWN and player == BLACK:
                return 2
            elif piece == BLACK_PAWN and player == WHITE:
                return 2
            if last_move[0,1] == last_move[1,1] == move[1,1]:
                if moved_record[-1][0][1] == "7" and moved_record[-1][0][3] == "5" and the_map[move[0,0],move[1,1]] == BLACK_PAWN and the_map[move[0,0],move[0,1]] == WHITE_PAWN:
                    move_pure(the_map, move)
                    the_map[move[0,0],move[1,1]] = 0
                    return
                elif moved_record[-1][0][1] == "2" and moved_record[-1][0][3] == "4" and the_map[move[0,0],move[1,1]] == WHITE_PAWN and the_map[move[0,0],move[0,1]] == BLACK_PAWN:
                    move_pure(the_map, move)
                    the_map[move[0,0],move[1,1]] = 0
                    return
        return 2



def game_play(the_map, player, record_castling_able, record_list = None, method = 0,dm = 0, dbw = 0):


    # set up this round player
    if record_list is None:
        record_list = list()

    if player == BLACK:
        player = WHITE
        opponent = BLACK
    else:
        player = BLACK
        opponent = WHITE


    # display
    if method == 0:
        print("-" * 50)
        if player == WHITE:
            print("White turn")
        elif player == BLACK:
            print("Black turn")
        display_board(the_map, method=dm, bw=dbw)


    # get input
    if method == 0:
        the_input = input("Please input your move(example: A2A4, Q, B, S): ").upper()
    elif len(record_list) == 0:
        return startingPosition.copy(), np.array([[0, 0, 0], [0, 0, 0]])
    else:
        the_input = record_list[method - 1][0]


    # if quit or black
    if the_input == "Q":
        return
    if the_input == "B":
        if len(record_list) == 0:
            player = opponent
            print("You are not Back able now!")
        else:
            record_list.pop()
            the_map, record_castling_able = game_play(startingPosition.copy(),BLACK,np.array([[0, 0, 0], [0, 0, 0]]), record_list, method=1, dm=dm,dbw=dbw)
        return game_play(the_map, player, record_castling_able, record_list, dm=dm,dbw=dbw)
    if the_input == "S":
        while True:
            print()
            print("-" * 50)
            print(menu1)
            s = input("your input: ")
            if s == '1':
                print(text_chess_rule)
                input("(press enter to esc chess rule page)")
            elif s == '2':
                print(readme)
                input("(press enter to esc help page)")
            elif s == '5':
                return
            elif s == '4':
                break
            elif s == '3':
                # set up the game
                player = BLACK
                record_castling_able = np.array([[0, 0, 0], [0, 0, 0]])
                the_map = startingPosition.copy()
                return game_play(the_map, player, record_castling_able, dm=dm, dbw=dbw)
            else:
                print("wrong input")
        player = opponent
        return game_play(the_map, player, record_castling_able, record_list, dm=dm, dbw=dbw)


    # check input
    if len(the_input) != 4 or the_input[0:2] not in converted_array or the_input[2:] not in converted_array:
        print("wrong input!")
        player = opponent
        return game_play(the_map, player, record_castling_able,record_list, dm=dm, dbw=dbw)
    else:
        move = np.array(
            [get_coordinate(the_input[0:2], converted_array), get_coordinate(the_input[2:], converted_array)])


    # checking the move
    if method == 0:
        ans = check_rule(the_map, move, player, record_castling_able,moved_record=record_list, method=0)
    else:
        ans = check_rule(the_map, move, player, record_castling_able, moved_record=record_list[:method-1], method=1)
    if ans == 1:
        print("you will be check!")
        player = opponent
        return game_play(the_map, player, record_castling_able, record_list, dm=dm, dbw=dbw)
    elif ans == 2:
        print("you cant do this!")
        player = opponent
        return game_play(the_map, player, record_castling_able, record_list, dm=dm, dbw=dbw)


    # record action for check castling
    for action in move:
        if action[0] == 7 and action[1] == 0:
            record_castling_able[0][0] = 1
        elif action[0] == 7 and action[1] == 7:
            record_castling_able[0][1] = 1
        elif action[0] == 7 and action[1] == 4:
            record_castling_able[0][2] = 1
        elif action[0] == 0 and action[1] == 0:
            record_castling_able[1][0] = 1
        elif action[0] == 0 and action[1] == 7:
            record_castling_able[1][1] = 1
        elif action[0] == 0 and action[1] == 4:
            record_castling_able[1][2] = 1


    #check checkmate
    checkmate = True
    if method == 0:
        for r0 in range(8):
            for c0 in range(8):
                for r1 in range(8):
                    for c1 in range(8):
                        testing_map = the_map.copy()
                        ans_1 = check_rule(testing_map, np.array([[r0,c0],[r1,c1]]), opponent, record_castling_able,moved_record=record_list,method=1)
                        if ans_1 != 1 and ans_1 != 2:
                            checkmate = False
        if checkmate:
            print("-" * 50)
            display_board(the_map, method=dm, bw=dbw)
            print("Checkmate! ")
            if player == WHITE:
                print("White win the game!")
            elif player == BLACK:
                print("Black win the game!")
            input("press enter to continue")
            return

        if ans is None:
            record_list.append([the_input, None])
        else:
            record_list.append([the_input, ans - 2])
            if len(record_list) > 2:
                record_list[-2][1] = ans - 2


        return game_play(the_map, player, record_castling_able, record_list, dm=dm, dbw=dbw)
    else:
        if len(record_list) > method:
            return game_play(the_map, player, record_castling_able, record_list, method=method+1, dm=dm, dbw=dbw)
        return the_map, record_castling_able

