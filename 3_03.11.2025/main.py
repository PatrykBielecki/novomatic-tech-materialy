import requests
from typing import Dict, Optional, Any, Tuple
# # # ============================================================
# # # BLOK 3 (2h): Funkcje i organizacja logiki testowej
# # # ============================================================

# # ------------------------------------------------------------
# # [1] Pierwszy GET + status_code + prosta decyzja
# # ------------------------------------------------------------
# print("[1] GET + status_code")
# try:
#     import requests
#     url = "https://httpbin.org/status/200"
#     r = requests.get(url, timeout=5)
#     print("URL:", url)
#     print("Kod:", r.status_code)
#     if r.status_code == 200:
#         print("✅ API OK")
#     else:
#         print("❌ API down (kod:", r.status_code, ")")
# except Exception as e:
#     print("Błąd:", e)
# print()

# # ZADANIE 1:
# # - Zmień url na "https://httpbin.org/status/404" i sprawdź komunikat.
# # - Dodaj prosty elif dla 404: wypisz "Nie znaleziono (404)".





# # ------------------------------------------------------------
# # [2] Try/Except — bezpieczne wywołanie (błędna domena)
# # ------------------------------------------------------------
# print("[2] Obsługa wyjątków (błędny adres)")
# import requests
# bad_url = "https://to_nie_istnieje.abc"
# try:
#     r = requests.get(bad_url, timeout=3)
#     print("Kod:", r.status_code)
# except requests.exceptions.RequestException as e:
#     print("Oczekiwany błąd połączenia:", repr(e))
# print()

# # ZADANIE 2:
# # - Zmień timeout na 1 i sprawdź, czy komunikat błędu jest podobny.
# # - Dodaj drugi except dla ogólnego Exception i inny wydruk.





# # ------------------------------------------------------------
# # [3] Nagłówki odpowiedzi — content-type, server
# # ------------------------------------------------------------
# print("[3] Nagłówki odpowiedzi")
# url = "https://api.github.com"
# r = requests.get(url, timeout=5)
# headers: Dict[str, str] = dict(r.headers)
# print("Status:", r.status_code)
# print("content-type:", headers.get("content-type"))
# print("server:", headers.get("server"))
# print()

# # ZADANIE 3:
# # - Jeśli w content-type NIE ma słowa "json" (lowercase), wypisz ostrzeżenie.
# # - Wypisz liczbę wszystkich nagłówków (len(headers)).





# # ------------------------------------------------------------
# # [4] Odczyt treści: .text (surowy) vs .json() (parsowany)
# # ------------------------------------------------------------
# print("[4] .text vs .json()")
# r = requests.get("https://api.github.com", timeout=5)
# print("Krótki podgląd .text (pierwsze 80 znaków):")
# print(r.text[:280].replace("\n", " ") + "...")
# print()

# data: Optional[Dict[str, Any]] = None
# json_err: Optional[Exception] = None
# try:
#     data = r.json()  # spróbuj sparsować JSON
#     print("Klucze w JSON (pierwsze 10):", list(data.keys())[:10])
# except ValueError as e:
#     json_err = e
#     print("To nie jest poprawny JSON:", e)
# print()

# # ZADANIE 4:
# # - Jeśli json_err is None -> wypisz wartość klucza "current_user_url" (jeśli istnieje),
# #   inaczej wypisz "Brak JSON — nie można odczytać current_user_url".
# # - Obsłuż brak klucza przez .get(..., "brak").





# # ------------------------------------------------------------
# # [5] Parsowanie JSON — bezpieczny dostęp i prosta walidacja
# # ------------------------------------------------------------
# print("[5] Parsowanie JSON — bezpieczny dostęp")
# if data is not None:
#     current_user_url = data.get("current_user_url", None)
#     print("current_user_url:", current_user_url)
#     # Prosta walidacja: czy to wygląda na URL (zaczyna się od http)
#     if isinstance(current_user_url, str) and current_user_url.startswith("http"):
#         print("✅ Wygląda OK")
#     else:
#         print("⚠️  Wygląda podejrzanie lub brak")
# else:
#     print("Brak danych JSON do parsowania.")
# print()

# # ZADANIE 5:
# # - Dodaj sprawdzenie, czy istnieje klucz "rate_limit_url".
# # - Wypisz "OK" jeśli jest stringiem zaczynającym się od "http", w przeciwnym razie "NIE OK".




