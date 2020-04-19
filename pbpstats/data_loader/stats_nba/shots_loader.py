import json
import os
import requests
from pathlib import Path

from pbpstats import HEADERS, REQUEST_TIMEOUT, NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.summary_loader import StatsNbaSummaryLoader
from pbpstats.resources.shots.stats_nba_shot import StatsNbaShot


class StatsNbaShotsLoader(StatsNbaWebLoader, StatsNbaFileLoader):
    data_provider = 'stats_nba'
    resource = 'Shots'
    parent_object = 'Game'

    def __init__(self, game_id, source, file_directory):
        self.game_id = game_id
        self.source = source
        self.file_directory = file_directory
        self._load_data()
        self._make_shot_items()

    def _load_data(self):
        source_method = getattr(self, f'_from_{self.source}')
        source_method()

    def _from_file(self):
        self.home_file_path = f'{self.file_directory }/game_details/stats_home_shots_{self.game_id}.json'
        self.away_file_path = f'{self.file_directory }/game_details/stats_away_shots_{self.game_id}.json'

        home_data_file = Path(self.home_file_path)
        if not home_data_file.is_file():
            raise Exception(f'{self.home_file_path} does not exist')
        with open(self.home_file_path) as json_data:
            self.home_source_data = json.load(json_data)

        away_data_file = Path(self.away_file_path)
        if not away_data_file.is_file():
            raise Exception(f'{self.away_file_path} does not exist')
        with open(self.away_file_path) as json_data:
            self.away_source_data = json.load(json_data)

    def _from_web(self):
        summary = StatsNbaSummaryLoader(self.game_id, self.source, self.file_directory)
        home_team_id = summary.items[0].home_team_id
        away_team_id = summary.items[0].visitor_team_id
        league_url_part = f'{G_LEAGUE_STRING}.{NBA_STRING}' if self.league == G_LEAGUE_STRING else self.league
        self.base_url = f'https://stats.{league_url_part}.com/stats/shotchartdetail'
        base_paramaters = {
            'GameID': self.game_id,
            'Season': self.season,
            'SeasonType': self.season_type,
            'PlayerID': 0,
            'Outcome': '',
            'Location': '',
            'Month': 0,
            'SeasonSegment': '',
            'DateFrom': '',
            'DateTo': '',
            'OpponentTeamID': 0,
            'VsConference': '',
            'VsDivision': '',
            'Position': '',
            'RookieYear': '',
            'GameSegment': '',
            'Period': 0,
            'LastNGames': 0,
            'ContextMeasure': 'FG_PCT',
            'PlayerPosition': '',
            'LeagueID': self.game_id[0:2],
        }
        self.home_parameters = base_paramaters.copy()
        self.home_parameters['TeamID'] = home_team_id
        self.away_parameters = base_paramaters.copy()
        self.away_parameters['TeamID'] = away_team_id

        response = requests.get(self.base_url, self.home_parameters, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            self.home_source_data = response.json()
        else:
            response.raise_for_status()

        response = requests.get(self.base_url, self.away_parameters, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            self.away_source_data = response.json()
        else:
            response.raise_for_status()
        self._save_data_to_file()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            home_file_path = f'{self.file_directory}/game_details/stats_home_shots_{self.game_id}.json'
            with open(home_file_path, 'w') as outfile:
                json.dump(self.home_source_data, outfile)

            away_file_path = f'{self.file_directory}/game_details/stats_away_shots_{self.game_id}.json'
            with open(away_file_path, 'w') as outfile:
                json.dump(self.away_source_data, outfile)

    def _make_shot_items(self):
        self.items = [StatsNbaShot(item) for item in self.data]

    def make_list_of_dicts(self, results_set_index=0):
        """
        creates list of dicts from data
        """
        headers = self.home_source_data['resultSets'][results_set_index]['headers']
        home_rows = self.home_source_data['resultSets'][results_set_index]['rowSet']
        home_deduped_rows = self.dedupe_events_row_set(home_rows)
        away_rows = self.away_source_data['resultSets'][results_set_index]['rowSet']
        away_deduped_rows = self.dedupe_events_row_set(away_rows)
        return [dict(zip(headers, row)) for row in home_deduped_rows] + [dict(zip(headers, row)) for row in away_deduped_rows]
