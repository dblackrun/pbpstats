import json
import os

from pbpstats import NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.data_nba.web_loader import DataNbaWebLoader


class DataNbaBoxscoreWebLoader(DataNbaWebLoader):
    """
    A ``DataNbaBoxscoreWebLoader`` object should be instantiated and passed into ``DataNbaBoxscoreLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `data_<game_id>.json` in the `/game_details` subdirectory.
        If not provided response data will not be saved on disk.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, game_id):
        self.game_id = game_id
        league_url_part = NBA_STRING if self.league == G_LEAGUE_STRING else self.league
        self.url = f"http://data.{league_url_part}.com/data/v2015/json/mobile_teams/{self.league}/{self.season}/scores/gamedetail/{self.game_id}_gamedetail.json"
        return self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/game_details/data_{self.game_id}.json"
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)
