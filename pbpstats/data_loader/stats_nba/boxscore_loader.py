import json
import os

from pbpstats import NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.resources.boxscore.stats_nba_boxscore_item import StatsNbaBoxscoreItem


class StatsNbaBoxscoreLoader(StatsNbaFileLoader, StatsNbaWebLoader):
    """
    class for loading boxscore items from stats.nba.com
    supports loading from api request or from file saved
    on disk with api response data
    """
    data_provider = 'stats_nba'
    resource = 'Boxscore'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory):
        """
        game_id - string, stats.nba.com game id
        source - string, file or web
        file_directory - string, directory containing data saved on disk
            - required if loading from file
            - if not None when loading from web, response will be saved there
        """
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_boxscore_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.file_path = f'{self.file_directory}/game_details/stats_boxscore_{self.game_id}.json'
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = f'{G_LEAGUE_STRING}.{NBA_STRING}' if self.league == G_LEAGUE_STRING else self.league
        self.base_url = f'https://stats.{league_url_part}.com/stats/boxscoretraditionalv2'
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
            file_path = f'{self.file_directory}/game_details/stats_boxscore_{self.game_id}.json'
            with open(file_path, 'w') as outfile:
                json.dump(self.source_data, outfile)

    def _make_boxscore_items(self):
        self.items = [StatsNbaBoxscoreItem(item) for item in self.data]
        self.items += [StatsNbaBoxscoreItem(item) for item in self.make_list_of_dicts(results_set_index=1)]
