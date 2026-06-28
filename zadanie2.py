class Book:
    def __init__(self, title, author, total_copies):
        self._title = title
        self._author = author
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def total_copies(self):
        return self._total_copies

    @property
    def available_copies(self):
        return self._available_copies

    def borrow(self):
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def return_book(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1
            return True
        return False

    def __str__(self):
        return f"{self._title} - {self._author} (dostępnych: {self._available_copies}/{self._total_copies})"


class User:
    def __init__(self, login, password, role):
        self._login = login
        self._password = password
        self._role = role

    @property
    def login(self):
        return self._login

    @property
    def role(self):
        return self._role

    def check_password(self, password):
        return self._password == password

    def __str__(self):
        return f"{self._login} ({self._role})"


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "reader")
        self._borrowed = []
        self._extension_requests = []

    @property
    def borrowed(self):
        return self._borrowed

    @property
    def extension_requests(self):
        return self._extension_requests

    def add_borrowed(self, book):
        self._borrowed.append(book)

    def remove_borrowed(self, book):
        if book in self._borrowed:
            self._borrowed.remove(book)
            return True
        return False

    def request_extension(self, book):
        if book in self._borrowed and book not in self._extension_requests:
            self._extension_requests.append(book)
            return True
        return False

    def remove_extension_request(self, book):
        if book in self._extension_requests:
            self._extension_requests.remove(book)


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "librarian")


class Library:
    def __init__(self):
        self._books = []
        self._users = []

    def add_book(self, book):
        self._books.append(book)

    def add_user(self, user):
        self._users.append(user)

    def find_book(self, title):
        for book in self._books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_user(self, login):
        for user in self._users:
            if user.login == login:
                return user
        return None

    def authenticate(self, login, password):
        user = self.find_user(login)
        if user and user.check_password(password):
            return user
        return None

    def get_all_books(self):
        return self._books

    def get_all_borrowings(self):
        return [
            (user.login, book)
            for user in self._users
            if isinstance(user, Reader)
            for book in user.borrowed
        ]

    def get_all_extension_requests(self):
        return [
            (user, book)
            for user in self._users
            if isinstance(user, Reader)
            for book in user.extension_requests
        ]

    def borrow_book(self, reader, title):
        book = self.find_book(title)
        if not book:
            print("Nie znaleziono książki.")
            return
        if book.borrow():
            reader.add_borrowed(book)
            print(f"Wypożyczono: {book.title}")
        else:
            print("Brak dostępnych egzemplarzy.")

    def return_book(self, reader, title):
        book = self.find_book(title)
        if not book:
            print("Nie znaleziono książki.")
            return
        if reader.remove_borrowed(book):
            book.return_book()
            print(f"Zwrócono: {book.title}")
        else:
            print("Nie masz tej książki.")


def login(library):
    for attempt in range(3):
        login_input = input("Login: ")
        password_input = input("Hasło: ")
        user = library.authenticate(login_input, password_input)
        if user:
            print(f"Zalogowano jako {user}")
            return user
        print(f"Błędne dane. Pozostało prób: {2 - attempt}")
    print("Przekroczono limit prób. Program zakończony.")
    exit()


def reader_menu(library, user):
    while True:
        print("\n1. Przeglądaj katalog")
        print("2. Wypożycz książkę")
        print("3. Zwróć książkę")
        print("4. Moje wypożyczenia")
        print("5. Poproś o przedłużenie")
        print("0. Wyloguj")
        choice = input("Wybór: ")
        if choice == "1":
            for book in library.get_all_books():
                print(book)
        elif choice == "2":
            title = input("Tytuł: ")
            library.borrow_book(user, title)
        elif choice == "3":
            title = input("Tytuł: ")
            library.return_book(user, title)
        elif choice == "4":
            if not user.borrowed:
                print("Brak wypożyczonych książek.")
            else:
                for book in user.borrowed:
                    print(f"- {book}")
        elif choice == "5":
            title = input("Tytuł: ")
            book = library.find_book(title)
            if book and user.request_extension(book):
                print("Prośba o przedłużenie wysłana.")
            else:
                print("Nie można wysłać prośby.")
        elif choice == "0":
            print("Wylogowano.")
            break
        else:
            print("Nieznana opcja.")


def librarian_menu(library, user):
    while True:
        print("\n1. Przeglądaj katalog")
        print("2. Wszystkie wypożyczenia")
        print("3. Prośby o przedłużenie")
        print("0. Wyloguj")
        choice = input("Wybór: ")
        if choice == "1":
            for book in library.get_all_books():
                print(book)
        elif choice == "2":
            borrowings = library.get_all_borrowings()
            if not borrowings:
                print("Brak wypożyczeń.")
            else:
                for login_name, book in borrowings:
                    print(f"{login_name}: {book}")
        elif choice == "3":
            requests = library.get_all_extension_requests()
            if not requests:
                print("Brak próśb.")
            else:
                for reader, book in requests:
                    print(f"{reader.login} prosi o przedłużenie: {book.title}")
                    decision = input("Zatwierdź (t/n): ")
                    reader.remove_extension_request(book)
                    if decision.lower() == "t":
                        print("Przedłużenie zatwierdzone.")
                    else:
                        print("Przedłużenie odrzucone.")
        elif choice == "0":
            print("Wylogowano.")
            break
        else:
            print("Nieznana opcja.")


def init_library():
    library = Library()
    for book in [
        Book("Władca Pierścieni", "J.R.R. Tolkien", 3),
        Book("Harry Potter i Kamień Filozoficzny", "J.K. Rowling", 2),
        Book("Dune", "Frank Herbert", 1),
        Book("1984", "George Orwell", 4),
        Book("Solaris", "Stanisław Lem", 2),
    ]:
        library.add_book(book)
    for user in [
        Reader("jan", "haslo123"),
        Reader("anna", "tajne456"),
        Reader("piotr", "qwerty789"),
        Librarian("bibliotekarz", "admin123"),
    ]:
        library.add_user(user)
    return library


def main():
    library = init_library()
    user = login(library)
    if user.role == "librarian":
        librarian_menu(library, user)
    else:
        reader_menu(library, user)


if __name__ == "__main__":
    main()
