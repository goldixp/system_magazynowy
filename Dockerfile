# Używamy odchudzonej (slim) wersji Pythona, co spełnia wymóg optymalizacji z wytycznych
FROM python:3.12-slim

# Ustawiamy zmienne środowiskowe:
# PYTHONDONTWRITEBYTECODE - Python nie będzie tworzył plików .pyc na dysku
# PYTHONUNBUFFERED - logi będą od razu lecieć na konsolę (łatwiejsze debugowanie)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy plik z wymaganiami i instalujemy je (--no-cache-dir zmniejsza rozmiar kontenera!)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą resztę kodu naszego projektu do kontenera
COPY . /app/

# Otwieramy port 8000, na którym domyślnie działa Django
EXPOSE 8000

# Komenda domyślna, która odpali serwer, gdy uruchomimy kontener
CMD "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"