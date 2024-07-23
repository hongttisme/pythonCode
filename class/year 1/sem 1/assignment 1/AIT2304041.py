menu = """1. Add new movie to the coming soon movie list
2. Add new movie to the showing now movie list (moved a movie from coming soon to showing now)
3. Remove a movie from showing now (it will be moved to shown list)
4. Print Coming Soon list
5. Print Showing now list
6. Print Shown list
7. Exit 
"""


class Cinema:
    def __init__(self, cinema_id, cinema_name):
        self.__Cinema_Id = cinema_id
        self.__Cinema_name = cinema_name
        self.__Showing_Now = []
        self.__Coming_Soon = []
        self.__Shown = []

    def update_cinema_id(self, cinema_id):
        self.__Cinema_Id = cinema_id

    def update_cinema_name(self, cinema_name):
        self.__Cinema_name = cinema_name

    def update_showing_now(self, showing_now):
        self.__Showing_Now = showing_now

    def update_coming_soon(self, coming_soon):
        self.__Coming_Soon = coming_soon

    def update_shown(self, shown):
        self.__Shown = shown

    def display_cinema_id(self):
        return self.__Cinema_Id

    def display_cinema_name(self):
        return self.__Cinema_name

    def display_showing_now(self):
        return self.__Showing_Now

    def display_coming_soon(self):
        return self.__Coming_Soon

    def display_shown(self):
        return self.__Shown


the_cinema = Cinema(1234, "example")
is_continue = 1
print("Welcome to my little program :D!")
while is_continue == 1:
    print("-" * 100)
    print(menu)
    the_input = input("please enter 1 to 7 for the corresponding operation: ")
    print("\n\n\n\n")

    if the_input == "1":
        the_list = the_cinema.display_coming_soon()
        the_list.append(input("please input the new coming soon movie name: "))
        the_cinema.update_coming_soon(the_list)

    elif the_input == "2":
        shows = the_cinema.display_coming_soon()
        if len(shows) == 0:
            print("you have no coming soon movie!!!!")
            continue

        print("Coming soon movie list: ")

        i = 0
        for show in shows:
            i += 1
            print(f"{i}) {show}, ", end='')

        print('')
        checking = 1
        the_number = None
        while checking == 1:
            the_number = input("please enter number for adding the corresponding show into showing now: ")
            for x in range(1, i+1):
                if the_number == f"{x}":
                    checking = 0
            if checking == 1:
                print("invalid input! you have to input again!")
        the_list = the_cinema.display_coming_soon()
        the_show = the_list.pop(int(the_number) - 1)
        the_cinema.update_coming_soon(the_list)
        the_list = the_cinema.display_showing_now()
        the_list.append(the_show)
        the_cinema.update_showing_now(the_list)

    elif the_input == "3":
        shows = the_cinema.display_showing_now()
        if len(shows) == 0:
            print("you have no showing movie!!!!")
            continue
        i = 0
        for show in shows:
            i += 1
            print(f"{i}) {show}, ", end='')

        print('')
        print("Showing now movie list: ")
        checking = 1
        the_number = None
        while checking == 1:
            the_number = input("please enter number to remove the corresponding show in showing now: ")
            for x in range(1, i + 1):
                if the_number == f"{x}":
                    checking = 0
            if checking == 1:
                print("invalid input! you have to input again!")
        the_list = the_cinema.display_showing_now()
        the_show = the_list.pop(int(the_number) - 1)
        the_cinema.update_showing_now(the_list)
        the_list = the_cinema.display_shown()
        the_list.append(the_show)
        the_cinema.update_shown(the_list)
    elif the_input == "4":
        print(f"here is the coming soon movie list {the_cinema.display_coming_soon()}")
    elif the_input == "5":
        print(f"here is the showing now movie list {the_cinema.display_showing_now()}")
    elif the_input == "6":
        print(f"here is the shown movie list {the_cinema.display_shown()}")
    elif the_input == "7":
        is_continue = 0
        f = open("output.txt", 'w')
        f.write(f"cinema id: {the_cinema.display_cinema_id()}\n")
        f.write(f"cinema name: {the_cinema.display_cinema_name()}\n")
        f.write(f"coming soon: {the_cinema.display_coming_soon()}\n")
        f.write(f"showing now: {the_cinema.display_showing_now()}\n")
        f.write(f"shown: {the_cinema.display_shown()}\n")
        f.close()

    else:
        print("invalid input!! you have to input it again!!")
