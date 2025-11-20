from api.api_client import ApiClient

def test_change_balance():
    client = ApiClient()

    users = client.get_users()
    assert users is not None, "Brak użytkowników"

    user = users[0]
    user_id = user["id"]

    old_balance = float(user["balance"])
    delta = 50.0

    # zmieniamy balans
    resp = client.update_user_balance(user_id, old_balance + delta)
    assert resp.status_code == 200, "Update payload nie działa"

    # ponownie pobieramy usera
    refreshed = client.get_user_by_id(user_id)
    new_balance = float(refreshed["balance"])

    assert new_balance == old_balance + delta, "Balans nie uległ poprawnej zmianie"
