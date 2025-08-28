# Dokumentacja Notes Manager 3000

## 1. Architektura

Aplikacja składa się z dwóch głównych części:

* **Backend**:

  * Framework: **FastAPI**
  * BD: **SQLModel** (nad SQLite)
  * Obsługa REST API: CRUD dla notatek

* **Frontend**:

  * Framework: **Vue 3 (Composition API)** + **Vite**
  * Stylowanie: **SCSS**
  * Funkcjonalności:

    * Dashboard z listą notatek (sortowanie, filtrowanie, wyszukiwanie)
    * Widok pojedynczej notatki (edycja, usuwanie, ulubione)
    * Toasty (`vue3-toastify`) do powiadomień
    * Responsywność (`@media`)

* **Testy**:

  * Backend: **pytest** + FastAPI `TestClient`
  * Frontend: **Vitest** + `@vue/test-utils`

---

## 2. Instalacja

Zbuduj Dockerfile

---

## 3. Uruchamianie

### Backend

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 --reload-dir backend
```

API dostępne pod: `http://localhost:8000/api/v1/notes`

### Frontend (dev)

```bash
cd frontend
npm run dev
```

Frontend: `http://localhost:5173`

Aplikację testujemy w środowisku deweloperskim.

---

## 4. Backend – API

### Model `Note`

* `id: int`
* `title: str`
* `content: str`
* `is_favourite: bool`
* `created_at: datetime`
* `updated_at: datetime`

### Endpointy

#### GET `/api/v1/notes`

Lista notatek.

* Parametry:

  * `query`: filtr tytułu
  * `favourite`: `true|false`
  * `sort`: `created_desc|created_asc|updated_desc|updated_asc`
* Zwraca: listę notatek.

#### GET `/api/v1/notes/{id}`

Pobranie notatki po ID.

#### POST `/api/v1/notes`

Tworzenie nowej notatki.

* Body: `{ title: str, content: str, isFavourite: bool }`

#### PATCH `/api/v1/notes/{id}`

Aktualizacja notatki.

* Body: pola do zmiany (`title`, `content`, `isFavourite`)

#### DELETE `/api/v1/notes/{id}`

Usunięcie notatki.

---

## 5. Frontend – funkcjonalności

### Dashboard

* Wyświetla listę notatek:

  * sekcja **Ulubione**
  * sekcja **Pozostałe**
* Sortowanie: domyślnie najnowsze
* Filtrowanie: checkbox „tylko ulubione”
* Wyszukiwanie: input (z debouncingiem 300ms)
* Każda notatka: komponent `NoteCard`

### Note view

* Edycja tytułu i treści
* Przyciski akcji:

  * ✔ zapisz (toast success/error)
  * ✖ usuń (redirect)
  * ☆/★ toggle favourite
* Walidacja: tytuł wymagany (toast error)
* Nieistniejąca notatka -> przekierowanie do listy notatek

### Komponent `NoteCard`

* Grid z tytułem, treścią skróconą, ikoną ulubionych i usuwania
* Emituje eventy: `open`, `toggle-favourite`, `delete`

---

## 6. Stylowanie

* Zmienne SCSS w `variables.scss`
* Responsywność: media queries `max-width: 768px`
* Grid w `NoteCard` dopasowany do szerokości
* Na mobilkach elementy w kolumnach

---

## 7. Testy

### Backend (`pytest`)

* Uruchomienie:
```bash
cd backend
pytest
```

* `test_create_note_returns_201_and_json`
* `test_list_contains_created_note`
* `test_patch_note_updates_isFavourite`
* `test_delete_note_returns_204`
* `test_get_deleted_note_returns_404`

### Frontend (`Vitest`)

* Uruchomienie:
```bash
cd frontend
npm run test
```

* `NoteCard.spec.ts`:

  * kliknięcie karty → emituje `open`
  * kliknięcie gwiazdki → `toggle-favourite`
  * kliknięcie krzyżyka → `delete`

## 8. Potencjalne zmiany
* Zamiana prymitywnych "czcionkowych" ikon na ładne svg stworzone faktycznie dla tej aplikacji
* Podgląd notatki widoczny obok listy notatek - zembeddowany router view obok
* Udostępnianie notatek innym i wspólna edycja poprzez websocket
* Jakiekolwiek zabezpieczenie API
* Zapisywanie notatek poprzez websocket - usunięcie przycisku "zapisz"
* Ładniejsze okno confirm, zamiast domyślnego przeglądarkowego
* Obsługa gestów na telefonie - przeciągnięcie na bok otwiera listę notatek w formie menu

Oczywiście wiadomo jak to jest. Fajnie pomyśleć sobie o takich zmianach, ale w ramach projektu rekrutacyjnego nie ma to za wiele sensu. Z kolei gdybym miał tworzyć faktycznego konkurenta dla znanych aplikacji notatkowych, pewnie po prostu zacząłbym od sprawdzenia, co one oferują i co dałoby się w nich zmonetyzować. Na tej podstawie można łatwo wybrać, jakie ulepszenia byłyby zupełnie konieczne do bycia konkurencyjnym, a jakie to tylko kosmetyka.