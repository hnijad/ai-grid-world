import atexit
import numpy as np

import numpy

from config import get_general_config
from game_server_client import GameServerClient
from grid_world import QLearning
from util import save_q_table_state, visualize_the_world, save_reward_cell, save_visited_cells, visualize_visited_cells, save_mines

if __name__ == '__main__':
    user_id = get_general_config('user_id')
    api_key = get_general_config('api_key')
    team_id = get_general_config('team_id')
    world_id = get_general_config('world_id')
    gsc = GameServerClient(user_id, api_key, team_id, is_mocked=False)
    #visualize_the_world(world_id)
    #visualize_visited_cells(world_id)

    qlearning = QLearning(gsc, world_id, alpha=0.6, gamma=0.9, epsilon=0.3)

    qlearning.start_learning()

    atexit.register(save_q_table_state, world_id, qlearning.q_table)
    atexit.register(save_reward_cell, world_id, qlearning.reward_cell)
    atexit.register(save_visited_cells, world_id, qlearning.is_visited)
    atexit.register(save_mines, world_id, qlearning.mines)
