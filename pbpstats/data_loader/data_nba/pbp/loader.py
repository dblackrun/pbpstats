"""
``DataNbaPbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.pbp.data_nba_pbp_item.DataNbaPbpItem` objects for each event

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import DataNbaPbpFileLoader, DataNbaPbpLoader

    source_loader = DataNbaPbpFileLoader("/data")
    pbp_loader = DataNbaPbpLoader("0021900001", source_loader)
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.data_nba.base import DataNbaLoaderBase
from pbpstats.resources.pbp.data_nba_pbp_item import DataNbaPbpItem


class DataNbaPbpLoader(DataNbaLoaderBase):
    """
    Loads data.nba.com source pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.pbp.data_nba_pbp_item.DataNbaPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.data_nba.pbp.file.DataNbaPbpFileLoader` or :obj:`~pbpstats.data_loader.data_nba.pbp.web.DataNbaPbpWebLoader` object
    """

    data_provider = "data_nba"
    resource = "Pbp"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.source_data = source_loader.load_data(self.game_id)
        self._make_pbp_items()

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
