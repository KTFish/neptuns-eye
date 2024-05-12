#!/bin/bash
# Uruchomienie skryptu do pobierania pliku
poetry run python /neptuns-eye/neptunseye/fetch_las_files.py

# Uruchomienie głównego skryptu aplikacji
poetry run python /neptuns-eye/neptunseye/main.py