# # ------------------------------------------------------------
# # [6] Funkcja: fetch_json(url) -> (json|None, status, headers, error)
# # ------------------------------------------------------------
# print("[6] Funkcja fetch_json(url)")
# def fetch_json(url: str, timeout: int = 5) -> Tuple[Optional[Dict[str, Any]], int, Dict[str, str], Optional[Exception]]:
#     """
#     Wykonuje GET i próbuje zwrócić JSON.
#     Zwraca: (json|None, status_code, headers, error|None)
#     - Jeśli parsowanie JSON się nie uda, error to ValueError.
#     - Jeśli problem połączenia, error to RequestException (lub inny Exception).
#     """
#     try:
#         resp = requests.get(url, timeout=timeout)
#         hdrs = dict(resp.headers)
#         try:
#             j = resp.json()
#             return j, resp.status_code, hdrs, None
#         except ValueError as ve:
#             return None, resp.status_code, hdrs, ve
#     except Exception as e:
#         return None, -1, {}, e

# data2, status2, headers2, err2 = fetch_json("https://api.github.com")
# print("status:", status2, "| err:", repr(err2))
# if data2:
#     print("Przykładowe klucze:", data2)
# print()

# # ZADANIE 6:
# # - Dodaj parametr retries=3 (domyślnie) i sleep 0.2s między próbami (time.sleep),
# #   spróbuj ponowić, jeśli wystąpi RequestException lub status >=500.
# # - Zwracaj wynik pierwszego sukcesu lub ostatniego błędu.




# # ------------------------------------------------------------
# # [7] Funkcje pomocnicze do JSON: is_json_response, get_in
# # ------------------------------------------------------------
# print("[7] Funkcje pomocnicze do JSON")
# def is_json_response(headers: Dict[str, str]) -> bool:
#     ctype = headers.get("content-type") or headers.get("Content-Type") or ""
#     return "json" in ctype.lower()

# def get_in(d: Dict[str, Any], path: List[str], default: Any = None) -> Any:
#     """
#     Bezpieczne pobieranie zagnieżdżonej wartości.
#     get_in({"a":{"b":1}}, ["a","b"]) -> 1
#     """
#     cur: Any = d
#     for k in path:
#         if not isinstance(cur, dict) or k not in cur:
#             return default
#         cur = cur[k]
#     return cur

# if data2:
#     print("is_json_response:", is_json_response(headers2))
#     print("get_in(['resources','core','limit']):", get_in(data2, ["resources", "core", "limit"], default="brak"))
# print()




# # ------------------------------------------------------------
# # [11] JSONPlaceholder — szybki podgląd danych (GET)
# # ------------------------------------------------------------
# print("[11] JSONPlaceholder: GET podgląd")
# BASE = "https://jsonplaceholder.typicode.com"

# # Lista postów
# r = requests.get(f"{BASE}/posts", timeout=5)
# print("Status /posts:", r.status_code, "| Ile rekordów?:", len(r.json()) if r.ok else 0)

# # Pojedynczy post
# r = requests.get(f"{BASE}/posts/1", timeout=5)
# print("Status /posts/1:", r.status_code)
# print("Post #1 klucze:", list(r.json().keys()) if r.ok else "brak")
# print()

# # Komentarze do konkretnego posta
# r = requests.get(f"{BASE}/posts/1/comments", timeout=5)
# print("Status /posts/1/comments:", r.status_code, "| Liczba komentarzy:", len(r.json()) if r.ok else 0)

# # Filtrowanie po query string
# r = requests.get(f"{BASE}/comments", params={"postId": 1}, timeout=5)
# print("Status /comments?postId=1:", r.status_code, "| Liczba:", len(r.json()) if r.ok else 0)
# print()

# # ZADANIE 11:
# # - Pobierz /users/2 i wypisz name oraz email.
# # - Pobierz /todos?completed=true i policz ile elementów przyszło.




# # ------------------------------------------------------------
# # [12] JSONPlaceholder — POST (tworzenie, symulowane)
# # ------------------------------------------------------------
# print("[12] JSONPlaceholder: POST /posts (symulacja tworzenia)")
# payload = {"title": "mój tytuł", "body": "treść wpisu", "userId": 1}
# r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
# print("Status POST /posts:", r.status_code)
# print("Odpowiedź:", r.json())  # powinno zawierać wygenerowane "id"
# print()

# # ZADANIE 12:
# # - Sprawdź, czy odpowiedź ma pole "id" (if "id" in r.json(): ...).
# # - Zrób drugi POST na /comments z polami: name, email, body, postId.




