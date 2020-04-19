import json
import os

from pbpstats import (
    NBA_STRING, G_LEAGUE_STRING, D_LEAGUE_STRING, WNBA_STRING, PLAYOFFS_STRING,
    REGULAR_SEASON_STRING, NBA_GAME_ID_PREFIX, G_LEAGUE_GAME_ID_PREFIX, WNBA_GAME_ID_PREFIX
)
from pbpstats.data_loader.data_nba.file_loader import DataNbaFileLoader
from pbpstats.data_loader.data_nba.web_loader import DataNbaWebLoader
from pbpstats.resources.games.data_nba_game_item import DataNbaGameItem


class DataNbaScheduleLoader(DataNbaFileLoader, DataNbaWebLoader):
    data_provider = 'data_nba'
    resource = 'Games'
    parent_object = 'Season'

    def __init__(self, league, season, season_type, source, file_directory=None):
        self.league_string = league
        self.season_year = season.split('-')[0]
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_game_items(season_type)

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/schedule/data_{self.league_string}_{self.season_year}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = NBA_STRING if self.league_string == G_LEAGUE_STRING else self.league_string
        league_part = D_LEAGUE_STRING if self.league_string == G_LEAGUE_STRING else self.league_string
        self.url = f'https://data.{league_url_part}.com/data/10s/v2015/json/mobile_teams/{league_part}/{self.season_year}/league/{self.league_id}_full_schedule.json'
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/schedule/data_{self.league_string}_{self.season_year}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    def _make_game_items(self, season_type):
        self.season_type = season_type
        self.items = [DataNbaGameItem(game) for item in self.data for game in item['mscd']['g'] if self._is_season_type(game)]

    def _is_season_type(self, game):
        if game['gid'][2] == '4' and self.season_type == PLAYOFFS_STRING:
            return True
        elif game['gid'][2] == '2' and self.season_type == REGULAR_SEASON_STRING:
            return True
        return False

    @property
    def data(self):
        return self.source_data['lscd']

    @property
    def league_id(self):
        if self.league_string == NBA_STRING:
            return NBA_GAME_ID_PREFIX
        elif self.league_string == WNBA_STRING:
            return WNBA_GAME_ID_PREFIX
        elif self.league_string == G_LEAGUE_STRING:
            return G_LEAGUE_GAME_ID_PREFIX
