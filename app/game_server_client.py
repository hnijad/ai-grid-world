import requests
from requests.adapters import HTTPAdapter, Retry


class GameServerClient:
    def __init__(self, user_id, api_key, team_id):
        self.session = requests.Session()
        self.base_url = 'https://www.notexponential.com/aip2pgaming/api/rl'
        self.team_id = team_id
        self.session.headers = {
            'userid': str(user_id),
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-api-key': api_key,
            'User-Agent': 'Python 3.9'
        }
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def make_move(self, world_id, direction):
        url = self.base_url + "/gw.php"
        data = {
            "type": "move",
            "worldId": world_id,
            "teamId": self.team_id,
            "move": direction
        }
        response = self.session.post(url, data=data, timeout=30)
        print(response.json())
        return response.json()

    def enter_a_world(self, world_id):
        url = self.base_url + "/gw.php"
        data = {
            "type": "enter",
            "worldId": world_id,
            "teamId": self.team_id,
        }
        response = self.session.post(url, data=data, timeout=30)
        print(response.json())
        return response.json()

    def where_am_i(self):
        url = self.base_url + "/gw.php?type=location" + "&teamId=" + self.team_id
        response = self.session.get(url)
        print(response)
        return response.json()