# # ------------------------------------------------------------
# # [13] JSONPlaceholder — PUT i PATCH (aktualizacje, symulowane)
# # ------------------------------------------------------------
# print("[13] JSONPlaceholder: PUT / PATCH na /posts/1 (symulacja)")
# # PUT — pełna aktualizacja
# r = requests.put(
#     f"{BASE}/posts/1",
#     json={"id": 1, "title": "NOWY TYTUŁ", "body": "NOWA TREŚĆ", "userId": 1},
#     timeout=5,
# )
# print("Status PUT /posts/1:", r.status_code)
# print("PUT body:", r.json())

# # PATCH — częściowa aktualizacja
# r = requests.patch(f"{BASE}/posts/1", json={"title": "tytuł tylko zmieniony"}, timeout=5)
# print("Status PATCH /posts/1:", r.status_code)
# print("PATCH body:", r.json())
# print()

# # ZADANIE 13:
# # - Po PATCH sprawdź, że w odpowiedzi "title" == "tytuł tylko zmieniony".
# # - Zrób PATCH na /users/1 zmieniając tylko "username" i wypisz z odpowiedzi "username".




# # ------------------------------------------------------------
# # [14] JSONPlaceholder — DELETE (usuwanie, symulowane)
# # ------------------------------------------------------------
# print("[14] JSONPlaceholder: DELETE /posts/1 (symulacja)")
# r = requests.delete(f"{BASE}/posts/1", timeout=5)
# print("Status DELETE /posts/1:", r.status_code)
# if r.status_code in (200, 204):
#     print("✅ Usunięcie przyjęte (symulacja).")
# else:
#     print("❌ Niespodziewany status:", r.status_code)
# print()

# # ZADANIE 14:
# # - Zrób DELETE na /comments/1 i uznaj operację za OK przy statusie 200 lub 204.
# # - Wypisz „Test zaliczony” jeśli oba DELETE-y były OK, inaczej „Test NIEZALICZONY”.




# # ------------------------------------------------------------
# # [15] (Opcjonalnie) Małe funkcje pod JSONPlaceholder (+ mini asercje)
# # ------------------------------------------------------------
# print("[15] Funkcje pomocnicze dla JSONPlaceholder")

# def jp_get(path: str, **params):
#     """GET na JSONPlaceholder, zwraca (data|None, status)."""
#     url = f"{BASE}/{path.lstrip('/')}"
#     try:
#         resp = requests.get(url, params=params or None, timeout=5)
#         try:
#             return resp.json(), resp.status_code
#         except ValueError:
#             return None, resp.status_code
#     except requests.exceptions.RequestException:
#         return None, -1

# def jp_create_post(title: str, body: str, user_id: int) -> Tuple[dict, int]:
#     """POST /posts — zwraca (json, status)."""
#     resp = requests.post(
#         f"{BASE}/posts",
#         json={"title": title, "body": body, "userId": user_id},
#         timeout=5,
#     )
#     return resp.json(), resp.status_code

# def assert_true(cond: bool, msg: str = "Warunek nie jest True") -> None:
#     if not cond:
#         raise AssertionError(msg)

# # Krótka demonstracja funkcji:
# data_posts, st = jp_get("/posts")
# print("jp_get('/posts') status:", st, "| długość:", len(data_posts) if isinstance(data_posts, list) else "brak")

# created, stc = jp_create_post("abc", "def", 1)
# print("jp_create_post status:", stc, "| id?:", created.get("id") if isinstance(created, dict) else None)

# # Mini-asercje:
# if isinstance(created, dict):
#     assert_true("id" in created, "POST /posts powinien zwrócić id")
# print("✅ Mini-asercje dla JSONPlaceholder OK\n")

# # ZADANIE 15:
# # - Dodaj funkcję jp_update_post_partial(post_id, **fields) -> (json, status) używając PATCH.
# # - Dodaj funkcję jp_delete(path) -> status i użyj jej do usunięcia /posts/1 i /comments/1 (symulacja).


# # ZADANIE 7:
# # - Dodaj funkcję assert_in(item, collection) — jeśli nie ma, rzuć AssertionError.
# # - Użyj assert_in do sprawdzenia, że w root JSON GitHuba jest klucz "rate_limit_url".





# # ------------------------------------------------------------
# # [8] Skanowanie kilku endpointów JSON: zlicz OK/FAIL
# # ------------------------------------------------------------
# print("[8] Skanowanie listy endpointów (JSON)")

# urls = [
#     "https://api.github.com",              # JSON 200
#     "https://httpbin.org/json",            # JSON 200
#     "https://httpbin.org/status/404",      # 404
#     "https://to_nie_istnieje.abc",         # błąd połączenia
# ]

# ok = 0
# fail = 0

