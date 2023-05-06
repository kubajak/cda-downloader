import requests
from bs4 import BeautifulSoup
import subprocess

# funkcja do pobierania jednego linku przy użyciu yt-dlp
def download_link(link):
    subprocess.run(['yt-dlp.exe', 'https://www.cda.pl' + link])

if __name__ == '__main__':
    # pobranie linku do folderu od użytkownika
    user_link = str(input("Podaj link: "))
    page = requests.get(user_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # znalezienie linków do filmów na stronie
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/video/'):
            links.append(href)

    # pobranie każdego filmu po kolei
    for link in links:
        download_link(link)
