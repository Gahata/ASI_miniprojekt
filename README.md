# ASI_miniprojekt
Zadanie zaliczeniowe na zajęcia ASI
Paweł Jezierski s17676

Model przewiduje szansę na deszcz na podstawie danych pogodowych z poprzedniego dnia.


# Działanie
* Github actions działa lokalnie na systemie ubuntu
* Github actions uruchamia całość po git push lub manualnie
1) Uruchamiany jest ETL
* Wczytywane są dane z katalogu /data/raw
* Odrzucane są niepotrzebne kolumny
* Odrzucane są puste kolumny i wiersze
* Dodawane są brakujące dane
* Zapisywane są przetworzone dane do
2) Trenowany i testowany jest  Logistic Regression
3) Uruchamiane jest FastAPI z funkcją predict, która przyjmuje dane i zwraca szansę na deszcz


# Uruchomienie:

Całość uruchamiana jest przez github actions na maszynie lokalnej.

Do uruchomienia manualnie API:
* Otwieramy konsolę w folderze z projektem
* Wykonujemy komendę: 'uvicorn src.api:app --reload'

# Używanie predykcji:
* http://127.0.0.1:8000/docs
* Używamy get /predict z danymi