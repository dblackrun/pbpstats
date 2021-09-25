"""
``DataNbaPossessionLoader`` loads possession data for a game and creates :obj:`~pbpstats.resources.possessions.possession.Possession` objects for each possession

The following code will load possession data for game id "0021900001" from a pbp file located in the ``/pbp`` subdirectory of the ``/data`` directory

.. code-block:: python

    from pbpstats.data_loader import DataNbaPossessionFileLoader, DataNbaPossessionLoader

    source_loader = DataNbaPossessionFileLoader("/data")
    possession_loader = DataNbaPossessionLoader("0021900001", source_loader)
    print(possession_loader.items[0].data)  # prints dict with the first possession of the game
"""
from pbpstats.data_loader.data_nba.enhanced_pbp.loader import DataNbaEnhancedPbpLoader
from pbpstats.data_loader.nba_possession_loader import NbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


class DataNbaPossessionLoader(NbaPossessionLoader):
    """
    Loads data.nba.com source possession data for game.
    Possessions are stored in items attribute as :obj:`~pbpstats.resources.possessions.possession.Possession` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.data_nba.possessions.file.DataNbaPossessionFileLoader` or :obj:`~pbpstats.data_loader.data_nba.possessions.web.DataNbaPossessionWebLoader` object
    """

    data_provider = "data_nba"
    resource = "Possessions"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.file_directory = source_loader.file_directory
        pbp_events = DataNbaEnhancedPbpLoader(game_id, source_loader.enhanced_pbp_source_loader)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [
            Possession(possession_events) for possession_events in events_by_possession
        ]
        self._add_extra_attrs_to_all_possessions()
