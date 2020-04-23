import json
import os

from pbpstats import (
    NBA_STRING, G_LEAGUE_STRING, WNBA_STRING, NBA_GAME_ID_PREFIX,
    G_LEAGUE_GAME_ID_PREFIX, WNBA_GAME_ID_PREFIX
)
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaGameFinderLoader(StatsNbaFileLoader, StatsNbaWebLoader):
    """
    Class for loading game finder data from stats.nba.com
    data.nba.com schedule end point doesn't have data for older season
    this is an easy way to get all games for a season
    """
    data_provider = 'stats_nba'
    resource = 'Games'
    parent_object = 'Season'

    def __init__(self, league, season, season_type, source, file_directory=None):
        self.league_string = league
        self.season_string = season
        self.season_type_string = season_type
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_game_data_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.season_string.replace("-", "_")}_{self.season_type_string.replace(" ", "_")}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = f'{G_LEAGUE_STRING}.{NBA_STRING}' if self.league_string == G_LEAGUE_STRING else self.league_string
        self.base_url = f'https://stats.{league_url_part}.com/stats/leaguegamefinder'
        self.parameters = {
            "PlayerOrTeam": 'T',
            "gtPTS": 1,
            "Season": self.season_string,
            "SeasonType": self.season_type_string,
            "LeagueID": self.league_id
        }
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.season_string.replace("-", "_")}_{self.season_type_string.replace(" ", "_")}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    @property
    def league_id(self):
        if self.league_string == NBA_STRING:
            return NBA_GAME_ID_PREFIX
        elif self.league_string == WNBA_STRING:
            return WNBA_GAME_ID_PREFIX
        elif self.league_string == G_LEAGUE_STRING:
            return G_LEAGUE_GAME_ID_PREFIX

    def _make_game_data_items(self):
        self.items = []
        sorted_games = sorted(self.data, key=lambda k: k['GAME_ID'])
        for team1, team2 in zip(sorted_games[0::2], sorted_games[1::2]):
            item = self._make_single_dict_for_game(team1, team2)
            self.items.append(StatsNbaGameItem(item))

    @staticmethod
    def _make_single_dict_for_game(team1, team2):
        """
        MATCHUP is vistor team @ home team for visitor
        MATCHUP is home team vs visitor team for home
        """
        item = {
            'GAME_ID': team1['GAME_ID'],
            'GAME_DATE_EST': team1['GAME_DATE'],
            'GAME_STATUS_TEXT': 'Final',
            'HOME_TEAM_ID': team1['TEAM_ID'] if '@' not in team1['MATCHUP'] else team2['TEAM_ID'],
            'VISITOR_TEAM_ID': team1['TEAM_ID'] if '@' in team1['MATCHUP'] else team2['TEAM_ID'],
        }
        return item
