"""
``StatsNbaSummaryLoader`` loads summary data for a game and
creates :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem`
objects for game

The following code will load summary data for game id "0021900001" from
a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader.stats_nba.summary.file import StatsNbaSummaryFileLoader
    from pbpstats.data_loader.stats_nba.summary.loader import StatsNbaSummaryLoader

    source_loader = StatsNbaSummaryFileLoader("/data")
    summary_loader = StatsNbaSummaryLoader("0021900001", source_loader)
    print(summary_loader.items[0].data) # prints game summary dict for game
"""
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase
from pbpstats.resources.games.stats_nba_game_item import StatsNbaGameItem


class StatsNbaSummaryLoader(StatsNbaLoaderBase):
    """
    Loads stats.nba.com source summary data for game.
    Summary data is stored in items attribute
    as :obj:`~pbpstats.resources.games.stats_nba_game_item.StatsNbaGameItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.summary.file.StatsNbaSummaryFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.summary.web.StatsNbaSummaryWebLoader` object
    """

    data_provider = "stats_nba"
    resource = "Games"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_summary_items()

    def _make_summary_items(self):
        self.items = [StatsNbaGameItem(item) for item in self.data]
