"""
``DataNbaBoxscoreLoader`` loads boxscore data for a game and creates :obj:`~pbpstats.resources.boxscore.data_nba_boxscore_item.DataNbaBoxscoreItem` objects for each player and team

The following code will load boxscore data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import DataNbaBoxscoreFileLoader, DataNbaBoxscoreLoader

    source_loader = DataNbaBoxscoreFileLoader("/data")
    boxscore_loader = DataNbaBoxscoreLoader("0021900001", source_loader)
    print(boxscore_loader.items[0].data) # prints dict with a player's boxscore data for game
"""
from pbpstats.data_loader.data_nba.base import DataNbaLoaderBase
from pbpstats.resources.boxscore.data_nba_boxscore_item import DataNbaBoxscoreItem


class DataNbaBoxscoreLoader(DataNbaLoaderBase):
    """
    Loads data.nba.com source boxscore data for game.
    Team/Player data is stored in items attribute as :obj:`~pbpstats.resources.boxscore.data_nba_boxscore_item.DataNbaBoxscoreItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.data_nba.boxscore.file.DataNbaBoxscoreFileLoader` or :obj:`~pbpstats.data_loader.data_nba.boxscore.web.DataNbaBoxscoreWebLoader` object
    """

    data_provider = "data_nba"
    resource = "Boxscore"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_boxscore_items()

    def _make_boxscore_items(self):
        """
        makes :obj:`~pbpstats.resources.boxscore.DataNbaBoxscoreItem` items for each player/team
        """
        home = self.data["hls"]
        away = self.data["vls"]
        self.items = [
            DataNbaBoxscoreItem(item, team_id=away["tid"], team_abbreviation=away["ta"])
            for item in away["pstsg"]
        ]
        self.items += [
            DataNbaBoxscoreItem(item, team_id=home["tid"], team_abbreviation=home["ta"])
            for item in home["pstsg"]
        ]
        self.items.append(
            DataNbaBoxscoreItem(
                away["tstsg"], team_id=away["tid"], team_abbreviation=away["ta"]
            )
        )
        self.items.append(
            DataNbaBoxscoreItem(
                home["tstsg"], team_id=home["tid"], team_abbreviation=home["ta"]
            )
        )

    @property
    def data(self):
        """
        returns raw JSON response data
        """
        return self.source_data["g"]
