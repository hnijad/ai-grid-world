import atexit

from config import get_general_config
from game_server_client import GameServerClient
from grid_world import QLearning
from util import save_q_table_state, visualize_the_world

if __name__ == '__main__':
    user_id = get_general_config('user_id')
    api_key = get_general_config('api_key')
    team_id = get_general_config('team_id')
    world_id = get_general_config('world_id')
    gsc = GameServerClient(user_id, api_key, team_id, is_mocked=True)

    qlearning = QLearning(gsc, world_id, alpha=0.2, gamma=0.9, epsilon=0.2)
    qlearning.print_q_table()

    atexit.register(save_q_table_state, world_id, qlearning.q_table)

    for i in range(100000):
        qlearning.start_learning()
