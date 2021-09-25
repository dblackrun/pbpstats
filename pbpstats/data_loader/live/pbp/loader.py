"""
``LivePbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.pbp.live_pbp_item.LivePbpItem` objects for each event

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import LivePbpFileLoader, LivePbpLoader

    source_loader = LivePbpFileLoader("/data")
    pbp_loader = LivePbpLoader("0021900001", source_loader)
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.live.base import LiveLoaderBase
from pbpstats.resources.pbp.live_pbp_item import LivePbpItem


class LivePbpLoader(LiveLoaderBase):
    """
    Loads live data source pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.pbp.live_pbp_item.LivePbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.live.pbp.file.LivePbpFileLoader` or :obj:`~pbpstats.data_loader.live.pbp.web.LivePbpWebLoader` object
    """

    data_provider = "live"
    resource = "Pbp"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_pbp_items()

    def _make_pbp_items(self):
        self.items = [LivePbpItem(event) for event in self.data]

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["game"]["actions"]
