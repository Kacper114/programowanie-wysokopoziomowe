books = [
    {"title": "Władca Pierścieni", "author": "J.R.R. Tolkien", "quantity": 3},
    {"title": "Harry Potter i Kamień Filozoficzny", "author": "J.K. Rowling", "quantity": 2},
    {"title": "Dune", "author": "Frank Herbert", "quantity": 1},
    {"title": "1984", "author": "George Orwell", "quantity": 4},
    {"title": "Solaris", "author": "Stanisław Lem", "quantity": 2},
]

users = [
    {"login": "jan", "password": "haslo123", "role": "reader", "borrowed": []},
    {"login": "anna", "password": "tajne456", "role": "reader", "borrowed": []},
    {"login": "piotr", "password": "qwerty789", "role": "reader", "borrowed": []},
]


def find_user(login):
    for user in users:
        if user["login"] == login:
            return user
    return None


def login():
    for attempt in range(3):
        login_input = input("Login: ")
        password_input = input("Hasło: ")
        user = find_user(login_input)
        if user and user["password"] == password_input:
            print(f"Zalogowano jako {user['login']}")
            return user
        print(f"Błędne dane. Pozostało prób: {2 - attempt}")
    print("Przekroczono limit prób. Program zakończony.")
    exit()


def browse_catalog():
    print("\n--- Katalog książek ---")
    for book in books:
        print(f"{book['title']} - {book['author']} (dostępnych: {book['quantity']})")


def borrow_book(user):
    title = input("Podaj tytuł książki: ")
    for book in books:
        if book["title"].lower() == title.lower():
            if book["quantity"] > 0:
                book["quantity"] -= 1
                user["borrowed"].append(book["title"])
                print(f"Wypożyczono: {book['title']}")
            else:
                print("Brak dostępnych egzemplarzy.")
            return
    print("Nie znaleziono książki.")


def my_borrowings(user):
    print("\n--- Twoje wypożyczenia ---")
    if not user["borrowed"]:
        print("Brak wypożyczonych książek.")
    else:
        for title in user["borrowed"]:
            print(f"- {title}")


def show_menu():
    print("\n1. Przeglądaj katalog")
    print("2. Wypożycz książkę")
    print("3. Moje wypożyczenia")
    print("0. Wyloguj")


def main():
    user = login()
    while True:
        show_menu()
        choice = input("Wybór: ")
        if choice == "1":
            browse_catalog()
        elif choice == "2":
            borrow_book(user)
        elif choice == "3":
            my_borrowings(user)
        elif choice == "0":
            print("Wylogowano.")
            break
        else:
            print("Nieznana opcja.")


if __name__ == "__main__":
    main()
