from chessRule import *
# all constant stored in chessRule.py
# all things about display stored in display.py
def chess_board_setup():
    while True:
        display_board(startingPosition)
        a = input("does the chessboard align correctly?(Y/N)").upper()
        the_method = None
        if a == 'N':
            the_method = 1
            break
        elif a == 'Y':
            the_method = 0
            break
        else:
            print("Wrong input! Please input again")

    while True:
        display_board(startingPosition, method=the_method)
        a = input("Is the white piece on the bottom?(Y/N)").upper()
        the_bw = None
        if a == 'N':
            the_bw = 1
            break
        elif a == 'Y':
            the_bw = 0
            break
        else:
            print("wrong input! please input again")
    input("All done!, are you ready to go? (press enter to continue)")
    return the_method, the_bw

print("welcome to our chess game!!")
input("first, lets configure our chessboard (press enter to continue)")
method, bw = chess_board_setup()
print()
print("-" * 50)
while True:

    print(menu)
    s = input("your input: ")
    if s == '1':
        print(text_chess_rule)
        input("(press enter to esc chess rule page)")
    elif s == '2':
        print(readme)
        input("(press enter to esc help page)")
    elif s == '5':
        print("Bye, see you!")
        break
    elif s == '4':
        method,bw=chess_board_setup()
    elif s == '3':
        # set up the game
        player = BLACK
        record_castling_able = np.array([[0, 0, 0], [0, 0, 0]])
        the_map = startingPosition.copy()
        game_play(the_map,player,record_castling_able,dm=method,dbw=bw)
    else:
        print("wrong input")


    print()
    print("-"*50)

