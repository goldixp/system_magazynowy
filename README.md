# System Zarządzania Magazynem

Zintegrowany system informatyczny usprawniający zarządzanie magazynem. Program umożliwia śledzenie produktów za pomocą unikalnych kodów SKU, rejestrację dostaw oraz wydań, a także integrację z systemem generowania kodów QR.

## Wykorzystane technologie:
* **Backend:** Python 3.x / Django Framework
* **Baza danych:** PostgreSQL
* **Konteneryzacja:** Docker & Docker Compose 
* **Infrastruktura CI/CD:** GitHub Actions -> Render 

## Kluczowe Funkcjonalności (W trakcie realizacji)
* Pełna obsługa CRUD dla produktów magazynowych.
* System unikalnych kodów SKU dla każdego towaru.
* Automatyczne alerty o niskim stanie produktów.
* Bezpieczna obsługa współbieżności przy jednoczesnych operacjach na bazie danych.
* Integracja zewnętrzna (Generowanie kodów QR dla produktów).

## Instrukcja Uruchomienia (Środowisko lokalne)
1. Sklonuj repozytorium.
2. Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python -m venv venv
   venv\Scripts\activate
3. Zainstaluj wymagane pakiety:
   ```bash
   pip install django
4. Uruchom serwer deweloperski:
   python manage.py runserver