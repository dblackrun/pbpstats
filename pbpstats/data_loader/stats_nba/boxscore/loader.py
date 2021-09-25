"""
``StatsNbaBoxscoreLoader`` loads boxscore data for a game and
creates :obj:`~pbpstats.resources.boxscore.stats_nba_boxscore_item.StatsNbaBoxscoreItem`
objects for each player and team

The following code will load boxscore data for game id "0021900001" from
a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import StatsNbaBoxscoreFileLoader, StatsNbaBoxscoreLoader

    source_loader = StatsNbaBoxscoreFileLoader("/data")
    boxscore_loader = StatsNbaBoxscoreLoader("0021900001", source_loader)
    print(boxscore_loader.items[0].data) # prints dict with a player's boxscore data for game
"""
from pbpstats.data_loader.stats_nba.base import StatsNbaLoaderBase
from pbpstats.resources.boxscore.stats_nba_boxscore_item import StatsNbaBoxscoreItem


class StatsNbaBoxscoreLoader(StatsNbaLoaderBase):
    """
    Loads stats.nba.com source boxscore data for game.
    Team/Player data is stored in items attribute as :obj:`~pbpstats.resources.boxscore.stats_nba_boxscore_item.StatsNbaBoxscoreItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.stats_nba.boxscore.file.StatsNbaBoxscoreFileLoader` or :obj:`~pbpstats.data_loader.stats_nba.boxscore.web.StatsNbaBoxscoreWebLoader` object
    """

    data_provider = "stats_nba"
    resource = "Boxscore"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_boxscore_items()

    def _make_boxscore_items(self):
        self.items = [StatsNbaBoxscoreItem(item) for item in self.data]
        self.items += [
            StatsNbaBoxscoreItem(item)
            for item in self.make_list_of_dicts(results_set_index=1)
        ]
