

nazwa_pliku = input("Podaj nazwe pliku: ")

with open(nazwa_pliku, 'rb') as plik_wejsciowy:
    zawartosc = plik_wejsciowy.read()

with open('lab1zad.png', 'wb') as plik_wyjsciowy:
    plik_wyjsciowy.write(zawartosc)

