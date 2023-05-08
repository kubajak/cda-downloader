import os
import sys
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

if not os.path.exists('yt-dlp.exe'):
    print('Downloading yt-dlp...')
    subprocess.run(['curl', '-L', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', '-o', 'yt-dlp.exe'])

def download_link(link, folder_name):
    # utworzenie nowego folderu, jeśli nie istnieje
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # pobranie filmu i zapisanie go w nowym folderze
    subprocess.run(['yt-dlp.exe', '-o', f'{folder_name}/%(title)s.%(ext)s', 'https://www.cda.pl' + link])

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

    # pobranie nazwy folderu od użytkownika
    folder_name = str(input("Podaj nazwę folderu (lub zostaw puste dla domyślnej nazwy): ")).strip()

    # użycie domyślnej nazwy folderu, jeśli użytkownik nie podał nazwy
    if not folder_name:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f'pobrane_filmy_{date_time}'

    # pobranie każdego filmu po kolei
    for link in links:
        download_link(link, folder_name)
