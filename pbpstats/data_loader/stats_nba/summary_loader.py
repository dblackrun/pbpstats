"""
``StatsNbaSummaryLoader`` loads summary data for a game and
creates :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem`
objects for game

The following code will load summary data for game id "0021900001" from
a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader.stats_nba.summary_loader import StatsNbaSummaryLoader

    summary_loader = StatsNbaSummaryLoader("0021900001", "file", "/data")
    print(summary_loader.items[0].data) # prints game summary dict for game
"""
import json
import os

from pbpstats import NBA_STRING, G_LEAGUE_STRING
from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.stats_nba.file_loader import StatsNbaFileLoader
from pbpstats.data_loader.stats_nba.web_loader import StatsNbaWebLoader
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaSummaryLoader(StatsNbaFileLoader, StatsNbaWebLoader):
    """
    Loads stats.nba.com source summary data for game.
    Summary data is stored in items attribute
    as :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `stats_summary_<game_id>.json` in the `/game_details` subdirectory.
        If not provided response data will not be saved on disk.
    """

    data_provider = "stats_nba"
    resource = "Games"
    parent_object = "Game"

    def __init__(self, game_id, source, file_directory=None):
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_summary_items()

    def _load_data(self):
        source_method = getattr(self, f"_from_{self.source}")
        source_method()

    @check_file_directory
    def _from_file(self):
        self.file_path = (
            f"{self.file_directory}/game_details/stats_summary_{self.game_id}.json"
        )
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = (
            f"{G_LEAGUE_STRING}.{NBA_STRING}"
            if self.league == G_LEAGUE_STRING
            else self.league
        )
        self.base_url = f"https://stats.{league_url_part}.com/stats/boxscoresummaryv2"
        self.parameters = {"GameId": self.game_id}
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = (
                f"{self.file_directory}/game_details/stats_summary_{self.game_id}.json"
            )
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

    def _make_summary_items(self):
        self.items = [StatsNbaGameItem(item) for item in self.data]
