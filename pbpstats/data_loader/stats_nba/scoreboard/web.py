import json
import os

from pbpstats import (
    NBA_STRING,
    G_LEAGUE_STRING,
    WNBA_STRING,
    NBA_GAME_ID_PREFIX,
    G_LEAGUE_GAME_ID_PREFIX,
    WNBA_GAME_ID_PREFIX,
)
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader


class StatsNbaScoreboardWebLoader(StatsNbaWebLoader):
    """
    A ``StatsNbaScoreboardWebLoader`` object should be instantiated and passed into ``StatsNbaScoreboardLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `stats_<league>_<date>.json` in the `/schedule` subdirectory.
        If not provided response data will not be saved on disk.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, date, league_string):
        self.date = date
        self.league_string = league_string
        league_url_part = (
            f"{G_LEAGUE_STRING}.{NBA_STRING}"
            if self.league_string == G_LEAGUE_STRING
            else self.league_string
        )
        self.base_url = f"https://stats.{league_url_part}.com/stats/scoreboardV2"
        self.parameters = {
            "DayOffset": 0,
            "LeagueID": self.league_id,
            "gameDate": self.date,
        }
        return self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.date.replace("/", "_")}.json'
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

    @property
    def league_id(self):
        """
        Returns League Id for league.

        00 for nba, 10 for wnba, 20 for g-league
        """
        if self.league_string == NBA_STRING:
            return NBA_GAME_ID_PREFIX
        elif self.league_string == WNBA_STRING:
            return WNBA_GAME_ID_PREFIX
        elif self.league_string == G_LEAGUE_STRING:
            return G_LEAGUE_GAME_ID_PREFIX
