from api.api_client import ApiClient

if __name__ == "__main__":
    client = ApiClient()

    users = client.get_users()
    print("Users:", users)
