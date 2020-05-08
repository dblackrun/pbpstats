"""
``StatsNbaScoreboardLoader`` loads all games for a date and
creates :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem`
objects for each game

The following code will load data for 02/03/2020

.. code-block:: python

    from pbpstats.data_loader import StatsNbaScoreboardLoader

    game_finder_loader = StatsNbaScoreboardLoader("02/03/2020", "nba", "/data, "file")
    print(game_finder_loader.items[0].data) # prints dict for first game
"""
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
from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaScoreboardLoader(StatsNbaFileLoader, StatsNbaWebLoader):
    """
    Loads stats.nba.com source data for date.
    Games are stored in items attribute
    as :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` objects

    :param str date: Formatted as MM/DD/YYYY
    :param str league_string: Options are 'nba', 'wnba' or 'gleague'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `stats_<league>_<date>.json` in the `/schedule` subdirectory.
        If None response data will not be saved on disk.
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    """

    data_provider = "stats_nba"
    resource = "Games"
    parent_object = "Day"

    def __init__(self, date, league_string, file_directory, source):
        self.date = date
        self.league_string = league_string
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_scoreboard_items()

    def _load_data(self):
        source_method = getattr(self, f"_from_{self.source}")
        source_method()

    @check_file_directory
    def _from_file(self):
        self.file_path = f'{self.file_directory}/schedule/stats_{self.league_string}_{self.date.replace("/", "_")}.json'
        self._load_data_from_file()

    def _from_web(self):
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
        self._load_request_data()

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

    def _make_scoreboard_items(self):
        self.items = [StatsNbaGameItem(item) for item in self.data]
