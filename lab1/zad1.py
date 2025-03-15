

nazwa_pliku = input("Podaj nazwe pliku: ")

with open(nazwa_pliku, 'r') as plik_wejsciowy:
    zawartosc = plik_wejsciowy.read()

with open('lab1zad.txt', 'w') as plik_wyjsciowy:
    plik_wyjsciowy.write(zawartosc)

