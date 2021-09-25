import json
import os
import requests
from pathlib import Path

from pbpstats import HEADERS, REQUEST_TIMEOUT, NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.data_loader.stats_nba.summary.loader import StatsNbaSummaryLoader
from pbpstats.data_loader.stats_nba.summary.web import StatsNbaSummaryWebLoader


class StatsNbaShotsWebLoader(StatsNbaWebLoader):
    """
    A ``StatsNbaShotsWebLoader`` object should be instantiated and passed into ``StatsNbaShotsLoader`` when loading data directly from the NBA Stats API

    :param str file_directory: (optional, use it if you want to store the response data on disk)
        Directory in which data should be either stored.
        The specific file location will be `stats_home_shots_<game_id>.json`
        and `stats_away_shots_<game_id>.json` in the `/game_details` subdirectory.
        If not provided response data will not be saved on disk.
    """
    def __init__(self, file_directory=None):
        self.file_directory = file_directory

    def load_data(self, game_id):
        self.game_id = game_id
        summary_source_loader = StatsNbaSummaryWebLoader(self.file_directory)
        summary = StatsNbaSummaryLoader(self.game_id, summary_source_loader)
        home_team_id = summary.items[0].home_team_id
        away_team_id = summary.items[0].visitor_team_id
        league_url_part = (
            f"{G_LEAGUE_STRING}.{NBA_STRING}"
            if self.league == G_LEAGUE_STRING
            else self.league
        )
        self.base_url = f"https://stats.{league_url_part}.com/stats/shotchartdetail"
        base_paramaters = {
            "GameID": self.game_id,
            "Season": self.season,
            "SeasonType": self.season_type,
            "PlayerID": 0,
            "Outcome": "",
            "Location": "",
            "Month": 0,
            "SeasonSegment": "",
            "DateFrom": "",
            "DateTo": "",
            "OpponentTeamID": 0,
            "VsConference": "",
            "VsDivision": "",
            "Position": "",
            "RookieYear": "",
            "GameSegment": "",
            "Period": 0,
            "LastNGames": 0,
            "ContextMeasure": "FG_PCT",
            "PlayerPosition": "",
            "LeagueID": self.game_id[0:2],
        }
        self.home_parameters = base_paramaters.copy()
        self.home_parameters["TeamID"] = home_team_id
        self.away_parameters = base_paramaters.copy()
        self.away_parameters["TeamID"] = away_team_id

        response = requests.get(
            self.base_url,
            self.home_parameters,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            self.home_source_data = response.json()
        else:
            response.raise_for_status()

        response = requests.get(
            self.base_url,
            self.away_parameters,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            self.away_source_data = response.json()
        else:
            response.raise_for_status()
        self._save_data_to_file()
        return self.home_source_data, self.away_source_data

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            home_file_path = f"{self.file_directory}/game_details/stats_home_shots_{self.game_id}.json"
            with open(home_file_path, "w") as outfile:
                json.dump(self.home_source_data, outfile)

            away_file_path = f"{self.file_directory}/game_details/stats_away_shots_{self.game_id}.json"
            with open(away_file_path, "w") as outfile:
                json.dump(self.away_source_data, outfile)
