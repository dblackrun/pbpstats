"""
``LivePossessionLoader`` loads possession data for a game and creates :obj:`~pbpstats.resources.possessions.possession.Possession` objects for each possession

The following code will load possession data for game id "0021900001" from a pbp file located in the ``/pbp`` subdirectory of the ``/data`` directory

.. code-block:: python

    from pbpstats.data_loader import LivePossessionFileLoader, LivePossessionLoader

    source_loader = LivePossessionFileLoader("/data")
    pbp_loader = LivePossessionLoader("0021900001", source_loader)
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.live.enhanced_pbp.loader import LiveEnhancedPbpLoader
from pbpstats.data_loader.nba_possession_loader import NbaPossessionLoader
from pbpstats.resources.possessions.possession import Possession


class LivePossessionLoader(NbaPossessionLoader):
    """
    Loads live data source possession data for game.
    Possessions are stored in items attribute as :obj:`~pbpstats.resources.possessions.possession.Possession` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.live.possessions.file.LivePossessionFileLoader` or :obj:`~pbpstats.data_loader.live.possessions.web.LivePossessionWebLoader` object
    """
    data_provider = "live"
    resource = "Possessions"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.game_id = game_id
        self.file_directory = source_loader.file_directory
        pbp_events = LiveEnhancedPbpLoader(game_id, source_loader.enhanced_pbp_source_loader)
        self.events = pbp_events.items
        events_by_possession = self._split_events_by_possession()
        self.items = [
            Possession(possession_events) for possession_events in events_by_possession
        ]
        self._add_extra_attrs_to_all_possessions()
