import configparser
import argparse

config = configparser.ConfigParser()
config.read('app/config.ini')

parser = argparse.ArgumentParser()
parser.add_argument("-world_id", "--world_id", help="world id")
args = parser.parse_args()


def get_general_config(key):
    return config['general'][key]


if args.world_id:
    config.set("general", "world_id", args.world_id)
