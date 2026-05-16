# Zadanie 2 - Biblioteka OOP

Rozwiazanie zadania z zajec 2 z programowania wysokopoziomowego.

Program jest obiektowa wersja aplikacji biblioteki. Zawiera:

- klase `Book`,
- klase bazowa `User`,
- klasy pochodne `Reader` i `Librarian`,
- klase `Library` z logika biznesowa,
- hermetyzacje przez pola chronione i properties,
- metode `__str__`,
- osobne menu dla czytelnika i bibliotekarza,
- liste wszystkich wypozyczen dla bibliotekarza,
- prosby czytelnikow o przedluzenie i ich obsluge przez bibliotekarza.

## Uruchomienie

```bash
python biblioteka_oop.py
```

## Dane testowe

| Login | Haslo | Rola |
| --- | --- | --- |
| anna | haslo123 | czytelnik |
| marek | qwerty | czytelnik |
| kasia | biblioteka | czytelnik |
| admin | admin123 | bibliotekarz |
