import requests
from typing import Optional, Dict, Any, List

# ============================================================
# BLOK 5 (2h): Obsługa API z użyciem biblioteki requests
# ============================================================
#
# Wersja korzystająca z GOTOWEGO API:
#   BASE_URL = "https://690cb8c2a6d92d83e84f1d7a.mockapi.io/api"
#
# ENDPOINTY:
#   GET  /users           → lista użytkowników
#   PUT  /users/{id}      → aktualizacja użytkownika (np. samego pola "balance")
#
# Przykładowy user:
# {
#   "id": "1",
#   "username": "ala",
#   "balance": 1200
# }
#
# PUT może przyjąć np.:
# {
#   "balance": 1300
# }
#
# ============================================================


BASE_URL = "https://690cb8c2a6d92d83e84f1d7a.mockapi.io/api"


# ------------------------------------------------------------
# [1] Podstawy: GET lista użytkowników, PUT aktualizacja
# ------------------------------------------------------------

def simple_get_users_example():
    """
    Prosty przykład GET:
    - pobierz listę użytkowników
    - wypisz ilu ich jest
    - wypisz kilku pierwszych
    """
    url = f"{BASE_URL}/users"
    print(f"➡️ GET {url}")
    r = requests.get(url, timeout=5)
    print("Status code:", r.status_code)

    if not r.ok:
        print("⚠️ Błąd podczas pobierania użytkowników")
        return

    users = r.json()
    print(f"📋 Liczba użytkowników: {len(users)}")
    print("Przykładowi użytkownicy (max 3):")
    for user in users[:3]:
        print(f"  id={user.get('id')}  username={user.get('username')}  balance={user.get('balance')}")
    print()


def simple_put_balance_example(user_id: str, new_balance: float):
    """
    Prosty przykład PUT:
    - aktualizacja pola balance dla podanego user_id
    """
    url = f"{BASE_URL}/users/{user_id}"
    payload = {"balance": new_balance}
    print(f"➡️ PUT {url} json={payload}")
    r = requests.put(url, json=payload, timeout=5)
    print("Status code:", r.status_code)

    if not r.ok:
        print("⚠️ Błąd podczas aktualizacji użytkownika")
        return

    updated = r.json()
    print("✅ Zaktualizowany użytkownik:", updated)
    print()


# # Demonstracja:
# simple_get_users_example()
# simple_put_balance_example("1", 1500)


# # ZADANIE 1:
# # - Napisz funkcję:
# #     get_user_by_id(user_id: str) -> dict | None
# #   która:
# #     1. pobierze listę użytkowników (GET /users)
# #     2. znajdzie użytkownika o danym id
# #     3. zwróci go (lub None jeśli nie ma takiego)
# # - Przetestuj dla istniejącego i nieistniejącego id.


# ------------------------------------------------------------
# [2] Statusy HTTP i parsowanie JSON (pomocnicze funkcje)
# ------------------------------------------------------------

def print_response_info(response: requests.Response) -> None:
    """Pomocnicza funkcja do wypisywania podstawowych info o odpowiedzi."""
    print("=== RESPONSE INFO ===")
    print("Status:", response.status_code)
    print("OK?   :", response.ok)
    print("Headers (skrócone):")
    for k, v in list(response.headers.items())[:5]:
        print(f"  {k}: {v}")
    print()


def parse_json_safely(response: requests.Response) -> Optional[Dict[str, Any]]:
    """Bezpieczne parsowanie JSON z obsługą wyjątków."""
    try:
        data = response.json()
        if isinstance(data, dict):
            keys = list(data.keys())
        else:
            keys = ["<lista / inny typ>"]
        print("JSON OK, informacje o strukturze:", keys)
        return data
    except ValueError:
        print("⚠️ Odpowiedź nie jest poprawnym JSON-em!")
        return None


# # Demonstracja:
# r = requests.get(f"{BASE_URL}/users", timeout=5)
# print_response_info(r)
# data = parse_json_safely(r)
# print("Typ danych:", type(data))
# print()


# # ZADANIE 2:
# # - Napisz funkcję validate_user_structure(user: dict) -> bool,
# #   która sprawdzi, czy user ma klucze: "id", "username", "balance".
# # - Przejdź po liście użytkowników z GET /users i:
# #     * policz ilu ma poprawną strukturę
# #     * ilu ma niepoprawną (brak któregoś klucza)
# #   Wynik wypisz w konsoli.


# ------------------------------------------------------------
# [3] Klasa ApiClient do pracy z Twoim API
# ------------------------------------------------------------

