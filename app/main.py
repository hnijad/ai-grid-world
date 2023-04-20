from client.game_server_client import GameServerClient
from config import get_general_config

if __name__ == '__main__':
    user_id = get_general_config('user_id')
    api_key = get_general_config('api_key')
    team_id = get_general_config('team_id')
    print(user_id, api_key, team_id)
    gsc = GameServerClient(user_id, api_key)

    print(gsc.make_move(team_id, 0, 'N'))
