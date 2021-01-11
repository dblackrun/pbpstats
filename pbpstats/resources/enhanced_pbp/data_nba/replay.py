from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Replay


class DataReplay(Replay, DataEnhancedPbpItem):
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