class ApiClient:
    """
    Prosty klient API do pracy z Twoim mock API użytkowników.
    Używa:
      - requests.Session
      - bazowego URL-a
      - przechowuje last_response do późniejszych asercji
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.last_response: Optional[requests.Response] = None

    def _url(self, path: str) -> str:
        """Łączy base_url i ścieżkę endpointu."""
        if not path.startswith("/"):
            path = "/" + path
        return self.base_url + path

    # ------------------- NISKIPOZIOMOWE METODY GET/PUT ------------------

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """Wykonuje żądanie GET z obsługą błędów sieciowych."""
        url = self._url(path)
        try:
            print(f"➡️ GET {url} params={params}")
            r = self.session.get(url, params=params, timeout=5)
            self.last_response = r
            print(f"⬅️ status: {r.status_code}")
            return r
        except requests.exceptions.RequestException as e:
            print("⚠️ Błąd połączenia przy GET:", e)
            self.last_response = None
            return None

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """Wykonuje żądanie PUT z obsługą błędów sieciowych."""
        url = self._url(path)
        try:
            print(f"➡️ PUT {url} json={json}")
            r = self.session.put(url, json=json, timeout=5)
            self.last_response = r
            print(f"⬅️ status: {r.status_code}")
            return r
        except requests.exceptions.RequestException as e:
            print("⚠️ Błąd połączenia przy PUT:", e)
            self.last_response = None
            return None

    # ------------------- WYSOKOPOZIOMOWE METODY API --------------------

    def get_users(self) -> Optional[List[Dict[str, Any]]]:
        """Pobiera listę użytkowników (GET /users)."""
        r = self.get("/users")
        if r is None or not r.ok:
            print("❌ Nie udało się pobrać listy użytkowników.")
            return None
        try:
            users = r.json()
        except ValueError:
            print("❌ /users nie zwróciło poprawnego JSON-a")
            return None
        print(f"📋 Pobranie użytkowników OK, liczba: {len(users)}")
        return users

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Znajduje użytkownika o danym ID.
        Implementacja:
          - pobieramy listę userów
          - filtrujemy po id
        (Można by też użyć GET /users/{id}, jeśli API to wspiera)
        """
        r = self.get(f"/users/{user_id}")
        if r is None or not r.ok:
            print("❌ Nie udało się pobrać użytkownika.")
            return None
        try:
            user = r.json()
        except ValueError:
            print(f"❌ /users/{user_id} nie zwróciło poprawnego JSON-a")
            return None
        if user is None:
            print(f"⚠️ Nie znaleziono usera o id={user_id}")
            return None
        return user

    def update_user_balance(self, user_id: str, new_balance: float) -> Optional[Dict[str, Any]]:
        """
        Aktualizuje pole balance użytkownika (PUT /users/{id}).
        """
        payload = {"balance": new_balance}
        r = self.put(f"/users/{user_id}", json=payload)
        if r is None or not r.ok:
            print("❌ Nie udało się zaktualizować balansu.")
            return None
        try:
            updated = r.json()
        except ValueError:
            print("❌ Odpowiedź z PUT nie jest JSON-em.")
            return None
        print(f"✅ Zaktualizowany balans usera {user_id}: {updated}")
        return updated

    def change_balance_by(self, user_id: str, delta: float) -> Optional[Dict[str, Any]]:
        """
        Zmienia balans użytkownika o delta (może być dodatnie lub ujemne):
          1. pobierz usera
          2. policz new_balance = current_balance + delta
          3. wyślij PUT z nowym balansem
        """
        user = self.get_user_by_id(user_id)
        if user is None:
            print("❌ Nie można zmienić balansu — user nie istnieje.")
            return None

        current_balance = user.get("balance", 0)
        try:
            current_balance = float(current_balance)
        except (TypeError, ValueError):
            print("❌ balance nie jest liczbą, nie można zmienić.")
            return None

        new_balance = current_balance + delta
        print(f"💰 Zmiana balansu usera {user_id}: {current_balance} -> {new_balance}")
        return self.update_user_balance(user_id, new_balance)

    # --------------------------------------------------------
    # Prosta walidacja statusu
    # --------------------------------------------------------

    def assert_last_status(self, expected: int):
        """
        Asercja ostatniego statusu HTTP.
          - jeśli brak last_response → wypisz komunikat
          - jeśli status != expected → rzuć AssertionError
          - jeśli OK → wypisz „STATUS OK”
        """
        if self.last_response is None:
            print("⚠️ Brak last_response – nie mogę sprawdzić statusu.")
            return

        actual = self.last_response.status_code
        if actual != expected:
            raise AssertionError(f"Status {actual}, oczekiwano {expected}")
        print(f"✅ STATUS OK (oczekiwano i otrzymano {expected})")


