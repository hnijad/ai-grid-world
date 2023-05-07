import random
import time

import numpy as np

from game_server_client import GameServerClient
from util import load_q_table_state, map_direction_to_action, map_action_to_direction, COL, ROW, \
    directions, is_valid_position, get_valid_moves_from, load_reward_cell, load_visited_cells, load_mines, \
    save_mines, save_visited_cells


class QLearning:
    def __init__(self, game_client: GameServerClient, world_id, alpha=0.6, gamma=0.9, epsilon=0.4):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = load_q_table_state(world_id)
        self.game_client = game_client
        self.world_id = world_id
        self.history = []
        self.reward_cell = load_reward_cell(world_id)
        self.mines = load_mines(world_id)
        self.is_visited = load_visited_cells(world_id)
        self.x_lim = self.reward_cell[0]
        self.y_lim = self.reward_cell[1]

    def update_q_table(self, x, y, x_p, y_p, action, reward):
        self.q_table[y][x][action] = (1 - self.alpha) * self.q_table[y][x][action] + \
                                     self.alpha * (reward + self.gamma * np.max(self.q_table[y_p][x_p]))

    def update_q_table_with_back_propagation(self):
        print("Updating q table")
        for s in reversed(self.history):
            self.update_q_table(s[0], s[1], s[2], s[3], s[4], s[5])

    def print_q_table(self):
        for x in range(ROW):
            for y in range(COL):
                print(str(x) + "," + str(y), " : ", map_action_to_direction(np.argmax(self.q_table[y, x])),
                      np.max(self.q_table[y, x]))

    def chose_an_action(self, x, y):
        valid_moves = get_valid_moves_from(x, y, min(self.x_lim + 1, COL), min(self.y_lim + 1, ROW))
        if np.random.uniform() < self.epsilon:
            random.shuffle(valid_moves)
            for move in valid_moves:
                if not self.is_visited[x + directions[move][0]][y + directions[move][1]]:
                    print("unvisited cell selected", x + directions[move][0], y + directions[move][1])
                    print("val = ", self.is_visited[x + directions[move][0]][y + directions[move][1]])
                    return move
            for move in valid_moves:
                if not self.mines[x + directions[move][0]][y + directions[move][1]]:
                    return move
                else:
                    print("Mine in cell", x + directions[move][0], y + directions[move][1])
            return valid_moves[0]
        actions = [map_direction_to_action(val) for val in valid_moves]
        q_values = self.q_table[y][x][actions]
        action = actions[np.argmax(q_values)]
        return map_action_to_direction(action)

    def start_learning(self):
        enter_world_req = self.game_client.enter_a_world(self.world_id)
        if enter_world_req['code'] != 'OK' and 'currently in world' not in enter_world_req['message']:
            print("Could not enter the world ", enter_world_req['code'])
            return
        if enter_world_req['code'] != 'OK' and 'currently in world' in enter_world_req['message']:
            loc_req = self.game_client.where_am_i(self.world_id)
            x, y = map(int, loc_req['state'].split(":"))
        else:
            x, y = map(int, enter_world_req['state'].split(":"))
        cnt = 0
        while True:
            try:
                cnt = cnt + 1
                direction = self.chose_an_action(x, y)
                move_req = self.game_client.make_move(self.world_id, direction)
                if move_req['code'] != 'OK':
                    print("Could not make a move ", move_req['code'])
                    continue
                reward = move_req["reward"]
                if abs(reward) < 2:
                    reward = 0
                action = map_direction_to_action(direction)
                if move_req["newState"]:
                    new_x, new_y = int(move_req["newState"]["x"]), int(move_req["newState"]["y"])
                    self.history.append((x, y, new_x, new_y, action, reward))
                    self.is_visited[new_x][new_y] = True
                    # self.update_q_table(x, y, new_x, new_y, action, reward)
                    x, y = new_x, new_y
                    print(new_x, new_y)
                    save_mines(self.world_id, self.mines)
                    save_visited_cells(self.world_id, self.is_visited)
                    time.sleep(0.5)
                else:
                    if reward > 0:
                        self.is_visited[x][y] = True
                        self.reward_cell = np.array([x, y])
                    if reward < 0:
                        self.is_visited[x][y] = True
                        self.mines[x, y] = True
                    self.q_table[y, x, action] = reward
                    self.update_q_table_with_back_propagation()
                    self.history.clear()
                    break
            except Exception as e:
                print("Exception while requesting client ", e)
                time.sleep(1)

        print("cnt=", cnt)
