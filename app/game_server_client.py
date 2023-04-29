import json

import numpy as np
import requests
from requests.adapters import HTTPAdapter, Retry

from local_training_env import get_next_action_by_prob
from util import COL, ROW, directions, is_valid_position


class GameServerClient:
    def __init__(self, user_id, api_key, team_id, is_mocked=False):
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

        # data for mocking
        self.is_mocked = is_mocked
        self.mock_state = np.zeros((ROW, COL))
        self.mock_state[9, 9] = +1
        self.mock_state[5, 5] = -1
        self.mock_state[6, 6] = -1
        self.current_location = (0, 0)

    def make_move(self, world_id, direction):
        if self.is_mocked:
            next_action = get_next_action_by_prob(direction)
            #print(next_action)
            new_x = self.current_location[0] + directions[next_action][0]
            new_y = self.current_location[1] + directions[next_action][1]
            if not is_valid_position(new_x, new_y):
                new_x = self.current_location[0]
                new_y = self.current_location[1]
            resp = {
                "code": "OK",
                "worldId": world_id,
                "reward": self.mock_state[new_x, new_y],
                "newState": {
                    "x": new_x,
                    "y": new_y,
                }
            }
            self.current_location = (new_x, new_y)
            if self.mock_state[new_x, new_y] != 0:
                self.current_location = (0, 0)
            return resp

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
        if self.is_mocked:
            resp = {
                "code": "OK",
                "worldId": 0,
                "runId": 0,
                "state": "0:0"
            }
            return resp

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
        if self.is_mocked:
            resp = {
                "code": "OK",
                "world": "0",
                "state": str(self.current_location[0]) + ":" + str(self.current_location[1])
            }
            return resp

        url = self.base_url + "/gw.php?type=location" + "&teamId=" + self.team_id
        response = self.session.get(url)
        print(response)
        return response.json()
