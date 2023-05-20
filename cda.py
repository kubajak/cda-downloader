import os
import sys
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
import threading
import signal
from queue import Queue

def pobierz_ytdlp():
    #Pobierz yt-dlp jeśli nie zostanie znaleziony.
    if not os.path.exists('yt-dlp.exe'):
        print('Pobieranie yt-dlp...')
        try:
            subprocess.run(['curl', '-L', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', '-o', 'yt-dlp.exe'])
        except Exception as e:
            print(f'Błąd podczas pobierania yt-dlp: {e}')
            sys.exit(1)

def utworz_katalog(nazwa_katalogu):
    #Utwórz nowy katalog jeśli nie istnieje.
    try:
        if not os.path.exists(nazwa_katalogu):
            os.makedirs(nazwa_katalogu)
    except OSError as e:
        print(f'Błąd podczas tworzenia katalogu: {e}')
        return False
    return True

def pobierz_film(link, nazwa_katalogu, jakosc):
    #Pobierz film i zapisz go w nowym katalogu.
    try:
        subprocess.run(['yt-dlp.exe', '-f', f'bestvideo[height<=?{jakosc}]+bestaudio/best[height<=?{jakosc}]', '-o', f'{nazwa_katalogu}/%(title)s.%(ext)s', 'https://www.cda.pl' + link])
    except Exception as e:
        print(f'Błąd podczas pobierania filmu: {e}')

def wybierz_jakosc():
    #Pozwól użytkownikowi wybrać jakość pobranego filmu.
    jakosc = input("Wybierz jakość pobranego filmu (480p, 720p lub 1080p): ")
    while jakosc not in ['480p', '720p', '1080p']:
        print("Niepoprawna jakość. Wybierz ponownie.")
        jakosc = input("Wybierz jakość pobranego filmu (480p, 720p lub 1080p): ")
    return jakosc

def pobierz_link_uzytkownika():
    #Pobierz link do katalogu od użytkownika.
    link_uzytkownika = str(input("Podaj link do katalogu: "))
    
    #Sprawdź czy podany link pochodzi z cda.pl i ponownie pytaj o link jeśli nie jest z cda.pl
    while not link_uzytkownika.startswith('https://www.cda.pl'):
        print("Podany link nie jest z cda.pl")
        link_uzytkownika = str(input("Podaj link do katalogu: "))
    return link_uzytkownika

def pobierz_zawartosc_strony(link_uzytkownika):
    #Pobierz zawartość strony pod podanym linkiem.
    try:
        strona = requests.get(link_uzytkownika)
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas pobierania strony: {e}")
        sys.exit(1)
    return strona.content

def pobierz_linki_do_filmow(zawartosc_strony):
    #Znajdź linki do filmów na stronie.
    soup = BeautifulSoup(zawartosc_strony, 'html.parser')
    linki = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/video/'):
            linki.append(href)
    #Usuń duplikaty z listy linków
    linki = list(dict.fromkeys(linki))
    return linki

def pobierz_nazwe_katalogu():
    #Pobierz nazwę katalogu od użytkownika.
    nazwa_katalogu = str(input("Podaj nazwę katalogu (lub zostaw puste dla domyślnej nazwy): ")).strip()
    #Użyj domyślnej nazwy katalogu jeśli użytkownik nie podał nazwy
    if not nazwa_katalogu:
        teraz = datetime.now()
        data_czas = teraz.strftime("%Y-%m-%d_%H-%M-%S")
        nazwa_katalogu = f'pobrane_filmy_{data_czas}'
    return nazwa_katalogu

def wybierz_liczbe_pobieran():
    # Pozwól użytkownikowi wybrać liczbę jednoczesnych pobierań filmów.
    liczba_pobieran = input("Wybierz liczbę jednoczesnych pobierań filmów (lub wpisz 'max' dla pobierania wszystkich na raz): ")
    while not (liczba_pobieran.isdigit() and int(liczba_pobieran) > 0) and liczba_pobieran != 'max':
        print("Niepoprawna liczba pobierań. Wybierz ponownie.")
        liczba_pobieran = input("Wybierz liczbę jednoczesnych pobierań filmów (lub wpisz 'max' dla pobierania wszystkich na raz): ")
    if liczba_pobieran == 'max':
        return float('inf')
    else:
        return int(liczba_pobieran)


def pobierz_filmy(linki, nazwa_katalogu):
    def signal_handler(sig, frame):
        print('Przerywanie pobierania filmów...')
        for t in watki:
            t.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    jakosc = wybierz_jakosc()
    liczba_pobieran = wybierz_liczbe_pobieran()
    watki = []
    q = Queue()
    for link in linki:
        q.put(link)

    def pobierz_film_z_kolejki():
        while not q.empty():
            link = q.get()
            pobierz_film(link, nazwa_katalogu, jakosc)
            q.task_done()

    for i in range(liczba_pobieran):
        t = threading.Thread(target=pobierz_film_z_kolejki)
        t.start()
        watki.append(t)

    q.join()

    # Poczekaj na zakończenie wszystkich wątków
    for t in watki:
        t.join()


if __name__ == '__main__':
    pobierz_ytdlp()
    
    link_uzytkownika = pobierz_link_uzytkownika()
    
    zawartosc_strony = pobierz_zawartosc_strony(link_uzytkownika)
    
    linki = pobierz_linki_do_filmow(zawartosc_strony)
    
    nazwa_katalogu = pobierz_nazwe_katalogu()
    
    if utworz_katalog(nazwa_katalogu):
        pobierz_filmy(linki, nazwa_katalogu)
