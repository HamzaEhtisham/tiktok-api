import requests
import time

class TikTokAPI:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def fetch_tiktok_data(self, sec_uid, retries=3, delay=5):
        url = "https://tiktok.evelode.com/tiktok-api"
        querystring = {"secUid": sec_uid, "count": "30", "minCursor": "0", "maxCursor": "0"}
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host
        }
        for _ in range(retries):
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying in {} seconds...".format(delay))
                time.sleep(delay)
            elif response.status_code == 404:
                print("Error: Data not found (404). Please check the sec_uid.")
                return None
            else:
                print(f"Error: Unable to fetch data, status code: {response.status_code}")
                return None
        print("Failed to fetch data after multiple retries.")
        return None

    def sort_data(self, data, sort_by):
        followings = data.get('userList')
        if not followings:
            print("No followings data found.")
            return []

        sort_by = sort_by.lower()
        if sort_by == "username":
            sort_key = lambda x: x['user'].get('uniqueId', '').lower()
        elif sort_by == "nickname":
            sort_key = lambda x: x['user'].get('nickname', '').lower()
        elif sort_by == "followers":
            sort_key = lambda x: x['stats'].get('followerCount', 0)
        elif sort_by == "following":
            sort_key = lambda x: x['stats'].get('followingCount', 0)
        else:
            print("Invalid sort field. Sorting by username.")
            sort_key = lambda x: x['user'].get('uniqueId', '').lower()

        sorted_followings = sorted(followings, key=sort_key, reverse=(sort_by in ["followers", "following"]))
        return sorted_followings

    def display_data(self, followings):
        for item in followings:
            user = item.get('user', {})
            stats = item.get('stats', {})
            print(f"Username: {user.get('uniqueId', 'N/A')}")
            print(f"Nickname: {user.get('nickname', 'N/A')}")
            print(f"Followers: {stats.get('followerCount', 'N/A')}")
            print(f"Following: {stats.get('followingCount', 'N/A')}")
            print(f"Bio: {user.get('signature', 'N/A')}")
            print("-" * 40)

if __name__ == "__main__":
    api_key = "fafe24d5e3684657009032fd363072aa"
    host = "tiktok.evelode.com"
    sec_uid = "MS4wLjABAAAAY3pcRUgWNZAUWlErRzIyrWoc1cMUIdws4KMQQAS5aKN9AD1lcmx5IvCXMUJrP2dB"

    tiktok_api = TikTokAPI(api_key, host)
    data = tiktok_api.fetch_tiktok_data(sec_uid)
    if data:
        while True:
            print("Sort by:")
            print("1. Username")
            print("2. Nickname")
            print("3. Followers")
            print("4. Following")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")

            if choice == "5":
                break

            sort_by = {
                "1": "username",
                "2": "nickname",
                "3": "followers",
                "4": "following"
            }.get(choice, "username")

            sorted_data = tiktok_api.sort_data(data, sort_by)
            tiktok_api.display_data(sorted_data)
