"""
``LivePbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.pbp.live_pbp_item.LivePbpItem` objects for each event

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import LivePbpLoader

    pbp_loader = LivePbpLoader("0021900001", "file", "/data")
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
import json
import os

from pbpstats.data_loader.abs_data_loader import check_file_directory
from pbpstats.data_loader.live.file_loader import LiveFileLoader
from pbpstats.data_loader.live.web_loader import LiveWebLoader
from pbpstats.resources.pbp.live_pbp_item import LivePbpItem


class LivePbpLoader(LiveFileLoader, LiveWebLoader):
    """
    Loads live data source pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.pbp.live_pbp_item.LivePbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param str source: Where should data be loaded from. Options are 'web' or 'file'
    :param str file_directory: (optional if source is 'web')
        Directory in which data should be either stored (if source is web) or loaded from (if source is file).
        The specific file location will be `live_<game_id>.json` in the `/pbp` subdirectory.
        If not provided response data will not be saved on disk.
    """

    data_provider = "live"
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
        self.file_path = f"{self.file_directory}/pbp/live_{self.game_id}.json"
        self._load_data_from_file()

    def _from_web(self):
        self.url = f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.game_id}.json"
        self._load_request_data()

    def _save_data_to_file(self):
        if self.file_directory is not None and os.path.isdir(self.file_directory):
            file_path = f"{self.file_directory}/pbp/live_{self.game_id}.json"
            with open(file_path, "w") as outfile:
                json.dump(self.source_data, outfile)

    def _make_pbp_items(self):
        self.items = [LivePbpItem(event) for event in self.data]

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["game"]["actions"]
