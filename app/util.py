import numpy as np
import matplotlib.pyplot as plt

COL = 10
ROW = 10

directions = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}  # (x, y) pair


def save_q_table_state(world_id, state):
    np.save(f"states/world-{world_id}.npy", state)


def load_q_table_state(world_id):
    try:
        return np.load(f"states/world-{world_id}.npy")
    except FileNotFoundError as e:
        return np.zeros((ROW, COL, 4))


def is_valid_position(x, y) -> bool:
    return 0 <= x < ROW and 0 <= y < COL


def map_action_to_direction(action):
    if action == 0:
        return "N"
    if action == 1:
        return "E"
    if action == 2:
        return "S"
    return "W"


def map_action_to_arrows(action):
    if action == 0:
        return "↑"
    if action == 1:
        return "→"
    if action == 2:
        return "↓"
    return "←"


def map_action_to_arrows_local(action):
    if action == 0:
        return "→"
    if action == 1:
        return "↑"
    if action == 2:
        return "←"
    return "↓"


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


def visualize_the_world():
    q_tab = load_q_table_state(34)

    grid = np.argmax(q_tab, axis=2)
    row = grid.shape[1]
    col = grid.shape[0]
    zeros = np.zeros((col, row))

    plt.figure(figsize=(6, 6), dpi=100)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            plt.text(j, i, map_action_to_arrows_local(grid[i, j]),
                     ha='center', va='center', color='red')

    plt.imshow(zeros, cmap='Greys', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.show()


visualize_the_world()
