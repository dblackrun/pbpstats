"""
``LiveEnhancedPbpLoader`` loads pbp data for a game and creates :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects for each event

Enhanced data for each event includes current players on floor, score, fouls to give and number of fouls committed by each player,
plus additional data depending on event type

The following code will load pbp data for game id "0021900001" from a file located in a subdirectory of the /data directory

.. code-block:: python

    from pbpstats.data_loader import LiveEnhancedPbpFileLoader, LiveEnhancedPbpLoader

    source_loader = LiveEnhancedPbpFileLoader("/data")
    pbp_loader = LiveEnhancedPbpLoader("0021900001", source_loader)
    print(pbp_loader.items[0].data)  # prints dict with the first event of the game
"""
from pbpstats.data_loader.live.pbp.loader import LivePbpLoader
from pbpstats.data_loader.nba_enhanced_pbp_loader import NbaEnhancedPbpLoader
from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_factory import (
    LiveEnhancedPbpFactory,
)
from pbpstats.resources.enhanced_pbp import Rebound


class LiveEnhancedPbpLoader(LivePbpLoader, NbaEnhancedPbpLoader):
    """
    Loads data.nba.com source enhanced pbp data for game.
    Events are stored in items attribute as :obj:`~pbpstats.resources.enhanced_pbp.enhanced_pbp_item.EnhancedPbpItem` objects

    :param str game_id: NBA Stats Game Id
    :param source_loader: :obj:`~pbpstats.data_loader.live.enhanced_pbp.file.LiveEnhancedPbpFileLoader` or :obj:`~pbpstats.data_loader.live.enhanced_pbp.web.LiveEnhancedPbpWebLoader` object
    """

    data_provider = "live"
    resource = "EnhancedPbp"
    parent_object = "Game"

    def __init__(self, game_id, source_loader):
        self.file_directory = source_loader.file_directory
        super().__init__(game_id, source_loader)

    def _make_pbp_items(self):
        factory = LiveEnhancedPbpFactory()
        self.items = [
            factory.get_event_class(event["actionType"], event.get("subType", ""))(
                event, self.game_id
            )
            for event in self.data
        ]
        self._add_extra_attrs_to_all_events()
        self._change_team_id_on_drebs()

    def _change_team_id_on_drebs(self):
        """
        live pbp changes possession on dreb, swap team to be consistent with other sources
        """
        for event in self.items:
            if isinstance(event, Rebound):
                if event.is_real_rebound and not event.oreb:
                    event.offense_team_id = event.previous_event.offense_team_id
