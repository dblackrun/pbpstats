import json
import os

from pbpstats import (
    NBA_STRING,
    G_LEAGUE_STRING
)

from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader


class StatsNbaGameFinderWebLoader(StatsNbaWebLoader):
    """
    A ``StatsNbaGameFinderWebLoader`` object should be instantiated and passed into ``StatsNbaGameFinderLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `stats_<league>_<season>_<season_type>.json` in the `/schedule` subdirectory.
        If not provided response data will not be saved on disk.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, league, season, season_type):
        self.league_string = league
        self.season_string = season
        self.season_type_string = season_type
        league_url_part = (
            f"{G_LEAGUE_STRING}.{NBA_STRING}"
            if self.league_string == G_LEAGUE_STRING
            else self.league_string
        )
        self.base_url = f"https://stats.{league_url_part}.com/stats/leaguegamefinder"
        self.parameters = {
            "PlayerOrTeam": "T",
            "gtPTS": 1,
            "Season": self.season_string,
            "SeasonType": self.season_type_string,
            "LeagueID": self.league_id,
        }
        return self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.season_string.replace("-", "_")}_{self.season_type_string.replace(" ", "_")}.json'
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)
