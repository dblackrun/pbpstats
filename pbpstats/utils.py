import json
from pathlib import Path

import pbpstats
import requests


def swap_team_id_for_game(current_team, teams):
    """
    changes team with ball

    args:
    current_team - team_id that currently has the ball
    teams - list of team ids for game

    returns:
    other team id
    """
    if current_team == teams[0]:
        return teams[1]
    else:
        return teams[0]


def generate_lineup_ids(current_players):
    """
    generates lineup ids for both teams - hyphen separated sorted player id strings

    args:
    current_players - dict with list of player ids
        ex - {'11': ['1', '2', '3', '4', '5'], '19': ['9', '11', '13', '14', '15']}

    returns dict with lineup id by team id
    """
    lineup_ids = {}
    for team_id in current_players.keys():
        players = [str(player_id) for player_id in current_players[team_id]]  # make sure player ids are strings so sort is consistent
        sorted_player_ids = sorted(players)
        lineup_id = '-'.join(sorted_player_ids)
        lineup_ids[team_id] = lineup_id
    return lineup_ids


def get_season_from_game_id(game_id):
    """
    4th and 5th characters in game id represent season year
    ex. for 2016-17 season 4th and 5th characters would be 16
    for WNBA, season is just year, ex. 2016

    args:
    game_id - string

    returns:
    season - string
    """
    league = get_league_from_game_id(game_id)
    if game_id[3] == "9":
        if game_id[4] == "9":
            if league != pbpstats.WNBA_STRING:
                return "1999-00"
            else:
                return "1999"
        else:
            if league != pbpstats.WNBA_STRING:
                return "19" + game_id[3] + game_id[4] + "-" + game_id[3] + str(int(game_id[4]) + 1)
            else:
                return "19" + game_id[3] + game_id[4]
    else:
        if game_id[4] == "9":
            if league != pbpstats.WNBA_STRING:
                return "20" + game_id[3] + game_id[4] + "-" + str(int(game_id[3]) + 1) + "0"
            else:
                return "20" + game_id[3] + game_id[4]
        else:
            if league != pbpstats.WNBA_STRING:
                return "20" + game_id[3] + game_id[4] + "-" + game_id[3] + str(int(game_id[4]) + 1)
            else:
                return "20" + game_id[3] + game_id[4]


def get_season_type_from_game_id(game_id):
    """
    3rd character in game id represent season type
    2 for reg season, 4 for playoffs

    args:
    game_id - string

    returns:
    season_type - string, None if not playoffs or regular season
    """
    if game_id[2] == "4":
        return pbpstats.PLAYOFFS_STRING
    elif game_id[2] == "2":
        return pbpstats.REGULAR_SEASON_STRING
    return None


def get_league_from_game_id(game_id):
    """
    First 2 in game id represent league
    00 for nba, 10 for wnba, 20 for g-league

    args:
    game_id - string

    returns:
    league - string
    """
    if game_id[0:2] == pbpstats.NBA_GAME_ID_PREFIX:
        return pbpstats.NBA_STRING
    elif game_id[0:2] == pbpstats.G_LEAGUE_GAME_ID_PREFIX:
        return pbpstats.G_LEAGUE_STRING
    elif game_id[0:2] == pbpstats.WNBA_GAME_ID_PREFIX:
        return pbpstats.WNBA_STRING
    return None


def get_json_response(base_url, params, file_path):
    """
    helper method to get json response

    args:
    base_url - string, api endpoint
    params - dict, query params
    file_path - string, checks if this file exists on disk
        if it does it will return the contents of the file
        otherwise it makes request and saves the request response to this file
    """
    if file_path is not None:
        data_file = Path(file_path)
        if data_file.is_file():
            with open(file_path) as json_data:
                return json.load(json_data)

    response = requests.get(base_url, params=params, headers=pbpstats.HEADERS, timeout=pbpstats.REQUEST_TIMEOUT)
    if response.status_code == 200:
        if file_path is not None:
            with open(file_path, 'w') as outfile:
                json.dump(response.json(), outfile)
        return response.json()
    else:
        response.raise_for_status()
