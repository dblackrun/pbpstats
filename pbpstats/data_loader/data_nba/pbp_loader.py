import json
import os

from pbpstats import NBA_STRING, D_LEAGUE_STRING
from pbpstats.data_loader.data_nba.file_loader import DataNbaFileLoader
from pbpstats.data_loader.data_nba.web_loader import DataNbaWebLoader
from pbpstats.resources.pbp.data_nba_pbp_item import DataNbaPbpItem


class DataNbaPbpLoader(DataNbaFileLoader, DataNbaWebLoader):
    data_provider = 'data_nba'
    resource = 'Pbp'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_pbp_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/pbp/data_{self.game_id}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = NBA_STRING if self.league == D_LEAGUE_STRING else self.league
        self.url = f'https://data.{league_url_part}.com/data/v2015/json/mobile_teams/{self.league}/{self.season}/scores/pbp/{self.game_id}_full_pbp.json'
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/pbp/data_{self.game_id}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    def _make_pbp_items(self):
        self.items = [DataNbaPbpItem(event, item['p']) for item in self.data for event in item['pla']]

    @property
    def data(self):
        return self.source_data['g']['pd']
