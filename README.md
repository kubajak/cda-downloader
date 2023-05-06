<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Pobieranie filmów z serwisu CDA.pl</h1>
    <p>Ten skrypt umożliwia pobieranie filmów z serwisu CDA.pl.</p>
    <h2>Jak korzystać z tego skryptu?</h2>
    <ol>
        <li>git clone https://github.com/kubajak/cda-downloader.git</li>
        <li>Pobierz plik <code>yt-dlp.exe</code> i umieść go w tym samym folderze co plik z kodem.</li>
        <li>Uruchom plik z kodem.</li>
        <li>Podaj link do folderu użytkownika na CDA.pl.</li>
        <li>Skrypt pobierze linki do filmów i rozpocznie pobieranie każdego filmu po kolei.</li>
    </ol>
    <h2>Wymagania</h2>
    <p>Do uruchomienia tego skryptu wymagane są następujące biblioteki:</p>
    <ul>
        <li>requests</li>
        <li>BeautifulSoup</li>
    </ul>
    <p>Można je zainstalować przy użyciu polecenia:</p>
    <pre>python -m pip install -r requirements.txt</pre>
    <p>Powyższe polecenie zainstaluje wymagane biblioteki z pliku <code>requirements.txt</code>.</p>
    <div>
        <strong>Uwaga:</strong> Pobieranie filmów z serwisu CDA.pl może naruszać prawa autorskie. Korzystaj z tego skryptu tylko w celach edukacyjnych i zgodnie z prawem.
    </div>
</body>
</html>
