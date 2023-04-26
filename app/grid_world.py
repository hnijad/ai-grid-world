import random
import time

import numpy as np

from game_server_client import GameServerClient
from util import load_q_table_state


def is_valid_position(x, y) -> bool:
    return 0 <= x < 40 and 0 <= y < 40


def map_action_to_direction(action):
    if action == 0:
        return "N"
    if action == 1:
        return "E"
    if action == 2:
        return "S"
    return "W"


def map_direction_to_action(direction):
    if direction == "N":
        return 0
    if direction == "E":
        return 1
    if direction == "S":
        return 2
    return 3


directions = {"N": (1, 0), "E": (0, 1), "S": (-1, 0), "W": (0, -1)}


def get_valid_moves_from(x, y):
    return [k for k, v in directions.items() if is_valid_position(x + v[0], y + v[1])]


class QLearning:
    def __init__(self, game_client: GameServerClient, world_id, alpha=0.6, gamma=0.9, epsilon=0.4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = load_q_table_state(world_id)
        self.game_client = game_client
        self.world_id = world_id

    def update_q_table(self, x, y, x_p, y_p, action, reward):
        self.q_table[x][y][action] = (1 - self.alpha) * self.q_table[x][y][action] + \
                                     self.alpha * (reward + self.gamma * np.max(self.q_table[x_p][y_p]))

    def chose_an_action(self, x, y):
        valid_moves = get_valid_moves_from(x, y)
        if np.random.uniform() < self.epsilon:
            return random.choice(valid_moves)
        actions = [map_direction_to_action(val) for val in valid_moves]
        q_values = self.q_table[x][y][actions]
        action = actions[np.argmax(q_values)]
        return map_action_to_direction(action)

    def start_learning(self):
        enter_world_req = self.game_client.enter_a_world(self.world_id)
        if enter_world_req['code'] != 'OK' and 'currently in world' not in enter_world_req['message']:
            print("Could not enter the world ", enter_world_req['code'])
            return
        if enter_world_req['code'] != 'OK' and 'currently in world' in enter_world_req['message']:
            loc_req = self.game_client.where_am_i()
            x, y = map(int, loc_req['state'].split(":"))
            print(x, y)
        else:
            x, y = map(int, enter_world_req['state'].split(":"))

        while True:
            direction = self.chose_an_action(x, y)
            move_req = self.game_client.make_move(self.world_id, direction)
            if move_req['code'] != 'OK':
                print("Could not make a move ", move_req['code'])
                continue
            new_x, new_y = int(move_req["newState"]["x"]), int(move_req["newState"]["y"])
            reward = move_req["reward"]
            action = map_direction_to_action(direction)
            self.update_q_table(x, y, new_x, new_y, action, reward)
            print(x, y, new_x, new_y, reward)
            x, y = new_x, new_y
            time.sleep(1)
