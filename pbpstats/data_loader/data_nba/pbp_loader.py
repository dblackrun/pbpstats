"""
``DataNbaPbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.pbp.data_nba_pbp_item.DataNbaPbpItem` objects for each event

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import DataNbaPbpLoader

    pbp_loader = DataNbaPbpLoader("0021900001", "file", "/data")
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
import json
import os

from pbpstats import NBA_STRING, D_LEAGUE_STRING
from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.data_nba.file_loader import DataNbaFileLoader
from pbpstats.data_loader.data_nba.web_loader import DataNbaWebLoader
from pbpstats.resources.pbp.data_nba_pbp_item import DataNbaPbpItem


class DataNbaPbpLoader(DataNbaFileLoader, DataNbaWebLoader):
    """
    Loads data.nba.com source pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.pbp.data_nba_pbp_item.DataNbaPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `data_<game_id>.json` in the `/pbp` subdirectory.
        If not provided response data will not be saved on disk.
    """

    data_provider = "data_nba"
    resource = "Pbp"
    parent_object = "Game"

    def __init__(self, game_id, source, file_directory=None):
        self.game_id = game_id
        self.file_directory = file_directory
        self.source = source
        self._load_data()
        self._make_pbp_items()

    def _load_data(self):
        source_method = getattr(self, f"_from_{self.source}")
        source_method()

    @check_file_directory
    def _from_file(self):
        self.file_path = f"{self.file_directory}/pbp/data_{self.game_id}.json"
        self._load_data_from_file()

    def _from_web(self):
        league_url_part = NBA_STRING if self.league == D_LEAGUE_STRING else self.league
        self.url = f"https://data.{league_url_part}.com/data/v2015/json/mobile_teams/{self.league}/{self.season}/scores/pbp/{self.game_id}_full_pbp.json"
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/pbp/data_{self.game_id}.json"
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

    def _make_pbp_items(self):
        self.items = [
            DataNbaPbpItem(event, item["p"])
            for item in self.data
            for event in item["pla"]
        ]

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["g"]["pd"]
