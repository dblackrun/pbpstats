import json
import os

from pbpstats import (
    G_LEAGUE_GAME_ID_PREFIX,
    G_LEAGUE_STRING,
    NBA_GAME_ID_PREFIX,
    NBA_STRING,
    WNBA_GAME_ID_PREFIX,
    WNBA_STRING,
)
from pbpstats.data_loader.live.web_loader import LiveWebLoader


class LiveScheduleWebLoader(LiveWebLoader):
    """
    Only for the current NBA season
     A ``LiveScheduleWebLoader`` object should be instantiated and passed into ``LiveSchedulLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `live_<league>_<season_year>.json` in the `/schedule` subdirectory.
        If not provided response data will not be saved on disk.
    """

    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, league, season):
        self.league_string = league
        self.season_year = season.split("-")[0]
        self.url = f"https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_2.json"
        return self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/schedule/live_{self.league_string}_{self.season_year}.json"
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