# # Demonstracja podstaw ApiClient:
# client = ApiClient(BASE_URL)
# all_users = client.get_users()
# if all_users:
#     first_id = all_users[0]["id"]
#     client.get_user_by_id(first_id)
#     client.change_balance_by(first_id, 100)
#     client.assert_last_status(200)


# # ZADANIE 3:
# # - Napisz test:
# #     1. pobierz listę userów
# #     2. wybierz usera (np. pierwszego)
# #     3. zapamiętaj jego balance
# #     4. zmień balance o +50 (change_balance_by)
# #     5. pobierz usera ponownie i sprawdź:
# #          new_balance == old_balance + 50
# #        - jeśli nie → rzuć AssertionError
# # - Obsłuż w try/except AssertionError i wypisz
# #   „TEST OK” albo „TEST FAIL”.


# ------------------------------------------------------------
# [4] Mini „scenariusz testowy” – symulacja spina
# ------------------------------------------------------------

def run_demo_scenario():
    """
    Mały scenariusz testowy:
      1. Pobierz listę użytkowników.
      2. Wybierz jednego (np. pierwszego) jako „gracza”.
      3. Zapisz jego początkowy balance.
      4. Zasymuluj „spina”:
           - koszt spina: bet_amount
           - wygrana: win_amount
           - nowy balans: balance - bet_amount + win_amount
         (aktualizacja przez PUT /users/{id})
      5. Pobierz usera ponownie i sprawdź, czy balans się zgadza.
    """
    print("=== DEMO SCENARIUSZ: SPIN NA MOCK API ===")
    client = ApiClient(BASE_URL)

    print("\n[1] Pobieranie listy użytkowników")
    users = client.get_users()
    if not users:
        print("❌ Brak użytkowników – nie ma na kim testować.")
        return

    player = users[0]
    player_id = player.get("id")
    print(f"🎮 Wybrany gracz: id={player_id}, username={player.get('username')}")

    try:
        start_balance = float(player.get("balance", 0))
    except (TypeError, ValueError):
        print("❌ balance nie jest liczbą – przerwanie scenariusza.")
        return

    print(f"💰 Początkowy balance: {start_balance}")

    print("\n[2] Symulacja spina")
    bet_amount = 10.0
    win_amount = 15.0
    print(f"   bet_amount = {bet_amount}, win_amount = {win_amount}")

    expected_balance = start_balance - bet_amount + win_amount
    print(f"   Oczekiwany balans po spinie: {expected_balance}")

    updated_user = client.update_user_balance(player_id, expected_balance)
    if updated_user is None:
        print("❌ Nie udało się zaktualizować balansu – koniec scenariusza.")
        return

    print("\n[3] Walidacja balansu – pobranie usera ponownie")
    refreshed_user = client.get_user_by_id(player_id)
    if refreshed_user is None:
        print("❌ Nie udało się ponownie pobrać usera.")
        return

    try:
        final_balance = float(refreshed_user.get("balance", 0))
    except (TypeError, ValueError):
        print("❌ final_balance nie jest liczbą – przerwanie.")
        return

    print(f"💰 Balans po spinie (z API): {final_balance}")

    print("\n[4] Prosta asercja na balans")
    try:
        assert final_balance == expected_balance, (
            f"Balans zły! final={final_balance}, expected={expected_balance}"
        )
    except AssertionError as e:
        print("❌ TEST FAIL:", e)
    else:
        print("✅ TEST OK – balans po spinie jest poprawny.")

    print("=== KONIEC SCENARIUSZA ===\n")


# Demonstracja (odkomentuj, aby odpalić scenariusz z terminala):
if __name__ == "__main__":
    run_demo_scenario()

# # ZADANIE 4 (domknięcie bloku 5):
# # - Zmodyfikuj run_demo_scenario tak, aby:
# #     1. wykonywać kilka spinów w pętli (np. 5 razy):
# #           - za każdym razem inne bet_amount i win_amount
# #     2. sumować wszystkie win_amount do zmiennej total_win
# #     3. po zakończeniu:
# #           - wypisać total_win
# #           - rzucić AssertionError, jeśli total_win == 0
# #             (symulacja „brak wygranych → test niezaliczony”)
# # - Obsłuż AssertionError i wypisz „SCENARIUSZ OK” lub „SCENARIUSZ FAIL”.
