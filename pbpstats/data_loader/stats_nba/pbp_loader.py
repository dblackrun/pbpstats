import json
import os

from pbpstats import NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.resources.pbp.stats_nba_pbp_item import StatsNbaPbpItem


class StatsNbaPbpLoader(StatsNbaWebLoader, StatsNbaFileLoader):
    data_provider = 'stats_nba'
    resource = 'Pbp'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory=None):
        self.game_id = game_id
        self.source = source
        self.file_directory = file_directory
        self._load_data()
        self._make_pbp_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/pbp/stats_{self.game_id}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = f'{G_LEAGUE_STRING}.{NBA_STRING}' if self.league == G_LEAGUE_STRING else self.league
        self.base_url = f'https://stats.{league_url_part}.com/stats/playbyplayv2'
        self.parameters = {
            'GameId': self.game_id,
            'StartPeriod': 0,
            'EndPeriod': 10,
            'RangeType': 2,
            'StartRange': 0,
            'EndRange': 55800
        }
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/pbp/stats_{self.game_id}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    def _make_pbp_items(self):
        self.items = [StatsNbaPbpItem(item, i) for i, item in enumerate(self.data)]
