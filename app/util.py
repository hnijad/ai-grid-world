import numpy as np

COL = 40
ROW = 40

directions = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}  # (x, y) pair


def save_q_table_state(world_id, state):
    np.save(f"states/world-{world_id}.npy", state)


def load_q_table_state(world_id):
    try:
        return np.load(f"states/world-{world_id}.npy")
    except FileNotFoundError as e:
        return np.zeros((ROW, COL, 4))


def is_valid_position(x, y) -> bool:
    return 0 <= x < COL and 0 <= y < ROW


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


def get_valid_moves_from(x, y):
    return [k for k, v in directions.items() if is_valid_position(x + v[0], y + v[1])]