# for u in urls:
#     data3, st3, hdr3, er3 = fetch_json(u)
#     print("->", u)
#     print("   status:", st3, "| json:", isinstance(data3, dict), "| err:", type(er3).__name__ if er3 else None)
#     if er3 is None and st3 == 200 and is_json_response(hdr3):
#         ok += 1
#     else:
#         fail += 1

# print("Podsumowanie: OK =", ok, "| FAIL =", fail)
# if ok > fail:
#     print("🎉 ZALICZONE (przewaga OK)")
# else:
#     print("⚠️  NIEZALICZONE (więcej FAIL)")
# print()

# # ZADANIE 8:
# # - Dodaj drugi licznik: ile razy status był 2xx (dowolny) vs reszta.
# # - Wypisz procent powodzeń (OK/(OK+FAIL) * 100) zaokrąglony do 1 miejsca.




# # ------------------------------------------------------------
# # [9] Przykład reguły biznesowej na JSON — check_free_spin
# # (sam JSON w tej sekcji jest lokalny, nie z sieci)
# # ------------------------------------------------------------
# print("[9] Reguła: check_free_spin (lokalne JSON-y)")

# def check_free_spin(payload: Dict[str, Any]) -> bool:
#     """
#     True jeśli:
#     - features.free_spins.available == True i count > 0
#       LUB
#     - w bonus[] istnieje obiekt {type:'FREE_SPIN', active: True}
#     """
#     if get_in(payload, ["features", "free_spins", "available"], False) and \
#        get_in(payload, ["features", "free_spins", "count"], 0) > 0:
#         return True
#     for item in payload.get("bonus", []):
#         if item.get("type") == "FREE_SPIN" and item.get("active") is True:
#             return True
#     return False

# case_ok1 = {"features": {"free_spins": {"available": True, "count": 3}}}
# case_ok2 = {"bonus": [{"type": "FREE_SPIN", "active": True}]}
# case_no  = {"features": {"free_spins": {"available": True, "count": 0}}}

# print("OK1:", check_free_spin(case_ok1))
# print("OK2:", check_free_spin(case_ok2))
# print("NO :", check_free_spin(case_no))
# print()

# # ZADANIE 9:
# # - Rozszerz: jeśli payload["blocked"] == True -> zawsze False (nawet jeśli są spiny).
# # - Dodaj wariant promo: {"promo":{"type":"FS","remaining":N>0}} -> też True.




# # ------------------------------------------------------------
# # [10] Mini „asercje” + krótkie podsumowanie
# # ------------------------------------------------------------
# print("[10] Mini asercje + podsumowanie")
# def assert_true(cond: bool, msg: str = "Warunek nie jest True") -> None:
#     if not cond:
#         raise AssertionError(msg)

# # proste „testy” lokalnej logiki
# assert_true(check_free_spin(case_ok1) is True, "case_ok1 ma być True")
# assert_true(check_free_spin(case_ok2) is True, "case_ok2 ma być True")
# assert_true(check_free_spin(case_no)  is False, "case_no ma być False")

# print("✅ Mini testy local-logic: OK")
# print("\n=== KONIEC BLOKU 3 — wersja podstawowa ===")




# # ------------------------------------------------------------
# # [11] JSONPlaceholder — szybki podgląd danych (GET)
# # ------------------------------------------------------------
# print("[11] JSONPlaceholder: GET podgląd")
# BASE = "https://jsonplaceholder.typicode.com"

# # Lista postów
# r = requests.get(f"{BASE}/posts", timeout=5)
# print("Status /posts:", r.status_code, "| Ile rekordów?:", len(r.json()) if r.ok else 0)

# # Pojedynczy post
# r = requests.get(f"{BASE}/posts/1", timeout=5)
# print("Status /posts/1:", r.status_code)
# print("Post #1 klucze:", list(r.json().keys()) if r.ok else "brak")
# print()

# # Komentarze do konkretnego posta
# r = requests.get(f"{BASE}/posts/1/comments", timeout=5)
# print("Status /posts/1/comments:", r.status_code, "| Liczba komentarzy:", len(r.json()) if r.ok else 0)

# # Filtrowanie po query string
# r = requests.get(f"{BASE}/comments", params={"postId": 1}, timeout=5)
# print("Status /comments?postId=1:", r.status_code, "| Liczba:", len(r.json()) if r.ok else 0)
# print()

# # ZADANIE 11:
# # - Pobierz /users/2 i wypisz name oraz email.
# # - Pobierz /todos?completed=true i policz ile elementów przyszło.




