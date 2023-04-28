import numpy as np


def get_next_action_by_prob(direction):
    if direction == "N":
        return np.random.choice(["N", "W", "E"], p=[0.8, 0.1, 0.1])
    if direction == "S":
        return np.random.choice(["S", "W", "E"], p=[0.8, 0.1, 0.1])
    if direction == "W":
        return np.random.choice(["W", "N", "S"], p=[0.8, 0.1, 0.1])
    if direction == "E":
        return np.random.choice(["E", "N", "S"], p=[0.8, 0.1, 0.1])


