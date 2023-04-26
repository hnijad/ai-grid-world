import numpy as np


def save_q_table_state(world_id, state):
    np.save(f"states/world-{world_id}.npy", state)


def load_q_table_state(world_id):
    try:
        return np.load(f"states/world-{world_id}.npy")
    except FileNotFoundError as e:
        return np.zeros((40, 40, 4))