# # ------------------------------------------------------------
# # [12] JSONPlaceholder — POST (tworzenie, symulowane)
# # ------------------------------------------------------------
# print("[12] JSONPlaceholder: POST /posts (symulacja tworzenia)")
# payload = {"title": "mój tytuł", "body": "treść wpisu", "userId": 1}
# r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
# print("Status POST /posts:", r.status_code)
# print("Odpowiedź:", r.json())  # powinno zawierać wygenerowane "id"
# print()

# # ZADANIE 12:
# # - Sprawdź, czy odpowiedź ma pole "id" (if "id" in r.json(): ...).
# # - Zrób drugi POST na /comments z polami: name, email, body, postId.




# # ------------------------------------------------------------
# # [13] JSONPlaceholder — PUT i PATCH (aktualizacje, symulowane)
# # ------------------------------------------------------------
# print("[13] JSONPlaceholder: PUT / PATCH na /posts/1 (symulacja)")
# # PUT — pełna aktualizacja
# r = requests.put(
#     f"{BASE}/posts/1",
#     json={"id": 1, "title": "NOWY TYTUŁ", "body": "NOWA TREŚĆ", "userId": 1},
#     timeout=5,
# )
# print("Status PUT /posts/1:", r.status_code)
# print("PUT body:", r.json())

# # PATCH — częściowa aktualizacja
# r = requests.patch(f"{BASE}/posts/1", json={"title": "tytuł tylko zmieniony"}, timeout=5)
# print("Status PATCH /posts/1:", r.status_code)
# print("PATCH body:", r.json())
# print()

# # ZADANIE 13:
# # - Po PATCH sprawdź, że w odpowiedzi "title" == "tytuł tylko zmieniony".
# # - Zrób PATCH na /users/1 zmieniając tylko "username" i wypisz z odpowiedzi "username".




# # ------------------------------------------------------------
# # [14] JSONPlaceholder — DELETE (usuwanie, symulowane)
# # ------------------------------------------------------------
# print("[14] JSONPlaceholder: DELETE /posts/1 (symulacja)")
# r = requests.delete(f"{BASE}/posts/1", timeout=5)
# print("Status DELETE /posts/1:", r.status_code)
# if r.status_code in (200, 204):
#     print("✅ Usunięcie przyjęte (symulacja).")
# else:
#     print("❌ Niespodziewany status:", r.status_code)
# print()

# # ZADANIE 14:
# # - Zrób DELETE na /comments/1 i uznaj operację za OK przy statusie 200 lub 204.
# # - Wypisz „Test zaliczony” jeśli oba DELETE-y były OK, inaczej „Test NIEZALICZONY”.




# # ------------------------------------------------------------
# # [15] (Opcjonalnie) Małe funkcje pod JSONPlaceholder (+ mini asercje)
# # ------------------------------------------------------------
# print("[15] Funkcje pomocnicze dla JSONPlaceholder")

# def jp_get(path: str, **params):
#     """GET na JSONPlaceholder, zwraca (data|None, status)."""
#     url = f"{BASE}/{path.lstrip('/')}"
#     try:
#         resp = requests.get(url, params=params or None, timeout=5)
#         try:
#             return resp.json(), resp.status_code
#         except ValueError:
#             return None, resp.status_code
#     except requests.exceptions.RequestException:
#         return None, -1

# def jp_create_post(title: str, body: str, user_id: int) -> Tuple[dict, int]:
#     """POST /posts — zwraca (json, status)."""
#     resp = requests.post(
#         f"{BASE}/posts",
#         json={"title": title, "body": body, "userId": user_id},
#         timeout=5,
#     )
#     return resp.json(), resp.status_code

# def assert_true(cond: bool, msg: str = "Warunek nie jest True") -> None:
#     if not cond:
#         raise AssertionError(msg)

# # Krótka demonstracja funkcji:
# data_posts, st = jp_get("/posts")
# print("jp_get('/posts') status:", st, "| długość:", len(data_posts) if isinstance(data_posts, list) else "brak")

# created, stc = jp_create_post("abc", "def", 1)
# print("jp_create_post status:", stc, "| id?:", created.get("id") if isinstance(created, dict) else None)

# # Mini-asercje:
# if isinstance(created, dict):
#     assert_true("id" in created, "POST /posts powinien zwrócić id")
# print("✅ Mini-asercje dla JSONPlaceholder OK\n")

# # ZADANIE 15:
# # - Dodaj funkcję jp_update_post_partial(post_id, **fields) -> (json, status) używając PATCH.
# # - Dodaj funkcję jp_delete(path) -> status i użyj jej do usunięcia /posts/1 i /comments/1 (symulacja).
