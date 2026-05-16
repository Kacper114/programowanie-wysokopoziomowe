class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def total_copies(self):
        return self._total_copies

    @property
    def available_copies(self):
        return self._available_copies

    def borrow(self):
        if self._available_copies <= 0:
            return False

        self._available_copies -= 1
        return True

    def return_copy(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1
            return True

        return False

    def __str__(self):
        return (
            f"{self.title} - {self.author} "
            f"(dostepne: {self.available_copies}/{self.total_copies})"
        )


class User:
    def __init__(self, login, password, role):
        self.login = login
        self._password = password
        self.role = role

    def authenticate(self, password):
        return self._password == password

    def show_menu(self):
        raise NotImplementedError("Ta metoda powinna byc nadpisana w klasie pochodnej.")


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self.borrowed_books = []
        self.extension_requests = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def has_borrowed_book(self, book):
        return book in self.borrowed_books

    def add_extension_request(self, book):
        if book in self.extension_requests:
            return False

        self.extension_requests.append(book)
        return True

    def remove_extension_request(self, book):
        if book in self.extension_requests:
            self.extension_requests.remove(book)

    def show_menu(self):
        print("\nMENU CZYTELNIKA")
        print("1. Przegladaj katalog")
        print("2. Wypozycz ksiazke")
        print("3. Moje wypozyczenia")
        print("4. Popros o przedluzenie")
        print("5. Wyloguj")


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")

    def show_menu(self):
        print("\nMENU BIBLIOTEKARZA")
        print("1. Przegladaj katalog")
        print("2. Lista wszystkich wypozyczen")
        print("3. Obsluga prosb o przedluzenie")
        print("4. Wyloguj")


class Library:
    def __init__(self, books, users):
        self.books = books
        self.users = users
        self.extension_requests = []

    def find_user(self, login):
        for user in self.users:
            if user.login == login:
                return user
        return None

    def login(self):
        attempts_left = 3

        while attempts_left > 0:
            print("\nLOGOWANIE")
            login = input("Login: ").strip()
            password = input("Haslo: ").strip()
            user = self.find_user(login)

            if user is not None and user.authenticate(password):
                print(f"\nZalogowano jako: {user.login} ({user.role})")
                return user

            attempts_left -= 1
            print(f"Niepoprawny login lub haslo. Pozostalo prob: {attempts_left}")

        print("Przekroczono limit prob logowania. Program zostanie zamkniety.")
        return None

    def find_book_by_title(self, title):
        searched_title = title.lower()

        for book in self.books:
            if book.title.lower() == searched_title:
                return book
        return None

    def show_catalog(self):
        print("\nKATALOG KSIAZEK")

        for index, book in enumerate(self.books, start=1):
            print(f"{index}. {book}")

    def borrow_book(self, reader):
        print("\nWYPOZYCZENIE KSIAZKI")
        title = input("Podaj tytul ksiazki: ").strip()
        book = self.find_book_by_title(title)

        if book is None:
            print("Nie znaleziono ksiazki o podanym tytule.")
            return

        if not book.borrow():
            print("Brak dostepnych sztuk tej ksiazki.")
            return

        reader.borrow_book(book)
        print(f"Wypozyczono ksiazke: {book.title}")

    def show_reader_borrowed_books(self, reader):
        print("\nMOJE WYPOZYCZENIA")

        if len(reader.borrowed_books) == 0:
            print("Nie masz aktualnie wypozyczonych ksiazek.")
            return

        for index, book in enumerate(reader.borrowed_books, start=1):
            print(f"{index}. {book.title} - {book.author}")

    def show_all_borrowed_books(self):
        print("\nWSZYSTKIE WYPOZYCZENIA")
        any_borrowed = False

        for user in self.users:
            if isinstance(user, Reader):
                for book in user.borrowed_books:
                    print(f"{user.login}: {book.title} - {book.author}")
                    any_borrowed = True

        if not any_borrowed:
            print("Aktualnie nie ma zadnych wypozyczen.")

    def create_extension_request(self, reader):
        print("\nPROSBA O PRZEDLUZENIE")

        if len(reader.borrowed_books) == 0:
            print("Nie masz wypozyczonych ksiazek.")
            return

        self.show_reader_borrowed_books(reader)
        title = input("Podaj tytul ksiazki do przedluzenia: ").strip()
        book = self.find_book_by_title(title)

        if book is None or not reader.has_borrowed_book(book):
            print("Nie masz wypozyczonej ksiazki o podanym tytule.")
            return

        if not reader.add_extension_request(book):
            print("Prosba o przedluzenie tej ksiazki zostala juz wyslana.")
            return

        self.extension_requests.append({"reader": reader, "book": book})
        print(f"Wyslano prosbe o przedluzenie ksiazki: {book.title}")

    def show_extension_requests(self):
        print("\nPROSBY O PRZEDLUZENIE")

        if len(self.extension_requests) == 0:
            print("Brak prosb o przedluzenie.")
            return

        for index, request in enumerate(self.extension_requests, start=1):
            reader = request["reader"]
            book = request["book"]
            print(f"{index}. {reader.login} prosi o przedluzenie: {book.title}")

    def handle_extension_requests(self):
        self.show_extension_requests()

        if len(self.extension_requests) == 0:
            return

        try:
            request_number = int(input("Podaj numer prosby do obslugi: "))
        except ValueError:
            print("Podano niepoprawny numer.")
            return

        if request_number < 1 or request_number > len(self.extension_requests):
            print("Nie ma prosby o takim numerze.")
            return

        request = self.extension_requests[request_number - 1]
        decision = input("Zaakceptowac prosbe? (t/n): ").strip().lower()

        if decision not in ["t", "n"]:
            print("Niepoprawna decyzja.")
            return

        reader = request["reader"]
        book = request["book"]
        self.extension_requests.remove(request)
        reader.remove_extension_request(book)

        if decision == "t":
            print(f"Zaakceptowano prosbe uzytkownika {reader.login} dla ksiazki: {book.title}")
        else:
            print(f"Odrzucono prosbe uzytkownika {reader.login} dla ksiazki: {book.title}")

    def handle_reader_choice(self, choice, reader):
        if choice == "1":
            self.show_catalog()
            return True

        if choice == "2":
            self.borrow_book(reader)
            return True

        if choice == "3":
            self.show_reader_borrowed_books(reader)
            return True

        if choice == "4":
            self.create_extension_request(reader)
            return True

        if choice == "5":
            print("Wylogowano. Do zobaczenia!")
            return False

        print("Niepoprawny wybor. Wybierz opcje od 1 do 5.")
        return True

    def handle_librarian_choice(self, choice):
        if choice == "1":
            self.show_catalog()
            return True

        if choice == "2":
            self.show_all_borrowed_books()
            return True

        if choice == "3":
            self.handle_extension_requests()
            return True

        if choice == "4":
            print("Wylogowano. Do zobaczenia!")
            return False

        print("Niepoprawny wybor. Wybierz opcje od 1 do 4.")
        return True

    def run(self):
        print("SYSTEM BIBLIOTEKI - WERSJA OBIEKTOWA")
        user = self.login()

        if user is None:
            return

        is_running = True
        while is_running:
            user.show_menu()
            choice = input("Wybierz opcje: ").strip()

            if isinstance(user, Reader):
                is_running = self.handle_reader_choice(choice, user)
            elif isinstance(user, Librarian):
                is_running = self.handle_librarian_choice(choice)


def create_library():
    books = [
        Book("Lalka", "Boleslaw Prus", 3),
        Book("Pan Tadeusz", "Adam Mickiewicz", 2),
        Book("Quo Vadis", "Henryk Sienkiewicz", 4),
        Book("Ferdydurke", "Witold Gombrowicz", 1),
        Book("Solaris", "Stanislaw Lem", 2),
    ]

    users = [
        Reader("anna", "haslo123"),
        Reader("marek", "qwerty"),
        Reader("kasia", "biblioteka"),
        Librarian("admin", "admin123"),
    ]

    return Library(books, users)


def main():
    library = create_library()
    library.run()


if __name__ == "__main__":
    main()
