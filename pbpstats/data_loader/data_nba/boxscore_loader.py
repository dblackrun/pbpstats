import json
import os

from pbpstats import NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.data_nba.file_loader import DataNbaFileLoader
from pbpstats.data_loader.data_nba.web_loader import DataNbaWebLoader
from pbpstats.resources.boxscore.data_nba_boxscore_item import DataNbaBoxscoreItem


class DataNbaBoxscoreLoader(DataNbaFileLoader, DataNbaWebLoader):
    data_provider = 'data_nba'
    resource = 'Boxscore'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory):
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_boxscore_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/game_details/data_{self.game_id}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = NBA_STRING if self.league == G_LEAGUE_STRING else self.league
        self.url = f'http://data.{league_url_part}.com/data/v2015/json/mobile_teams/{self.league}/{self.season}/scores/gamedetail/{self.game_id}_gamedetail.json'
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/game_details/data_{self.game_id}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    def _make_boxscore_items(self):
        home = self.data['hls']
        away = self.data['vls']
        self.items = [DataNbaBoxscoreItem(item, team_id=away['tid'], team_abbreviation=away['ta']) for item in away['pstsg']]
        self.items += [DataNbaBoxscoreItem(item, team_id=home['tid'], team_abbreviation=home['ta']) for item in home['pstsg']]
        self.items.append(DataNbaBoxscoreItem(away['tstsg'], team_id=away['tid'], team_abbreviation=away['ta']))
        self.items.append(DataNbaBoxscoreItem(home['tstsg'], team_id=home['tid'], team_abbreviation=home['ta']))

    @property
    def data(self):
        return self.source_data['g']
