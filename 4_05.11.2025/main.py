import requests
from typing import Optional, Dict, Any
import time

# # ============================================================
# # BLOK 4 (2h): Programowanie obiektowe w testach API
# # ============================================================

# # ------------------------------------------------------------
# # [1] Klasy i obiekty — przykład prosty
# # ------------------------------------------------------------

class Player:
    """Reprezentuje gracza w testach API."""
    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self.balance = balance

    def __repr__(self) -> str:
        return f"<Player name={self.name}, balance={self.balance}>"

    def add_balance(self, amount: float):
        self.balance += amount
        print(f"{self.name} +{amount} => {self.balance}")

    def spend_balance(self, amount: float):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.name} -{amount} => {self.balance}")
        else:
            print(f"⚠️ {self.name} nie ma wystarczających środków!")

# Demonstracja:
# p1 = Player("Anna", 100)
# p1.add_balance(50)
# p1.spend_balance(120)
# p1.spend_balance(60)
# print(p1)
# print()

# # ZADANIE 1:
# # - Dodaj metodę transfer_to(self, other_player, amount),
# #   która przelewa środki do innego gracza.
# # - Upewnij się, że nie można przelać więcej niż się ma.
# # - Przetestuj na dwóch obiektach Player.


# # ------------------------------------------------------------
# # [2] Klasa z logiką API — proste metody
# # ------------------------------------------------------------


class GameSession:
    """Sesja gry: zarządza komunikacją z API i danymi sesji."""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.last_status: Optional[int] = None
        self.last_json: Optional[Dict[str, Any]] = None

    def check_api_status(self, endpoint: str = "/status/200"):
        """Sprawdza status API."""
        url = f"{self.base_url.rstrip('/')}{endpoint}"
        try:
            r = requests.get(url, timeout=3)
            self.last_status = r.status_code
            print(f"GET {url} → {r.status_code}")
            return r.status_code
        except requests.exceptions.RequestException as e:
            print("Błąd połączenia:", e)
            self.last_status = -1
            return -1

# Demonstracja:
# session = GameSession("https://httpbin.org")
# session.check_api_status("/status/200")
# print()

# # ZADANIE 2:
# # - Dodaj metodę fetch_json(self, path: str) -> dict|None,
# #   która pobiera JSON i zapisuje go w self.last_json.
# # - Obsłuż wyjątek RequestException oraz błędny JSON (ValueError).
# # - Przetestuj z endpointem: /json.


# # ------------------------------------------------------------
# # [3] Dziedziczenie — klasy bazowe i pochodne
# # ------------------------------------------------------------


# class BaseGame:
#     """Bazowa klasa gry."""
#     def __init__(self, name: str, base_url: str):
#         self.name = name
#         self.session = GameSession(base_url)

#     def check_connection(self) -> bool:
#         code = self.session.check_api_status("/status/200")
#         return code == 200


# class SlotGame(BaseGame):
#     """Gra typu slot (dziedziczy po BaseGame)."""
#     def __init__(self, name: str, base_url: str, player: Player):
#         super().__init__(name, base_url)
#         self.player = player
#         self.last_balance = player.balance

#     def check_balance_change(self) -> bool:
#         """Sprawdza, czy balans gracza uległ zmianie."""
#         changed = self.player.balance != self.last_balance
#         print(f"Balance changed? {changed} ({self.last_balance} → {self.player.balance})")
#         self.last_balance = self.player.balance
#         return changed


# # Demonstracja:
# player = Player("Jan", 200)
# game = SlotGame("Lucky7", "https://httpbin.org", player)
# print("Połączenie z API:", game.check_connection())
# player.add_balance(10)
# game.check_balance_change()
# print()

# # ZADANIE 3:
# # - Stwórz nową klasę BonusGame(BaseGame),
# #   z metodą grant_bonus(self, player, amount),
# #   która dodaje graczowi środki i wypisuje komunikat.
# # - Użyj metody add_balance z klasy Player.


# # ------------------------------------------------------------
# # [4] Kompozycja — klasy wewnątrz siebie
# # ------------------------------------------------------------


# class GameController:
#     """Łączy gracza i grę — symulacja testu API."""
#     def __init__(self, player: Player, game: BaseGame):
#         self.player = player
#         self.game = game

#     def play_round(self, cost: float, win: float):
#         """Symulacja rundy gry."""
#         print(f"🎰 Runda: koszt {cost}, wygrana {win}")
#         self.player.spend_balance(cost)
#         time.sleep(0.2)
#         self.player.add_balance(win)
#         print("Saldo po rundzie:", self.player.balance)
#         print("Sprawdzenie zmiany stanu:")
#         self.game.check_balance_change()

# # Demonstracja:
# ctrl = GameController(player, game)
# ctrl.play_round(20, 35)
# print()

# # ZADANIE 4:
# # - Dodaj metodę run_test_round(self, cost, win_expected),
# #   która:
# #     1. uruchamia play_round(cost, win_expected)
# #     2. sprawdza, że balans > 0
# #     3. wypisuje "TEST OK" lub "TEST FAIL"
# # - Przetestuj ją z dwoma różnymi wartościami win_expected.


# # ------------------------------------------------------------
# # [5] Mini test integracyjny — łączenie wszystkiego
# # ------------------------------------------------------------


# player = Player("Zosia", 100)
# slot = SlotGame("FruitBlast", "https://httpbin.org", player)
# controller = GameController(player, slot)

# # Demo gry:
# slot.session.check_api_status("/status/200")
# controller.play_round(10, 15)
# controller.play_round(20, 5)

# # ZADANIE 5:
# # - Dodaj metodę assert_balance(self, min_value),
# #   która rzuca AssertionError jeśli balans < min_value.
# # - Wywołaj ją po 2 rundach i sprawdź, czy test przechodzi.
# # - Jeśli AssertionError → wypisz „Test niezaliczony”.
# # - Jeśli OK → „Test zaliczony”.
