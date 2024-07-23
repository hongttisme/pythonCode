file = 'login_info'


def choose(the_range):
    c = input("Enter your choice: ")
    for i in range(1, the_range + 1):
        if f"{i}" == c:
            return c
    print("wrong input!, please enter again!")
    return choose(the_range)


def login():
    name = input("please enter your username: ")
    players = get_players()

    a = False
    current_account = None
    for player in players:
        if player[0] == name:
            current_account = player
            a = True
            break
    if a:
        pw = input("please enter your password: ")
        if pw == current_account[1]:
            print("you are login now!")
            return current_account
        else:
            print("wrong password!")
    else:
        print("username does not exist!")


def add_info(f, info):  # append something into the file
    store_append = open(f, 'a')
    store_append.write(info)


def read_info(f):  # return the things in the file
    store_read = open(f, 'r')
    result = store_read.readlines()
    store_read.close()
    return result


def get_players():  # get players info list
    players = []
    for info in read_info(file):
        player = []
        s = ''
        for char in info:
            if char == '\t' or char == '\n':
                player.append(s)
                s = ''
            else:
                s += char
        player[2] = int(player[2])
        players.append(player)

    return players  # [[username1, password1, score1], ............]


def new_player():  # register a new player account
    name = input("please enter your username: ")
    players = get_players()

    a = False
    for player in players:
        if player[0] == name:
            a = True
            break
    while a:
        name = input("this username was in use, pls enter a new one: ")
        a = False
        for player in players:
            if player[0] == name:
                a = True
                break

    pw = input("please enter your password: ")
    add_info(file, f'{name}\t{pw}\t{100}\n')
    print("All set!, your account are able to login now!")


add_info(file,'')
the_current_player = None
while True:
    if the_current_player is None:
        print("====haven't login MENU====")
        print("1. login")
        print("2. register new account")
        print("3. leave game")
        action = choose(3)
        if action == "1":
            the_current_player = login()
        elif action == "2":
            new_player()
            continue
        elif action == "3":
            print("bye bye")
            break
    else:
        print(f"===={the_current_player[0]} MENU====")
        print("1. logout")
        print("2. leave game")

        action = choose(2)

        if action == "1":
            print("logout successfully!!")
            the_current_player = None
        elif action == "2":
            print("bye bye")
            break
