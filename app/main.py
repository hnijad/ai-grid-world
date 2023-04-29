import atexit

import numpy as np

from config import get_general_config
from game_server_client import GameServerClient
from grid_world import QLearning
from util import save_q_table_state, ROW, COL, map_action_to_direction

if __name__ == '__main__':
    user_id = get_general_config('user_id')
    api_key = get_general_config('api_key')
    team_id = get_general_config('team_id')
    world_id = get_general_config('world_id')
    gsc = GameServerClient(user_id, api_key, team_id, is_mocked=True)
    np.random.seed(4)

    qlearning = QLearning(gsc, world_id, alpha=0.2, gamma=0.9, epsilon=0.3)
    atexit.register(save_q_table_state, world_id, qlearning.q_table)
    for i in range(100000):
        qlearning.start_learning()
    for i in range(ROW):
        for j in range(COL):
            print(str(i) + "," + str(j), " : ",  map_action_to_direction(np.argmax(qlearning.q_table[i, j])), np.max(qlearning.q_table[i, j]))
