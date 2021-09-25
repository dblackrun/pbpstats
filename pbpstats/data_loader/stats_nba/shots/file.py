import json
from pathlib import Path

from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader


class StatsNbaShotsFileLoader(StatsNbaFileLoader):
    """
    A ``StatsNbaShotsFileLoader`` object should be instantiated and passed into ``StatsNbaShotsLoader`` when loading data from file

    :param str file_directory:
        Directory in which data should be loaded from.
        The specific file location will be `stats_home_shots_<game_id>.json`
        and `stats_away_shots_<game_id>.json` in the `/game_details` subdirectory.
    """
    def __init__(self, file_directory):
        self.file_directory = file_directory

    @check_file_directory
    def load_data(self, game_id):
        self.game_id = game_id
        self.home_file_path = (
            f"{self.file_directory }/game_details/stats_home_shots_{self.game_id}.json"
        )
        self.away_file_path = (
            f"{self.file_directory }/game_details/stats_away_shots_{self.game_id}.json"
        )

        home_data_file = Path(self.home_file_path)
        if not home_data_file.is_file():
            raise Exception(f"{self.home_file_path} does not exist")
        with open(self.home_file_path) as json_data:
            self.home_source_data = json.load(json_data)

        away_data_file = Path(self.away_file_path)
        if not away_data_file.is_file():
            raise Exception(f"{self.away_file_path} does not exist")
        with open(self.away_file_path) as json_data:
            self.away_source_data = json.load(json_data)

        return self.home_source_data, self.away_source_data
