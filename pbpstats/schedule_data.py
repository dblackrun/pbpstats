import requests

import pbpstats
from pbpstats import utils


class ScheduleData(object):
    """
    class for schedule data - all games for season and season type
    """
    def __init__(self, season, season_type, league):
        self.Season = season
        self.SeasonType = season_type
        self.League = league
        self.SeasonKey = f"{season} {season_type}"

    def get_all_game_ids_for_season(self):
        """
        gets all game ids for season for league

        returns list of game ids
        """
        if self.League in [pbpstats.NBA_STRING, pbpstats.G_LEAGUE_STRING]:
            games_response = self.get_items_from_stats_nba_com()
            games_list = self.get_games_array_of_dicts_from_response(games_response)
            return self.get_sorted_game_ids(games_list)
        elif self.League == pbpstats.WNBA_STRING:
            months = ['05', '06', '07', '08', '09', '10']
            game_ids = []
            for month in months:
                game_ids += self.get_final_wnba_games_for_month(month)
            return game_ids

    def get_items_from_stats_nba_com(self):
        """
        gets games response from stats.nba.com for season

        Sets:
        StatsNbaResponseGames - request response (error if response status is not 200)
        """

        if self.League == pbpstats.NBA_STRING:
            base_url = 'https://stats.nba.com/stats/leaguegamefinder'
            league_id = pbpstats.NBA_GAME_ID_PREFIX
        elif self.League == pbpstats.G_LEAGUE_STRING:
            base_url = 'https://stats.gleague.nba.com/stats/leaguegamefinder'
            league_id = pbpstats.G_LEAGUE_GAME_ID_PREFIX

        parameters = {
            "PlayerOrTeam": 'T',
            "gtPTS": 1,
            "Season": self.Season,
            "SeasonType": self.SeasonType,
            "LeagueID": league_id
        }
        response = requests.get(base_url, params=parameters, headers=pbpstats.HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_games_array_of_dicts_from_response(self, games_response):
        """
        creates array of dicts with games from pbp response json
        """
        headers = games_response['resultSets'][0]['headers']
        rows = games_response['resultSets'][0]['rowSet']
        return [dict(zip(headers, row)) for row in rows]

    def get_sorted_game_ids(self, games):
        """
        sorts and dedupes game ids
        """
        return sorted(list(set([game['GAME_ID'] for game in games])))

    def get_final_wnba_games_for_month(self, month):
        """
        args:
        month - string - ex. for may month should be 05

        returns:
        list of game ids
        """
        url = f'http://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/{self.Season}/league/10_league_schedule_{month}.json'
        game_ids = []
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            response_json = response.json()
            games = response_json['mscd']['g']
            for game in games:
                if game['stt'] == 'Final' and utils.get_season_type_from_game_id(game['gid']) == self.SeasonType:
                    game_ids.append(game['gid'])
        else:
            response.raise_for_status()
        return game_ids
