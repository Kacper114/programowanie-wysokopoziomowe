books = [
    {"title": "Lalka", "author": "Boleslaw Prus", "available": 3},
    {"title": "Pan Tadeusz", "author": "Adam Mickiewicz", "available": 2},
    {"title": "Quo Vadis", "author": "Henryk Sienkiewicz", "available": 4},
    {"title": "Ferdydurke", "author": "Witold Gombrowicz", "available": 1},
    {"title": "Solaris", "author": "Stanislaw Lem", "available": 2},
]

users = [
    {"login": "anna", "password": "haslo123", "role": "czytelnik", "borrowed": []},
    {"login": "marek", "password": "qwerty", "role": "czytelnik", "borrowed": []},
    {"login": "kasia", "password": "biblioteka", "role": "czytelnik", "borrowed": []},
]


def find_user(login, password):
    for user in users:
        if user["login"] == login and user["password"] == password:
            return user
    return None


def login_user():
    attempts_left = 3

    while attempts_left > 0:
        print("\nLOGOWANIE")
        login = input("Login: ").strip()
        password = input("Haslo: ").strip()

        user = find_user(login, password)
        if user is not None:
            print(f"\nZalogowano jako: {user['login']} ({user['role']})")
            return user

        attempts_left -= 1
        print(f"Niepoprawny login lub haslo. Pozostalo prob: {attempts_left}")

    print("Przekroczono limit prob logowania. Program zostanie zamkniety.")
    return None


def show_catalog():
    print("\nKATALOG KSIAZEK")
    for index, book in enumerate(books, start=1):
        print(
            f"{index}. {book['title']} - {book['author']} "
            f"(dostepne sztuki: {book['available']})"
        )


def find_book_by_title(title):
    searched_title = title.lower()

    for book in books:
        if book["title"].lower() == searched_title:
            return book
    return None


def borrow_book(user):
    print("\nWYPOZYCZENIE KSIAZKI")
    title = input("Podaj tytul ksiazki: ").strip()
    book = find_book_by_title(title)

    if book is None:
        print("Nie znaleziono ksiazki o podanym tytule.")
        return

    if book["available"] <= 0:
        print("Brak dostepnych sztuk tej ksiazki.")
        return

    book["available"] -= 1
    user["borrowed"].append(book["title"])
    print(f"Wypozyczono ksiazke: {book['title']}")


def show_my_borrowed_books(user):
    print("\nMOJE WYPOZYCZENIA")

    if len(user["borrowed"]) == 0:
        print("Nie masz aktualnie wypozyczonych ksiazek.")
        return

    for index, title in enumerate(user["borrowed"], start=1):
        print(f"{index}. {title}")


def show_menu():
    print("\nMENU GLOWNE")
    print("1. Przegladaj katalog")
    print("2. Wypozycz ksiazke")
    print("3. Moje wypozyczenia")
    print("4. Wyloguj")


def handle_menu_choice(choice, user):
    if choice == "1":
        show_catalog()
        return True

    if choice == "2":
        borrow_book(user)
        return True

    if choice == "3":
        show_my_borrowed_books(user)
        return True

    if choice == "4":
        print("Wylogowano. Do zobaczenia!")
        return False

    print("Niepoprawny wybor. Wybierz opcje od 1 do 4.")
    return True


def main():
    print("SYSTEM BIBLIOTEKI")
    user = login_user()

    if user is None:
        return

    is_running = True
    while is_running:
        show_menu()
        choice = input("Wybierz opcje: ").strip()
        is_running = handle_menu_choice(choice, user)


main()
