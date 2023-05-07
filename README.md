<h1 align="center">Project 3 - Reinforcement Learning</h1>
<h4 align="center">Team members: Nijad Huseynov, Yusif Mukhtarov, Toghrul Tahirov</h4>


## Table of Contents

- [Build](#install)
- [Usage](#usage)
- [Implementation](#implementation)
- [Dependencies](#dependencies)

## Build
To build and run application execute the following commands.

```shell
python app/main.py
```

To run the unit test cases, run the following command.

```shell
python -m unittest tests/
```


## Usage
To run this program as an agent, we need to configure following parameters in ```app/config.ini```.
<li> The `api_key` parameter is API key for accessing game server, and it is required param </li>
<li> The `timeout` parameter is second in which game server declares our agent out of game. Currently, it is ignored </li>
<li> The `user_id` parameter is user id in game server, and it should be consistent with api_key. It is required param </li>
<li>The `team_id` parameter is the team id. It is required param, and it can also be passed as command line argument. </li>

## Implementation
```app/client/game_server_client.py``` class is responsible for making the api calls to server. <br>
```app/config.py``` is responsible for parsing the config values from  ```app/config.ini``` and command line. <br>

## Dependencies
The project uses the python's requests library to make the api calls to the server. In the testing process we have used
python3.