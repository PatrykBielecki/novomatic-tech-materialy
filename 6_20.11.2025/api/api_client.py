import requests
from typing import Optional, Dict, Any, List

BASE_URL = "https://690cb8c2a6d92d83e84f1d7a.mockapi.io/api"

class ApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.last_response: Optional[requests.Response] = None

    def _url(self, path: str) -> str:
        """Buduje pełny URL na podstawie ścieżki."""
        if not path.startswith("/"):
            path = "/" + path
        return self.base_url + path

    def get(self, path: str):
        """Wykonuje GET i zapisuje last_response."""
        r = self.session.get(self._url(path), timeout=5)
        self.last_response = r
        return r

    def put(self, path: str, json=None):
        """Wykonuje PUT i zapisuje last_response."""
        r = self.session.put(self._url(path), json=json, timeout=5)
        self.last_response = r
        return r

    # ------------------------ Metody API -------------------------

    def get_users(self) -> Optional[List[Dict[str, Any]]]:
        r = self.get("/users")
        return r.json() if r.ok else None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        r = self.get(f"/users/{user_id}")
        return r.json() if r.ok else None

    def update_user_balance(self, user_id: str, new_balance: float):
        return self.put(f"/users/{user_id}", json={"balance": new_balance})

    def change_balance_by(self, user_id: str, delta: float):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        current_balance = float(user.get("balance", 0))
        new_balance = current_balance + delta
        return self.update_user_balance(user_id, new_balance)
