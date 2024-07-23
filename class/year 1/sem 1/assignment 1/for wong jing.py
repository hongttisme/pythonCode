def choose(the_range):
    c = input("Enter your choice: ")
    for i in range(1, the_range + 1):
        if f"{i}" == c:
            return c
    print("wrong input!, please enter again!")
    return choose(the_range)


class Cinema:
    def __init__(self, the_id, name):
        self.__Cinema_Id = the_id
        self.__Cinema_name = name
        self.__Showing_Now = []
        self.__Coming_Soon = []
        self.__Shown = []

    def update_cinema_id(self, the_id):
        self.__Cinema_Id = the_id

    def update_cinema_name(self, cinema_name):
        self.__Cinema_name = cinema_name

    def update_movie_coming_soon(self, movies):
        self.__Coming_Soon = movies

    def update_movie_showing_now(self, movies):
        self.__Showing_Now = movies

    def update_movie_shown(self, movies):
        self.__Shown = movies

    def display_cinema_id(self):
        return self.__Cinema_Id

    def display_cinema_name(self):
        return self.__Cinema_name

    def display_movie_coming_soon(self):
        return self.__Coming_Soon

    def display_movie_showing_now(self):
        return self.__Showing_Now

    def display_movie_shown(self):
        return self.__Shown


cinema = Cinema("AIT2304", "Wong Jing Cinema")

while True:
    print("\nMenu")
    print("1. Add new movie to Coming Soon")
    print("2. Add new movie to Showing Now")
    print("3. Remove a movie from Showing Now")
    print("4. Print Coming Soon list")
    print("5. Print Showing Now list")
    print("6. Print Shown list")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        movie = input("Enter the name of the movie: ")
        l = cinema.display_movie_coming_soon()
        l.append(movie)
        cinema.update_movie_coming_soon(l)

    elif choice == "2":
        if len(cinema.display_movie_coming_soon()) == 0:
            print("Invalid choice. Please try again.")
            continue
        print("Coming Soon List:")
        a = []
        for movie in cinema.display_movie_coming_soon():
            a.append(movie)
            print(f"{len(a)}. {movie}")
        selection = int(choose(len(a))) - 1
        l = cinema.display_movie_showing_now()
        l.append(cinema.display_movie_coming_soon()[selection])
        cinema.update_movie_showing_now(l)
        l = cinema.display_movie_coming_soon()
        l.remove(cinema.display_movie_coming_soon()[selection])
        cinema.update_movie_coming_soon(l)

    elif choice == "3":
        if len(cinema.display_movie_showing_now()) == 0:
            print("Invalid choice. Please try again.")
            continue
        print("Showing Now List:")
        a = []
        for movie in cinema.display_movie_showing_now():
            a.append(movie)
            print(f"{len(a)}. {movie}")
        selection = int(choose(len(a))) - 1
        l = cinema.display_movie_shown()
        l.append(cinema.display_movie_showing_now()[selection])
        cinema.update_movie_shown(l)
        l = cinema.display_movie_showing_now()
        l.remove(cinema.display_movie_showing_now()[selection])
        cinema.update_movie_showing_now(l)
    elif choice == "4":
        print(cinema.display_movie_coming_soon())
    elif choice == "5":
        print(cinema.display_movie_showing_now())
    elif choice == "6":
        print(cinema.display_movie_shown())
    elif choice == "7":
        print("bye")
        file = open("output.txt", 'w')
        file.write(f"{cinema.display_cinema_id()=}, "
                   f"{cinema.display_cinema_name()=}, "
                   f"{cinema.display_movie_showing_now()=}, "
                   f"{cinema.display_movie_coming_soon()=}, "
                   f"{cinema.display_movie_shown()=}")
        file.close()
        break
    else:
        print("Invalid choice. Please try again.")
