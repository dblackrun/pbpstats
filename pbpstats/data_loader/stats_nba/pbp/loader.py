"""
``StatsNbaPbpLoader`` loads pbp data for a game and
creates :obj:`~pbpstats.resources.pbp.stats_nba_pbp_item.StatsNbaPbpItem` objects for each event

The following code will load pbp data for game id "0021900001" from a file
located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import StatsNbaPbpFileLoader, StatsNbaPbpLoader

    source_loader = StatsNbaPbpFileLoader("/data")
    pbp_loader = StatsNbaPbpLoader("0021900001", source_loader)
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase
from pbpstats.resources.pbp.stats_nba_pbp_item import StatsNbaPbpItem


class StatsNbaPbpLoader(StatsNbaLoaderBase):
    """
    Loads stats.nba.com source pbp data for game.
    Events are stored in items attribute
    as :obj:`~pbpstats.resources.pbp.stats_nba_pbp_item.StatsNbaPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.pbp.file.StatsNbaPbpFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.pbp.file.StatsNbaPbpWebLoader` object
    """

    data_provider = "stats_nba"
    resource = "Pbp"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self.file_directory = source_loader.file_directory
        self._make_pbp_items()

    def _make_pbp_items(self):
        self.items = [StatsNbaPbpItem(item, i) for i, item in enumerate(self.data)]
