import os
import sys
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
import threading

if not os.path.exists('yt-dlp.exe'):
    print('Downloading yt-dlp...')
    subprocess.run(['curl', '-L', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', '-o', 'yt-dlp.exe'])

def download_link(link, folder_name):
    # utworzenie nowego folderu, jeśli nie istnieje
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # pobranie filmu i zapisanie go w nowym folderze
    try:
        subprocess.run(['yt-dlp.exe', '-o', f'{folder_name}/%(title)s.%(ext)s', 'https://www.cda.pl' + link])
    except Exception as e:
        print(f'Error downloading video: {e}')

if __name__ == '__main__':
    # pobranie linku do folderu od użytkownika
    user_link = str(input("Podaj link do folderu: "))
    
    try:
        page = requests.get(user_link)
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas pobierania strony: {e}")
        sys.exit(1)

    soup = BeautifulSoup(page.content, 'html.parser')

    # znalezienie linków do filmów na stronie
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/video/'):
            links.append(href)

    # usunięcie duplikatów z listy links
    links = list(dict.fromkeys(links))

    # pobranie nazwy folderu od użytkownika
    folder_name = str(input("Podaj nazwę folderu (lub zostaw puste dla domyślnej nazwy): ")).strip()

    # użycie domyślnej nazwy folderu, jeśli użytkownik nie podał nazwy
    if not folder_name:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f'pobrane_filmy_{date_time}'

    # pobranie każdego filmu po kolei
    threads = []
    for link in links:
        t = threading.Thread(target=download_link, args=(link, folder_name))
        t.start()
        threads.append(t)

    # oczekiwanie na zakończenie wszystkich wątków
    for t in threads:
        t.join()
