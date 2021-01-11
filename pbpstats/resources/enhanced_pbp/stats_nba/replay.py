from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Replay


class StatsReplay(Replay, StatsEnhancedPbpItem):
    """
    Class for replay events
    """

    event_type = 18

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def support_ruling(self):
        return self.event_action_type == 4

    @property
    def overturn_ruling(self):
        return self.event_action_type == 5

    @property
    def ruling_stands(self):
        return self.event_action_type == 6
